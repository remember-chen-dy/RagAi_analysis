from fastapi import APIRouter, File, UploadFile, HTTPException, Response, Form, Depends,UploadFile
from ai_platform.types.common import ApiResponse
from ai_platform.models.session import session_manager
from pydantic import BaseModel, Field
from uuid import UUID
import uuid
import datetime
from typing import List,Optional
from loguru import logger
router=APIRouter()

class CreateChartRequest(BaseModel):
    """创建图表请求模型"""
    knowledge_base_ids: Optional[List[str]] = Field(
        None, 
        description="知识库ID列表（UUID字符串格式）"
    )
class DeleteChartRequest(BaseModel):
    """删除图表请求模型"""
    session_id: str = Field(..., description="会话ID")

#创建创建会话
@router.post("/create")
async def create_chart(request: CreateChartRequest):
    """创建会话"""
    try:
        session_id=str(uuid.uuid4())
        await session_manager.create_session(session_id,request.knowledge_base_ids)
        return ApiResponse(
            message="会话创建成功",
            code=200,
            success=True,
            timestamp=datetime.datetime.now(),
            data={"session_id": session_id})
    except Exception as e:
        logger.exception(f"创建会话失败: {e}")
        raise HTTPException(status_code=500, detail="创建会话失败")

#删除会话
@router.post("/delete")

async def delete_chart(request: DeleteChartRequest):
    """删除会话"""
    try:
        existing = await session_manager.delete_session(request.session_id)
        if existing is None:
            raise ApiResponse(
                code=200, 
                message="会话不存在",
                success=False,
                data={},
                timestamp=datetime.datetime.now(),
                )

        return ApiResponse(
            message="会话删除成功",
            code=200,
            success=True,
            timestamp=datetime.datetime.now())
    except Exception as e:
        logger.exception(f"删除会话失败: {e}")
        raise HTTPException(status_code=500, detail="删除会话失败")
        
#获取所有会话
@router.get("/all")
async def get_all_sessions():
    """获取所有会话"""
    try:
        sessions = await session_manager.get_all_sessions()
        return ApiResponse(
            message="会话列表获取成功",
            code=200,
            success=True,
            timestamp=datetime.datetime.now(),
            data=sessions)
    except Exception as e:
        logger.exception(f"获取会话列表失败: {e}")
        raise HTTPException(status_code=500, detail="获取会话列表失败")
        

