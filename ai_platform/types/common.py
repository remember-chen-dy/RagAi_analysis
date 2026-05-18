
from pydantic import BaseModel, Field
from typing import Optional, TypeVar, Generic
import datetime
T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    """通用API响应模型"""
    code: int = Field(description="响应状态码")
    success: bool = Field(description="请求是否成功")
    message: str = Field(description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now, description="响应时间戳")