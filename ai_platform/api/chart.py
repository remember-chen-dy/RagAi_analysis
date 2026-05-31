from fastapi import APIRouter, File, UploadFile, HTTPException, Response, Form, Depends,UploadFile
from ai_platform.types.common import ApiResponse
from ai_platform.models.session import session_manager
from ai_platform.query_engine.chat_instance import ChatInstance
from ai_platform.config.auth import get_current_user
from pydantic import BaseModel, Field
from uuid import UUID
import uuid
import datetime
from typing import List,Optional
from loguru import logger
from fastapi.responses import StreamingResponse
from fastapi.sse import EventSourceResponse

router=APIRouter(dependencies=[Depends(get_current_user)])

class CreateChartRequest(BaseModel):
    """创建图表请求模型"""
    knowledge_base_ids: Optional[List[str]] = Field(
        None, 
        description="知识库ID列表（UUID字符串格式）"
    )
class DeleteChartRequest(BaseModel):
    """删除图表请求模型"""
    session_id: str = Field(..., description="会话ID")

class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=2000,
        description="用户消息内容",
        examples=["请帮我分析一下最新的销售数据趋势"]
    )
    session_id: Optional[str] = Field(
        default=None,
        description="会话ID，如果不提供将创建新会话",
        examples=["session_123"]
    )
    knowledge_base_ids: Optional[List[str]] = Field(
        default=[],
        description="指定的知识库ID列表，用于检索相关信息",
        examples=[["kb_001", "kb_002"]]
    )
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
        

#聊天接口
@router.post("/chat")
async def chat(request: ChatRequest):
    """聊天接口（SSE 流式响应）"""
    session_id = request.session_id
    if not session_id:
        session_id = str(uuid.uuid4())
        await session_manager.create_session(session_id, request.knowledge_base_ids)

    chat_instance = ChatInstance(session_id=session_id)
    # await session_manager.save_chat_message(session_id, "user", request.message)

    async def event_stream():
        final_response = ""
        import json as _json
        try:
            async for chunk in chat_instance.stream_query(
                query=request.message,
                knowledge_base_ids=request.knowledge_base_ids,
            ):
                yield chunk
                try:
                    if chunk.startswith("data: "):
                        data = _json.loads(chunk[6:])
                        if data.get("done") and data.get("response"):
                            final_response = data["response"]
                except Exception:
                    pass
        except Exception as e:
            logger.exception(f"流式聊天失败: {e}")
            yield f"data: {_json.dumps({'error': str(e), 'done': True})}\n\n"

        if final_response and final_response != "Empty Response":
            try:
                await session_manager.save_chat_message(
                    session_id, "assistant", final_response
                )
            except Exception as e:
                logger.exception(f"保存AI回复失败: {e}")

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )

#查询历史对话接口
@router.post("/history")
async def get_history(request: DeleteChartRequest):
    """查询历史对话"""
    try:
        session_id = request.session_id
        if not session_id:
            raise HTTPException(status_code=400, detail="会话ID不能为空")
        
        history = await session_manager.get_session_history(session_id)

        return ApiResponse(
            message="历史对话获取成功",
            code=200,
            success=True,
            timestamp=datetime.datetime.now(),
            data=history
        )
    except Exception as e:
        logger.exception(f"查询历史对话失败: {e}")
        raise HTTPException(status_code=500, detail="查询历史对话失败")
