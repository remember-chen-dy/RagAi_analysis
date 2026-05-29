import json
from abc import ABC, abstractmethod
from typing import List, Optional, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine
from llama_index.core import Settings

from ai_platform.config.resource import (
    get_vector_store,
    get_vector_index,
    get_llm,
    get_embedding,
    get_chat_context_db,
    get_db_engine,
    get_llm_reranker,
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
                             "回答要简洁、准确、有帮助。 "
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

    def _build_filters(self, knowledge_base_ids: List[str]) -> MetadataFilters:
        """知识库过滤条件"""
        return MetadataFilters(
            filters=[
                MetadataFilter(
                    key="knowledge_base_id",
                    value=knowledge_base_ids if knowledge_base_ids else ["__none__"],
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
        """创建RAG引擎"""
        pass


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

        try:
            nodes = await self.vector_store.aquery(
                query_str,
                self.similarity_top_k,
                self.filters
            )
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
                retriever=retriever,  #检索
                memory=self.memory_block,  #记忆
                node_postprocessors=[LongContextReorder(), get_llm_reranker()], #后处理
                llm=self.llm,  #LLM
                verbose=True,  #是否打印详细信息
            )

            return chat_engine
        except Exception as e:
            logger.exception(f"向量检索引擎创建失败: {e}")
            raise



class HybridRagEngine(BaseRagEngine):
    """混合检索引擎"""

    def create_engine(
        self,
        knowledge_base_ids: List[str],
        similarity_top_k: int = 5
    ):
        """创建混合检索引擎"""
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

        bm25_nodes = vector_store.get_nodes(filters=filters)
        if bm25_nodes:
            bm25_retriever = BM25Retriever.from_defaults(
                nodes=bm25_nodes,
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
            logger.warning("BM25 无可用于索引的节点，回退到纯向量检索")
            hybrid_retriever = vector_retriever
    

        chat_engine = CondensePlusContextChatEngine.from_defaults(
            retriever=hybrid_retriever,
            memory=self.memory_block,
            llm=self.llm,
            node_postprocessors=[LongContextReorder(), get_llm_reranker()],
            verbose=True,
        )

        return chat_engine


class RagEngineFactory:
    """RAG引擎工厂类"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self._engines = {}

    async def stream_query(
        self,
        query: str,
        index_type: str,
        knowledge_base_ids: List[str],
        similarity_top_k: int = 5
    ) -> AsyncGenerator[str, None]:
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

        streaming_response = await query_engine.astream_chat(query)
        response_text = ""
        buffered_tokens = []

        async for token in streaming_response.async_response_gen():
            token_text = token if isinstance(token, str) else str(token)
            response_text += token_text
            buffered_tokens.append(token_text)

        if 'Empty Response' in response_text:
            empty_prompt = (
                "根据用户的问题，知识库中没有检索到相关信息。"
                "请直接根据你的知识回答用户问题，并在回答开头明确说明【以下回答由AI大模型直接生成，未基于知识库内容，仅供参考】。"
                "用户的问题是：{query}"
            )
            prompt = empty_prompt.format(query=query)
            llm_stream = await engine_impl.llm.astream_complete(prompt)
            response_text = ""
            previous_text = ""
            async for token in llm_stream:
                token_text = token if isinstance(token, str) else str(token)
                delta = token_text
                if token_text.startswith(previous_text):
                    delta = token_text[len(previous_text):]
                previous_text = token_text
                if delta:
                    yield f"data: {json.dumps({'token': delta, 'done': False})}\n\n"
            response_text = previous_text
        else:
            for token_text in buffered_tokens:
                yield f"data: {json.dumps({'token': token_text, 'done': False})}\n\n"

        yield f"data: {json.dumps({'done': True, 'response': response_text})}\n\n"
