import datetime
from pydoc import describe
from re import M
from venv import logger

from fastapi import APIRouter, HTTPException, Depends, Request, Response, status

from pydantic import BaseModel, Field, EmailStr
from ai_platform.models.user import user_manager
from typing import Optional,TypeVar,Generic
router=APIRouter()
# 定义泛型类型变量
T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    """通用API响应模型"""
    code: int = Field(description="响应状态码")
    success: bool = Field(description="请求是否成功")
    message: str = Field(description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now, description="响应时间戳")


class UserResponse(BaseModel):
    """用户信息响应模型"""
    username: str = Field(description="用户名", examples=["admin"])
    email: Optional[str] = Field(description="邮箱地址", examples=["admin@example.com"])
    full_name: Optional[str] = Field(description="真实姓名", examples=["管理员"])
    is_active: bool = Field(description="账户是否激活", examples=[True])
    is_superuser: bool = Field(description="是否为超级用户", examples=[False])
    created_at: Optional[str] = Field(description="账户创建时间", examples=["2024-01-01T00:00:00"])
    last_login: Optional[str] = Field(description="最后登录时间", examples=["2024-01-02T12:00:00"])
    avatar_url: Optional[str] = Field(description="头像URL", examples=[None])
    bio: Optional[str] = Field(description="个人简介", examples=[None])

class LoginResponse(BaseModel):
    """登录响应模型"""
    message: str = Field(description="响应消息", examples=["登录成功"])
    user: UserResponse = Field(description="用户信息")
    session_token: str = Field(description="会话令牌", examples=["abc123xyz"])
    expires_at: str = Field(description="令牌过期时间", examples=["2024-01-02T00:00:00"])

class LoginRequest(BaseModel):
    """用户登录请求模型"""
    username: str = Field(
        min_length=3,
        max_length=50,
        description="用户名",
        examples=["admin"]
    )
    password: str = Field(
        min_length=6,
        max_length=100,
        description="密码",
        examples=["123456"]
    )
    remember_me: bool = Field(
        default=False,
        description="记住登录状态，将延长会话有效期",
        examples=[False]
    )

class RegisterRequest(BaseModel):
    """用户注册模型"""
    username: str = Field(
        min_length=1,
        max_length=50,
        description="用户名",
        examples=["admin"]
    )
    password: str = Field(
        min_length=6,
        max_length=100,
        description="密码",
        examples=["123456"]
    )
    email: str=Field(
        default=None,
        min_length=1,
        max_length=50,
        description="邮箱",
        examples=[""]
    )

@router.post("/login")
async def loging(login_data: LoginRequest, request: Request, response: Response):
    print(login_data.username, login_data.password)
    logger.info(f"Login attempt: {login_data.username}")  # 注意 logger 的用法

    user = await user_manager.authenticate_user(login_data.username, login_data.password)
    if user is None:
        logger.warning(f"Failed login for {login_data.username}")
        raise HTTPException(
            status_code=200,
            detail="用户账号或者密码输入错误"
        )

    return ApiResponse(
        success=True,
        message="登录成功",
        code=200,
        data={
  
        },
        timestamp=datetime.datetime.now()
    )


@router.post("/register")
async def register(user_data:RegisterRequest,request: Request, response: Response):
    user = await user_manager.create_user(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
    )

    return ApiResponse(
        success=True,
        code=200,
        message="注册成功",
        data={},
        timestamp=datetime.datetime.now()
    )








