from typing import List
from typing import Optional
from xmlrpc.client import DateTime
from datetime import datetime
from sqlalchemy import select
from fastapi import APIRouter, HTTPException, Depends, Request, Response, status

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import hashlib
import secrets
from loguru import logger
from ai_platform.config.resource import create_engine
from sqlalchemy import Column, String, DateTime, Boolean, Text, or_
from sqlalchemy.ext.asyncio import AsyncSession
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    # 定义表的字段
    # 主键
    id: Mapped[int] = mapped_column(primary_key=True, index=True,comment="用户ID")
    username: Mapped[str] = mapped_column(String(50),nullable=False,unique=True,comment="用户名")
    password_hash: Mapped[str] = mapped_column(String(200),nullable=False,comment="密码哈希值")
    last_date: Mapped[datetime] = mapped_column(default=datetime.now,comment="最后登录时间")
    is_active: Mapped[bool] = mapped_column(default=True,comment="是否激活")
    email: Mapped[str] = mapped_column(unique=True,nullable=True,comment="邮箱")
    avatar_url: Mapped[str] = mapped_column(String(500),nullable=True,comment="头像URL")

    @staticmethod
    def hash_password(password: str) -> str:
        """哈希密码"""
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return f"{salt}:{pwd_hash.hex()}"

    @staticmethod
    def verify_password(password_hash: str, password: str) -> bool:
        """验证密码"""
        try:
            salt, stored_hash = password_hash.split(':')
            pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
            return pwd_hash.hex() == stored_hash
        except ValueError:
            return False

class UserSession(Base):
    """用户会话表"""
    __tablename__ = 'user_sessions'

    session_token = Column(String(128), primary_key=True, index=True,comment="会话令牌")
    username = Column(String(50), nullable=False, index=True,comment="用户名")
    created_at = Column(DateTime, default=datetime.now, nullable=False,comment="创建时间")
    expires_at = Column(DateTime, nullable=False,comment="过期时间")
    is_active = Column(Boolean, default=True, nullable=False,comment="是否激活")
    user_agent = Column(String(500), nullable=True,comment="用户代理")
    ip_address = Column(String(45), nullable=True,comment="IP地址")

    def is_expired(self) -> bool:
        """检查会话是否过期"""
        return datetime.now() > self.expires_at

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'session_token': self.session_token,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_active': self.is_active,
            'user_agent': self.user_agent,
            'ip_address': self.ip_address
        }

class UserManager:
    """用户管理器"""
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

            # 创建默认管理员用户
            # await self.create_default_admin() 
            logger.info("用户表初始化完成")
        except Exception as e:
            logger.exception(f"用户表初始化失败: {e}")
            raise

    #验证用户登陆
    async def authenticate_user(self, username: str, password: str):
        try:
            user = await self.get_username(username)
            if user is None:
                return None
            if not User.verify_password(user.password_hash, password):
                return None
            await self.last_login(user.id)
            return user
        except Exception as e:
            logger.exception(e)
            return None


    #获取用户登陆信息
    async def get_username(self, username: str):
        """根据用户名获取用户信息"""
        try:
            await self._get_engine()
            async with AsyncSession(self.engine) as session:
                stmt = select(User).where(User.username == username)
                result = await session.execute(stmt)
                user = result.scalars().first()
                if user:
                    session.expunge(user)
                return user
        except Exception as e:
            logger.exception(f"根据用户名获取用户信息失败: {e}")
            return None

    #更新登陆时间
    async def last_login(self, id: int):
        try:
            await self._get_engine()
            async with AsyncSession(self.engine) as session:
                user = await session.get(User, id)
                if user:
                    user.last_date = datetime.now()
                    await session.commit()
                    session.expunge(user)
                return user
        except Exception as e:
            logger.exception(e)
            return None
    
    async def create_user(self, username: str, password: str, email: Optional[str] = None):
        """创建用户"""
        try:
            await self._get_engine()
            password_hash = User.hash_password(password)
            async with AsyncSession(self.engine) as session:
                conditions = [User.username == username]
                if email:
                    conditions.append(User.email == email)
                stmt = select(User).where(or_(*conditions))
                result = await session.execute(stmt)
                existing_user = result.scalars().first()
                if existing_user:
                    raise HTTPException(
                        status_code=409,
                        detail='用户名或者邮箱已存在'
                    )
                new_user = User(
                    username=username,
                    password_hash=password_hash,
                    email=email,
                    is_active=True
                )
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)
                session.expunge(new_user)
                return new_user
        except HTTPException:
            raise
        except Exception as e:
            logger.exception(f"创建用户失败: {e}")
            raise


user_manager = UserManager()