import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple

from loguru import logger
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from ..models import KnowledgeBase, KnowledgeBaseFile, Base
from ai_platform.config.resource import create_engine
from pydantic import BaseModel, Field
from uuid import UUID
from sqlalchemy import delete, update


class KnowledgeService:
    """知识库服务"""
    def __init__(self):
        self.engine = None
        self.session = None
        self.knowledge_base_service = None

    async def _get_engine(self):
            """获取数据库引擎 创建适量123"""
            if self.engine is None:
                self.engine = create_engine()
            return self.engine

    async def init_knowledge_tables(self):
        """初始化数据库表"""
        try:
            engine = await self._get_engine()
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            # 创建默认知识库
            # await self.create_default_knowledge_base() 
            logger.info("知识库表初始化完成")
        except Exception as e:
            logger.exception(f"知识库表初始化失败: {e}")
            raise

    #创建知识库
    async def create_knowledge_base(self, name: str, description: str = None,initial_settings: Dict[str, Any] = None):
        """创建知识库"""
        try:
            await self._get_engine()
            async with AsyncSession(self.engine) as session:
                new_knowledge_base = KnowledgeBase(
                    id=uuid.uuid4(),
                    name=name,
                    description=description,
                    create_time=datetime.now(),
                    update_time=datetime.now(),
                    status="building",
                    settings=initial_settings or {}
                )
                
                session.add(new_knowledge_base)
                await session.commit()
                session.refresh(new_knowledge_base)
                return new_knowledge_base
        except Exception as e:
            logger.exception(f"创建知识库失败: {e}")
            raise        
    
    # 获取知识库列表
    async def get_knowledge_base_list(self):
        """获取知识库列表"""
        try:
                await self._get_engine()
                async with AsyncSession(self.engine) as session:
                    query = select(KnowledgeBase).order_by(KnowledgeBase.create_time.desc())
                    knowledge_base_list = await session.execute(query)
                    return knowledge_base_list.scalars().all()
        except Exception as e:
            logger.exception(f"获取知识库列表失败: {e}")
            raise

    #删除知识库
    async def delete_knowledge_base(self, knowledge_base_id: UUID):
        """删除知识库"""
        try:
            await self._get_engine()
            async with AsyncSession(self.engine) as session:

                await session.execute(delete(KnowledgeBase).where(KnowledgeBase.id == knowledge_base_id))
                await session.commit()
                return True
        except Exception as e:
            logger.exception(f"删除知识库失败: {e}")
            raise
    
    #修改知识库
    async def update_knowledge_base(self, knowledge_base_id: UUID, name: str = None, description: str = None):
        """修改知识库"""
        try:
            await self._get_engine()
            async with AsyncSession(self.engine) as session:
                knowledge_base = await session.get(KnowledgeBase, knowledge_base_id)
                if knowledge_base is None:
                    raise ValueError(f"知识库 {knowledge_base_id} 不存在")
                if name:
                    knowledge_base.name = name
                if description:
                    knowledge_base.description = description
                await session.commit()
                return knowledge_base
        except Exception as e:
            logger.exception(f"修改知识库失败: {e}")
            raise

    #修改知识库设置
    async def update_knowledge_base_settings(self, knowledge_base_id: UUID, settings: Dict[str, Any] = None):
        """修改知识库设置"""
        try:
            await self._get_engine()    
            async with AsyncSession(self.engine) as session:
                knowledge_base = await session.get(KnowledgeBase, knowledge_base_id)
                if knowledge_base is None:
                    raise ValueError(f"知识库 {knowledge_base_id} 不存在")
                if settings:
                    knowledge_base.settings = settings
                else:
                    knowledge_base.settings = {}
                await session.commit()
                return knowledge_base
        except Exception as e:
            logger.exception(f"修改知识库设置失败: {e}")
            raise


knowledge_service =KnowledgeService()