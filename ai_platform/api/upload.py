
from typing import List, Optional, Any
from click.core import F
from fastapi import APIRouter, File, UploadFile, HTTPException, Response, Form, Depends,UploadFile
from ai_platform.services.minio_service import MinioService
from ai_platform.types.common import ApiResponse
import datetime
from ai_platform.services.konwledge_service import knowledge_service
from ai_platform.services.minio_service import minio_service 
from ai_platform.config.setting import settings
from uuid import  UUID
from loguru import logger
from ai_platform.services.konwledge_service import KnowledgeBaseFileCreate

router=APIRouter()

from pydantic import BaseModel, Field
class PreviewRequest(BaseModel):
    object_name: str

class UploadRequest(BaseModel):
    file: Any = Field(..., description="文件")
    knowledge_base_id: UUID = Field(..., description="知识库ID")

@router.post("/upload", response_model=ApiResponse[Any])
async def upload_file(
    files: List[UploadFile] = File(...),
    knowledge_base_id: str = Form(...)
):
    """文件上传接口 - 接受 form-data，支持多文件上传"""
    try:
        kb_id = UUID(knowledge_base_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="知识库ID格式不正确")

    await knowledge_service.get_knowledge_base_detail(kb_id)

    uploaded_files = []
    failed_files = []

    for file in files:
        try:
            logger.info(f"开始接收文件: {file.filename}, 大小: {file.size}")

            if not file.filename:
                failed_files.append({"filename": "unknown", "error": "文件名不能为空"})
                continue

            file_data = await file.read()

            upload_info = await minio_service.upload_file(
                kb_id,
                settings.minio_bucket,
                file_data=file_data,
                original_filename=file.filename,
                content_type=file.content_type or "application/octet-stream",
            )
            if not upload_info:
                failed_files.append({"filename": file.filename, "error": "上传到MinIO失败"})
                continue

            await knowledge_service.create_file_record(KnowledgeBaseFileCreate(
                knowledge_base_id=kb_id,
                filename=upload_info.get("original_filename", file.filename),
                file_path=upload_info.get("object_name", ""),
                original_filename=upload_info.get("original_filename", file.filename),
                file_size=upload_info.get("size", len(file_data)),
                file_type=upload_info.get("content_type", file.content_type),
                mime_type=upload_info.get("content_type", file.content_type),
            ))

            uploaded_files.append(file.filename)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"文件 {file.filename} 上传失败: {str(e)}")
            failed_files.append({"filename": file.filename, "error": str(e)})

    if not uploaded_files and failed_files:
        raise HTTPException(status_code=500, detail={
            "message": "所有文件上传失败",
            "failed_files": failed_files,
        })

    return ApiResponse(
        success=True,
        message=f"成功上传 {len(uploaded_files)} 个文件"
        + (f"，{len(failed_files)} 个失败" if failed_files else ""),
        code=200,
        timestamp=datetime.datetime.now(),
        data={
            "uploaded": uploaded_files,
            "failed": failed_files,
            "knowledge_base_id": str(kb_id),
        }
    )

@router.get("/filelist", response_model=ApiResponse[Any])
async def get_file_list():
    """所有文件列表"""
    files = await minio_service.list_files(settings.minio_bucket)
    return ApiResponse(
        success=True,
        code=200,
        timestamp=datetime.datetime.now(),
        message="获取文件列表成功" if files else "暂无文件",
        data={
            "files": files or [],
            "total": len(files) if files else 0,
        }
    )


#文件预览
@router.post("/filepreview", response_model=ApiResponse[Any])
async def preview_file(
    request: PreviewRequest
):
    """文件预览"""
    file_url = await minio_service.preview_file(
        bucket_name=settings.minio_bucket,
        object_name=request.object_name,
    )
    if not file_url:
        raise HTTPException(status_code=404, detail="文件不存在")
    return ApiResponse(
        success=True,
        message=f"文件预览成功: {request.object_name}", 
        code=200,
        timestamp=datetime.datetime.now(),
        data={
            "preview_url": file_url,
        }
    )

#文件删除
@router.post("/filedelete", response_model=ApiResponse[Any])
async def delete_file(
    request: PreviewRequest
):
    """文件删除"""
    success = await minio_service.delete_file(
        bucket_name=settings.minio_bucket,
        object_name=request.object_name,
    )
    if not success:
        raise HTTPException(status_code=400, detail={
            "message": "文件删除失败",
            "code": 400,
        })
    #删除数据库记录
    await knowledge_service.delete_file_record(request.object_name)
    
    return ApiResponse(
        success=True,
        message=f"文件删除成功: {request.object_name}", 
        code=200,
        timestamp=datetime.datetime.now(),
    )





