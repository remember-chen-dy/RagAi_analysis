from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
import textwrap
from sqlalchemy import create_engine
from ai_platform.config.setting import settings
#创建数据库引擎
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

def create_engine() -> AsyncEngine:
    """创建异步数据库引擎"""
    engine = create_async_engine(  # ✅ 使用 create_async_engine
        settings.async_postgres_url,
        pool_size=20,
        max_overflow=40,
        pool_recycle=3600,
        pool_pre_ping=True,
    )
    return engine