from sqlalchemy import Column, String, DateTime, Integer, Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from ai_platform.config.resource import create_engine
from typing import List,Union
import uuid
from datetime import datetime
import json
from loguru import logger
from sqlalchemy import select,text

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
                    kb_ids = row.knowledge_base_ids
                    if isinstance(kb_ids, str):
                        try:
                            kb_ids = json.loads(kb_ids)
                        except (json.JSONDecodeError, TypeError):
                            kb_ids = []
                    sessions.append(
                         {
                       "id": row.session_id,
                        "created_at": row.created_at,
                        "last_activity": row.last_activity,
                        "message_count": row.message_count,
                        "last_message": row.last_message,
                        "last_message_role": row.last_message_role,
                        "knowledge_base_ids": kb_ids or []
                        }
                    )
                
                return sessions
                
        except Exception as e:
            logger.exception(f"获取会话列表失败: {e}")
            return []
    
    #查询历史会话
    async def get_session_history(self, session_id: str) -> List[dict]:
        """获取会话历史记录"""
        try:
            engine = await self._get_engine()
            async with AsyncSession(engine) as session:
                result = await session.execute(text("SELECT * FROM chat_history WHERE key = :session_id ORDER BY id ASC"), {"session_id": session_id})
                rows = result.fetchall()
                
                history = []
                for row in rows:
                    row_dict = dict(row._mapping)
                    data_field = row_dict.get("data", {})

                    if isinstance(data_field, str):
                        try:
                            data_field = json.loads(data_field)
                        except (json.JSONDecodeError, TypeError):
                            data_field = {}

                    timestamp_ns = 0
                    if row_dict.get("timestamp"):
                        if isinstance(row_dict["timestamp"], int):
                            if row_dict["timestamp"] > 1e18:
                                timestamp_ns = row_dict["timestamp"]
                            else:
                                timestamp_ns = int(row_dict["timestamp"] * 1e9)
                        elif hasattr(row_dict["timestamp"], "timestamp"):
                            timestamp_ns = int(row_dict["timestamp"].timestamp() * 1e9)
                    
                    history_item = {
                        "id": row_dict.get("id"),
                        "key": row_dict.get("key", session_id),
                        "timestamp": timestamp_ns,
                        "role": row_dict.get("role", "user"),
                        "status": row_dict.get("status", "active"),
                        "data": data_field if isinstance(data_field, dict) else {}
                    }
                    history.append(history_item)
                
                return history
        except Exception as e:
            logger.exception(f"获取会话历史记录失败: {e}")
            return []

    async def save_chat_message(self, session_id: str, role: str, message_text: str):
        """保存聊天消息到历史记录"""
        try:
            engine = await self._get_engine()
            async with AsyncSession(engine) as db_session:
                import time
                import json

                message_data = {
                    "role": role,
                    "additional_kwargs": {},
                    "blocks": [
                        {
                            "block_type": "text",
                            "text": message_text
                        }
                    ]
                }

                insert_sql = text(
                    "INSERT INTO chat_history (key, timestamp, role, status, data) "
                    "VALUES (:key, :timestamp, :role, :status, :data)"
                )

                await db_session.execute(insert_sql, {
                    "key": session_id,
                    "timestamp": int(time.time() * 1e9),
                    "role": role,
                    "status": "active",
                    "data": json.dumps(message_data, ensure_ascii=False)
                })
                await db_session.commit()
                logger.info(f"保存聊天消息: session={session_id}, role={role}")

            await self._update_session_stats(session_id, role, message_text)

        except Exception as e:
            logger.exception(f"保存聊天消息失败: {e}")

    async def _update_session_stats(self, session_id: str, role: str, message_text: str):
        """更新会话统计信息（message_count, last_message, last_activity）"""
        try:
            engine = await self._get_engine()
            async with AsyncSession(engine) as db_session:
                stmt = select(ChatSession).where(ChatSession.session_id == session_id)
                result = await db_session.execute(stmt)
                chat_session = result.scalar_one_or_none()
                if chat_session:
                    chat_session.last_activity = datetime.now()
                    chat_session.message_count = (chat_session.message_count or 0) + 1
                    chat_session.last_message = message_text
                    chat_session.last_message_role = role
                    await db_session.commit()
        except Exception as e:
            logger.exception(f"更新会话统计失败: {e}")




session_manager = SessionManager()



