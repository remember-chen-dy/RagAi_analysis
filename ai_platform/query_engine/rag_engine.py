from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncEngine

from ai_platform.config.resource import (
    get_vector_store,
    get_vector_index,
    get_llm,
    get_embedding,
    get_chat_context_db,
    get_db_engine
)
from llama_index.core.memory import Memory, StaticMemoryBlock, FactExtractionMemoryBlock, VectorMemoryBlock
from llama_index.core.vector_stores import MetadataFilters, MetadataFilter, FilterOperator
from llama_index.core.chat_engine import CondensePlusContextChatEngine
from llama_index.core.retrievers import QueryFusionRetriever
from llama_index.core.retrievers.fusion_retriever import FUSION_MODES
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.base.llms.types import TextBlock
from llama_index.core.postprocessor import LongContextReorder
from llama_index.core.indices.property_graph import PropertyGraphIndex
from llama_index.core.vector_stores import VectorStoreQuery
from llama_index.core.schema import NodeWithScore
from llama_index.core import VectorStoreIndex
from loguru import logger


class BaseRagEngine(ABC):
    """RAG引擎基类"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.llm = get_llm()
        self.embed_model = get_embedding()
        self.chat_context_db = get_chat_context_db()
        self.async_engine = get_db_engine()

        self.memory_block = self._create_memory_block(session_id)

    def _create_memory_block(self, session_id: str) -> Memory:
        return Memory.from_defaults(
            session_id=session_id,
            token_limit=3000,
            token_flush_size=500,
            memory_blocks=[
                StaticMemoryBlock(
                    name="core_info",
                    static_content=[TextBlock(
                        text="你是一个AI智能助手，可以友好地基于提供的上下文信息回答用户的问题。"
                             "如果上下文信息中没有相关内容，你可以告诉用户你无法回答该问题。"
                             "回答要简洁、准确、有帮助。"
                    )],
                    priority=0,
                ),
                FactExtractionMemoryBlock(
                    name="extracted_info",
                    llm=self.llm,
                    max_facts=20,
                    priority=1,
                ),
                VectorMemoryBlock(
                    name="vector_memory",
                    vector_store=self.chat_context_db,
                    priority=2,
                    embed_model=self.embed_model,
                ),
            ],
            table_name="chat_history",
            chat_history_token_ratio=0.5,
            async_engine=self.async_engine,
        )

    def _build_filters(self, knowledge_base_ids: List[str]) -> Optional[MetadataFilters]:
        if not knowledge_base_ids:
            return None

        return MetadataFilters(
            filters=[
                MetadataFilter(
                    key="knowledge_base_id",
                    value=knowledge_base_ids,
                    operator=FilterOperator.IN,
                )
            ]
        )

    @abstractmethod
    def create_engine(
        self,
        knowledge_base_ids: List[str],
        similarity_top_k: int = 5
    ):
        pass


class VectorRagEngine(BaseRagEngine):
    """向量检索引擎"""

    def create_engine(
        self,
        knowledge_base_ids: List[str],
        similarity_top_k: int = 5
    ):
        """创建向量检索引擎"""
        try:
            filters = self._build_filters(knowledge_base_ids)
            logger.info(f"VectorRagEngine filters: {filters}")

            vector_store = get_vector_store()
            index = get_vector_index()

            retriever = VectorStoreRetriever(
                vector_store=vector_store,
                index=index,
                filters=filters,
                similarity_top_k=similarity_top_k,
                embed_model=self.embed_model,
            )

            chat_engine = CondensePlusContextChatEngine.from_defaults(
                retriever=retriever,
                memory=self.memory_block,
                llm=self.llm,
                verbose=True,
            )

            return chat_engine
        except Exception as e:
            logger.exception(f"向量检索引擎创建失败: {e}")
            raise


class VectorStoreRetriever:
    """基于PGVectorStore的自定义检索器"""

    def __init__(self, vector_store, index, filters=None, similarity_top_k=5, embed_model=None):
        self.vector_store = vector_store
        self.index = index
        self.filters = filters
        self.similarity_top_k = similarity_top_k
        self.embed_model = embed_model

    async def aretrieve(self, query_str: str) -> List[NodeWithScore]:
        """异步检索"""
        logger.info(f"VectorStoreRetriever query: {query_str}")

        try:
            nodes = await self.vector_store.aquery(
                query_str,
                self.similarity_top_k,
                self.filters
            )
            logger.info(f"VectorStoreRetriever found {len(nodes)} nodes")
            return nodes
        except Exception as e:
            logger.warning(f"PGVectorStore aquery failed: {e}, fallback to index retriever")
            retriever = self.index.as_retriever(
                filters=self.filters,
                similarity_top_k=self.similarity_top_k,
            )
            return await retriever.aretrieve(query_str)

    def retrieve(self, query_str: str) -> List[NodeWithScore]:
        import asyncio
        try:
            return asyncio.get_event_loop().run_until_complete(self.aretrieve(query_str))
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(self.aretrieve(query_str))


class HybridRagEngine(BaseRagEngine):
    """混合检索引擎"""

    def create_engine(
        self,
        knowledge_base_ids: List[str],
        similarity_top_k: int = 5
    ):
        filters = self._build_filters(knowledge_base_ids)

        vector_store = get_vector_store()
        index = get_vector_index()

        vector_retriever = VectorStoreRetriever(
            vector_store=vector_store,
            index=index,
            filters=filters,
            similarity_top_k=similarity_top_k,
            embed_model=self.embed_model,
        )

        nodes = self._get_nodes_from_store(vector_store, knowledge_base_ids)

        if nodes:
            bm25_retriever = BM25Retriever.from_defaults(
                nodes=nodes,
                similarity_top_k=similarity_top_k,
            )
            hybrid_retriever = QueryFusionRetriever(
                retrievers=[bm25_retriever, vector_retriever],
                similarity_top_k=similarity_top_k,
                num_queries=1,
                mode=FUSION_MODES.RECIPROCAL_RANK,
                use_async=True,
                verbose=True,
            )
        else:
            logger.warning("No nodes for BM25, using vector retriever only")
            hybrid_retriever = vector_retriever

        chat_engine = CondensePlusContextChatEngine.from_defaults(
            retriever=hybrid_retriever,
            memory=self.memory_block,
            llm=self.llm,
            node_postprocessors=[LongContextReorder()],
            verbose=True,
        )

        return chat_engine

    def _get_nodes_from_store(self, vector_store, knowledge_base_ids: List[str]):
        """从PGVectorStore获取节点"""
        import asyncio
        try:
            filters = self._build_filters(knowledge_base_ids)
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as pool:
                        future = pool.submit(asyncio.run, vector_store.aget_nodes(filters=filters))
                        nodes = future.result()
                else:
                    nodes = loop.run_until_complete(vector_store.aget_nodes(filters=filters))
            except RuntimeError:
                nodes = asyncio.run(vector_store.aget_nodes(filters=filters))
            return nodes
        except Exception as e:
            logger.warning(f"Failed to get nodes from store: {e}")
            return []


class RagEngineFactory:
    """RAG引擎工厂类"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self._engines = {}

    async def query(
        self,
        query: str,
        index_type: str,
        knowledge_base_ids: List[str],
        similarity_top_k: int = 5
    ):
        if index_type == "vector":
            engine_impl = VectorRagEngine(self.session_id)
        elif index_type == "hybrid":
            engine_impl = HybridRagEngine(self.session_id)
        else:
            raise ValueError(f"Unsupported index_type: {index_type}")

        query_engine = engine_impl.create_engine(
            knowledge_base_ids=knowledge_base_ids,
            similarity_top_k=similarity_top_k
        )

        response = await query_engine.achat(query)
        logger.info(f"Query response type: {type(response)}")

        response_text = ""
        source = []

        if response:
            if hasattr(response, 'response') and response.response:
                response_text = response.response
            else:
                response_text = str(response) if response else "无法生成回复"

            if hasattr(response, 'source_nodes') and response.source_nodes:
                for node in response.source_nodes:
                    try:
                        source.append({
                            "node_id": node.node.node_id if hasattr(node, 'node') and hasattr(node.node, 'node_id') else None,
                            "content": node.node.get_content() if hasattr(node, 'node') and hasattr(node.node, 'get_content') else str(node.node) if hasattr(node, 'node') else None,
                            "score": node.score if hasattr(node, 'score') else None,
                            "metadata": node.node.metadata if hasattr(node, 'node') and hasattr(node.node, 'metadata') else None,
                        })
                    except Exception as e:
                        logger.warning(f"Error extracting source node: {e}")

        return {
            "source": source,
            "query": query,
            "response": response_text,
            "metadata": {
                "session_id": self.session_id,
                "index_type": index_type,
                "knowledge_base_ids": knowledge_base_ids,
            }
        }
