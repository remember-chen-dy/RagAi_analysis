from sqlalchemy import Column, String, DateTime, Integer, Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from ai_platform.config.resource import create_engine
from typing import List,Union
import uuid
from datetime import datetime
import json
from loguru import logger
Base = declarative_base()


class ChatSession(Base):
    """聊天会话表"""
    __tablename__ = 'chat_sessions'

    session_id = Column(String(64), primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    last_activity = Column(DateTime, default=datetime.now(), nullable=False)
    message_count = Column(Integer, default=0, nullable=False)
    last_message = Column(Text, nullable=True)
    last_message_role = Column(String(20), nullable=True)
    chat_metadata = Column(Text, nullable=True)
    knowledge_base_ids = Column(Text, nullable=True)  # 新增：存储知识库ID列表的JSON字符串

    def set_knowledge_base_ids(self, kb_ids: List[str]):
        """设置知识库ID列表"""
        if kb_ids:
            self.knowledge_base_ids = json.dumps(kb_ids)
        else:
            self.knowledge_base_ids = None    

class SessionManager:
    """会话管理器"""
    def __init__(self):
        self.engine = None

    async def _get_engine(self):
        """获取数据库引擎 创建适量"""
        if self.engine is None:
            self.engine = create_engine()
        return self.engine

    async def init_tables(self):
        """初始化数据库表"""
        try:
            engine = await self._get_engine()
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("会话表初始化完成")
        except Exception as e:
            logger.exception(f"会话表初始化失败: {e}")
            raise

    #创建会话
    async def create_session(self, session_id: str,knowledge_base_ids: Union[List[Union[str,uuid.UUID]],None] = None,):
        """创建会话"""
        try:
            engine = await self._get_engine()
            async with AsyncSession(engine) as session:
                # 检查会话是否已存在
                existing = await session.get(ChatSession, session_id)
                if existing:
                    return existing
                # 创建新会话
                new_session = ChatSession(
                    session_id=session_id,
                    created_at=datetime.now(),
                    last_activity=datetime.now(),
                    message_count=0
                )
                
                # 设置知识库ID列表
                if knowledge_base_ids:
                    new_session.set_knowledge_base_ids(knowledge_base_ids)
                
                session.add(new_session)
                await session.commit()
                await session.refresh(new_session)
                logger.info(f"创建新会话: {session_id}, 知识库: {knowledge_base_ids}")
                return new_session

        except Exception as e:
            logger.exception(f"创建会话失败: {e}")
            raise
    
    #删除会话
    async def delete_session(self, session_id: str):
        """删除会话"""
        try:
            engine = await self._get_engine()
            async with AsyncSession(engine) as session:
                # 检查会话是否存在
                existing = await session.get(ChatSession, session_id)
                if not existing:
                    logger.warning(f"会话 {session_id} 不存在")
                    return None
                # 删除会话
                session.delete(existing)
                await session.commit()
                logger.info(f"删除会话: {session_id}")
        except Exception as e:
            logger.exception(f"删除会话失败: {e}")
            raise

    async def get_all_sessions(self, limit: int = 50, offset: int = 0) -> List[dict]:
        """获取所有会话列表"""
        try:
            engine = await self._get_engine()
            async with AsyncSession(engine) as session:
                from sqlalchemy import select
                stmt = (
                    select(ChatSession)
                    .order_by(ChatSession.last_activity.desc())
                    .limit(limit)
                    .offset(offset)  # ← 添加 offset
                )
                result = await session.execute(stmt)
                sessions =[]
                for row in result.scalars().all():
                    sessions.append(
                         {
                       "id": row.session_id,
                        "created_at": row.created_at,
                        "last_activity": row.last_activity,
                        "message_count": row.message_count,
                        "last_message": row.last_message,
                        "last_message_role": row.last_message_role,
                        "knowledge_base_ids":  json.dumps(row.knowledge_base_ids)  # 新增：返回会话的知识库配置
                        }
                    )
                
                return sessions
                
        except Exception as e:
            logger.exception(f"获取会话列表失败: {e}")
            return []

session_manager = SessionManager()



