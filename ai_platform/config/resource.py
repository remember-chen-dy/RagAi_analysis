import os
from typing import Optional

from llama_index.core import StorageContext, VectorStoreIndex, PropertyGraphIndex, TreeIndex
from llama_index.core.graph_stores.types import GraphStore, PropertyGraphStore
from llama_index.core.postprocessor import SentenceTransformerRerank, LLMRerank
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.embeddings.dashscope import DashScopeEmbedding
from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels
from llama_index.multi_modal_llms.dashscope import (
    DashScopeMultiModal,
    DashScopeMultiModalModels,
)
import dashscope
from llama_index.storage.docstore.postgres import PostgresDocumentStore
from llama_index.vector_stores.postgres import PGVectorStore
from loguru import logger
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from ai_platform.config.setting import settings
# from ai_platform.services.kafka_service import KafkaService
# from ai_platform.services.knowledge_service import KnowledgeService
from ai_platform.services.minio_service import  MinioService



class ResourceManager(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    llm: DashScope = Field(description="llm client")
    embedding: DashScopeEmbedding = Field(description="embedding client")
    vl_client: DashScopeMultiModal = Field(description="multi-modal llm client")
    doc_store: PostgresDocumentStore = Field(description="document store client")
    vector_db: PGVectorStore = Field(description="vector database client")
    chat_context_db: PGVectorStore = Field(default=None, description="chat context vector database client")
    # graph_db: Optional[GraphStore] = Field(default=None, description="graph database client")
    # graph_property_db: Optional[PropertyGraphStore] = Field(default=None, description="graph property database client")
    storage_context: Optional[StorageContext] = Field(default=None, description="storage context manager")
    db_engine: AsyncEngine | None = Field(default=None, description="database engine")
    # mino_service: MinioService = Field(description="MinIO service")
    # knowledge_base: object = Field(description="knowledge base service")
    vector_index: VectorStoreIndex | None = Field(default=None, description="vector index client")
    # property_graph_index: PropertyGraphIndex | None = Field(default=None, description="property graph index client")
    # tree_index: TreeIndex | None = Field(default=None, description="tree index client")
    # cross_encoder_reranker: BaseNodePostprocessor = Field(default=None, description="cross encoder reranker model")
    llm_reranker: BaseNodePostprocessor = Field(default=None, description="llm reranker model")


_resource_instance: Optional[ResourceManager] = None


def create_engine() -> AsyncEngine:
    """创建并配置数据库引擎"""
    engine = create_async_engine(
        settings.async_postgres_url,
        pool_size=20,
        max_overflow=40,
        pool_recycle=3600,
        pool_pre_ping=True,
        connect_args={
            "server_settings": {
                "jit": "off"  # 关闭JIT编译，避免一些连接问题
            }
        }
    )
    return engine

def init_resource():
    global _resource_instance
    if _resource_instance is None:
        _resource_instance = ResourceManager(
            vector_db=PGVectorStore.from_params(
                database=settings.postgres_db,
                user=settings.postgres_user,
                password=settings.postgres_password,
                table_name="data_vector_store",
                host=settings.postgres_host,
                port=settings.postgres_port,
                hybrid_search=True,
            ),
            # 聊天上下文向量数据库
            chat_context_db=PGVectorStore.from_params(
                database=settings.postgres_db,
                user=settings.postgres_user,
                password=settings.postgres_password,
                table_name="chat_context_store",
                host=settings.postgres_host,
                port=settings.postgres_port,
                hybrid_search=True,
            ),
            doc_store=PostgresDocumentStore.from_params(
                database=settings.postgres_db,
                user=settings.postgres_user,
                password=settings.postgres_password,
                host=settings.postgres_host,
                port=settings.postgres_port,
            ),
            # graph_db=Neo4jGraphStore(
            #     database=settings.neo4j_db,
            #     username=settings.neo4j_username,
            #     password=settings.neo4j_password,
            #     url=settings.neo4j_url
            # ),
            # graph_property_db=Neo4jPropertyGraphStore(
            #     database=settings.neo4j_db,
            #     username=settings.neo4j_username,
            #     password=settings.neo4j_password,
            #     url=settings.neo4j_url
            # ),
            llm=DashScope(
                            model_name=DashScopeGenerationModels.QWEN_MAX,
                            # model_name="kimi-k2.6",
                            api_key=os.getenv("DASHSCOPE_APIKEY"),
                            stream=False,
                            max_tokens=2000,  # 增加输出长度限制，支持更长的回复
                            temperature=0.2,  # 设置温度参数，让回复更稳定
                          ),
            embedding=DashScopeEmbedding(
                model_name="text-embedding-v2",
                # model_name="tongyi-embedding-vision-plus-2026-03-06",
                api_key=os.getenv("DASHSCOPE_APIKEY"),
            ),
            vl_client=DashScopeMultiModal(
                model_name='qwen3-vl-8b-instruct',
                api_key=os.getenv("DASHSCOPE_APIKEY"),
                stream=False,
            ),
            # cross_encoder_reranker=SentenceTransformerRerank(
            #     model="BAAI/bge-reranker-base",
            #     top_n=5
            # ),
            
            # # kafka_service=KafkaService(),
            # mino_service=MinioService(),
            # knowledge_base=KnowledgeService(),
            db_engine=create_engine()

        )
        _resource_instance.storage_context = StorageContext.from_defaults(
            vector_store=_resource_instance.vector_db,
            docstore=_resource_instance.doc_store,
        )

        try:
            _resource_instance.vector_index = VectorStoreIndex(
                embed_model=_resource_instance.embedding,
                storage_context=_resource_instance.storage_context,
                nodes=[],
            )

            # _resource_instance.tree_index = TreeIndex.from_documents(
            #     llm=get_llm(),
            #     embed_model=_resource_instance.embedding,
            #     storage_context=_resource_instance.storage_context,
            #     documents=[]
            # )

            _resource_instance.llm_reranker = LLMRerank(
                llm=_resource_instance.llm,
                choice_batch_size=5,
                top_n=5,
            )

            logger.info("成功从现有存储加载向量索引")
        except Exception as e:
            logger.exception(f"无法从现有存储加载向量索引: {e}")


def get_vector_store() -> PGVectorStore:
    if _resource_instance is None:
        raise RuntimeError("PGVectorStore has not been initialized.")
    return _resource_instance.vector_db


def get_llm() -> DashScope:
    if _resource_instance is None:
        raise RuntimeError("LLM has not been initialized.")
    return _resource_instance.llm


def get_embedding() -> DashScopeEmbedding:
    if _resource_instance is None:
        raise RuntimeError("Embedding model has not been initialized.")
    return _resource_instance.embedding

def get_vl_client() -> DashScopeMultiModal:
    if _resource_instance is None:
        raise RuntimeError("Resource manager has not been initialized. Call init_resource() first.")
    return _resource_instance.vl_client



# def get_minio_service() -> MinioService:
#     if _resource_instance is None:
#         raise RuntimeError("Minio service has not been initialized.")
#     return _resource_instance.mino_service


# def get_knowledge_service() -> KnowledgeService:
#     if _resource_instance is None:
#         raise RuntimeError("Knowledge service has not been initialized.")
#     return _resource_instance.knowledge_base


# def get_storage_context() -> StorageContext:
#     if _resource_instance is None or _resource_instance.storage_context is None:
#         raise RuntimeError("Storage context has not been initialized.")
#     return _resource_instance.storage_context

#VectorStoreIndex 向量索引
def get_vector_index() -> VectorStoreIndex:
    if _resource_instance is None or _resource_instance.vector_index is None:
        raise RuntimeError("Vector index has not been initialized.")
    return _resource_instance.vector_index


# def get_property_graph_index() -> PropertyGraphIndex:
#     if _resource_instance is None or _resource_instance.property_graph_index is None:
#         raise RuntimeError("Property graph index has not been initialized.")
#     return _resource_instance.property_graph_index


# def get_tree_index() -> TreeIndex:
#     if _resource_instance is None or _resource_instance.tree_index is None:
#         raise RuntimeError("Tree index has not been initialized.")
#     return _resource_instance.tree_index


def get_db_engine() -> AsyncEngine:
    if _resource_instance is None or _resource_instance.db_engine is None:
        raise RuntimeError("Database engine has not been initialized.")
    return _resource_instance.db_engine


# def get_cross_encoder_reranker() -> BaseNodePostprocessor:
#     if _resource_instance is None or _resource_instance.cross_encoder_reranker is None:
#         raise RuntimeError("Cross encoder reranker has not been initialized.")
#     return _resource_instance.cross_encoder_reranker


def get_llm_reranker() -> BaseNodePostprocessor:
    if _resource_instance is None or _resource_instance.llm_reranker is None:
        raise RuntimeError("LLM reranker has not been initialized.")
    return _resource_instance.llm_reranker


# def get_doc_store() -> PostgresDocumentStore:
#     if _resource_instance is None or _resource_instance.doc_store is None:
#         raise RuntimeError("Document store has not been initialized.")
#     return _resource_instance.doc_store

def get_chat_context_db() -> PGVectorStore:
    if _resource_instance is None or _resource_instance.chat_context_db is None:
        raise RuntimeError("Chat context vector database has not been initialized.")
    return _resource_instance.chat_context_db