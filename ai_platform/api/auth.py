import datetime
from pydoc import describe
from re import M
from venv import logger

from fastapi import APIRouter, HTTPException, Depends, Request, Response, status

from pydantic import BaseModel, Field, EmailStr
from ai_platform.models.user import user_manager
from typing import Optional,TypeVar,Generic
from ai_platform.config.auth import create_access_token, get_current_user
from ai_platform.config.setting import settings
router=APIRouter()
T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    code: int = Field(description="响应状态码")
    success: bool = Field(description="请求是否成功")
    message: str = Field(description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now, description="响应时间戳")

class UserResponse(BaseModel):
    username: str = Field(description="用户名", examples=["admin"])
    email: Optional[str] = Field(description="邮箱地址", examples=["admin@example.com"])
    is_active: bool = Field(description="账户是否激活", examples=[True])
    avatar_url: Optional[str] = Field(description="头像URL", examples=[None])

class LoginResponse(BaseModel):
    token: str = Field(description="JWT访问令牌")
    token_type: str = Field(default="Bearer", description="令牌类型")
    expires_in: int = Field(description="令牌过期时间(秒)")
    user: UserResponse = Field(description="用户信息")

class LoginRequest(BaseModel):
    username: str = Field(
        min_length=2,
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

class RegisterRequest(BaseModel):
    username: str = Field(
        min_length=2,
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
    email: str = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="邮箱",
        examples=[""]
    )

@router.post("/login")
async def loging(request: LoginRequest):
    user = await user_manager.authenticate_user(request.username, request.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户账号或者密码输入错误"
        )

    token = create_access_token(data={"sub": user.username, "user_id": user.id})
    expires_in = settings.jwt_access_token_expire_minutes * 60

    return ApiResponse(
        success=True,
        message="登录成功",
        code=200,
        data={
            "token": token,
            "token_type": "Bearer",
            "expires_in": expires_in,
            "user": {
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "avatar_url": user.avatar_url,
            }
        },
        timestamp=datetime.datetime.now()
    )


@router.post("/register")
async def register(user_data: RegisterRequest, request: Request, response: Response):
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


@router.get("/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    user = await user_manager.get_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )
    return ApiResponse(
        success=True,
        code=200,
        message="获取用户信息成功",
        data={
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "avatar_url": user.avatar_url,
        },
        timestamp=datetime.datetime.now()
    )
