import datetime
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID

from pydantic.types import Json  # ✅ 添加 UUID 导入
from ai_platform.types.common import ApiResponse
from ai_platform.services.konwledge_service import knowledge_service

router = APIRouter()

# 定义请求模型
class CreateKnowledgeBaseRequest(BaseModel):
    name: str = Field(..., description="知识库名称")
    description: Optional[str] = Field(None, description="知识库描述")
    initial_settings: Optional[Dict[str, Any]] = Field(None, description="知识库初始设置")

# 定义响应模型（只定义一次）
class KnowledgeBaseResponse(BaseModel):
    """知识库响应模型"""
    id: UUID = Field(..., description="知识库ID")
    name: str = Field(..., description="知识库名称")
    description: Optional[str] = Field(None, description="知识库描述")
    status: str = Field(..., description="知识库状态")
    settings: Optional[Dict[str, Any]] = Field(None, description="知识库设置")
    create_time: datetime.datetime = Field(..., description="创建时间")
    update_time: Optional[datetime.datetime] = Field(None, description="更新时间")
    
    # ✅ 添加 Pydantic v2 配置（重要！）
    model_config = {
        "from_attributes": True  # 允许从 ORM 对象创建
    }

# 定义请求模型
class UpdateKnowledgeBaseSettingsRequest(BaseModel):
    knowledge_base_id: UUID = Field(..., description="知识库ID")
    settings: Optional[Dict[str, Any]] = Field(None, description="知识库设置")


@router.post("/create", response_model=ApiResponse[Any])
async def create_knowledge_base(request: CreateKnowledgeBaseRequest):
    """创建知识库"""
    knowledge_base = await knowledge_service.create_knowledge_base(
        request.name, 
        request.description, 
        request.initial_settings
    )

    if knowledge_base is None:
        raise HTTPException(
            status_code=400,
            detail="知识库名称已存在，创建失败"
        )

    return ApiResponse(
        success=True,
        code=200,
        message="知识库创建成功",
        data={},
        timestamp=datetime.datetime.now()
    )

# 获取知识库列表
@router.get("/list", response_model=ApiResponse[List[KnowledgeBaseResponse]])
async def get_knowledge_base_list():
    """获取知识库列表"""
    try:
        knowledge_bases = await knowledge_service.get_knowledge_base_list()
        
        return ApiResponse(
            success=True,
            code=200,
            message="获取知识库列表成功",
            data=knowledge_bases,  # ORM 对象会被自动转换
            timestamp=datetime.datetime.now()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取知识库列表失败: {str(e)}"
        )

# 删除知识库
@router.delete("/delete/{knowledge_base_id}", response_model=ApiResponse[Any])
async def delete_knowledge_base(knowledge_base_id: UUID):
    """删除知识库"""
    try:
        await knowledge_service.delete_knowledge_base(knowledge_base_id)
        return ApiResponse(
            success=True,
            code=200,
            message="知识库删除成功",
            data={},
            timestamp=datetime.datetime.now()
        )
    except ValueError as e:
        return ApiResponse(
            success=False,
            code=400,
            message=str(e),
            data={},
            timestamp=datetime.datetime.now()
        )

# 修改知识库
@router.put("/update/{knowledge_base_id}", response_model=ApiResponse[Any])
async def update_knowledge_base(knowledge_base_id: UUID, request: CreateKnowledgeBaseRequest):
    """修改知识库"""
    await knowledge_service.update_knowledge_base(
        knowledge_base_id,
        name=request.name,
        description=request.description,
    )
    return ApiResponse(
        success=True,
        code=200,
        message="知识库修改成功",
        data={},
        timestamp=datetime.datetime.now()
    )
        

# 修改知识库设置
@router.post("/update_settings", response_model=ApiResponse[Any])
async def update_knowledge_base_settings(request: UpdateKnowledgeBaseSettingsRequest):
    """修改知识库设置"""
    result= await knowledge_service.update_knowledge_base_settings(
        request.knowledge_base_id,
        settings=request.settings
    )
    if result is None:
        raise HTTPException(
            status_code=400,
            detail="知识库设置修改失败"
        )
    return ApiResponse(
        success=True,
        code=200,
        message="知识库设置修改成功",
        data={},
        timestamp=datetime.datetime.now()
    )


@router.post("/build/{knowledge_base_id}", response_model=ApiResponse[Any])
async def build_knowledge_base(knowledge_base_id: UUID):
    """构建知识库（后台非阻塞）"""
    try:
        result = await knowledge_service.build_knowledge_base(knowledge_base_id)
        
        return ApiResponse(
            success=True,
            code=200,
            message="知识库构建已启动",
            data=result,
            timestamp=datetime.datetime.now()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"知识库构建失败: {str(e)}")

#读取知识库内容
@router.get("/read/{knowledge_base_id}", response_model=ApiResponse[Any])
async def read_knowledge_base(
    knowledge_base_id: UUID,
    page: int = Query(default=1, ge=1, description="页码，从 1 开始"),
    page_size: int = Query(default=20, ge=1, le=100, description="每页条数，最大 100"),
):
    """读取知识库 — 分页获取 data_vector_store 中的文件片段"""
    try:
        result = await knowledge_service.read_knowledge_base(knowledge_base_id, page, page_size)
        
        return ApiResponse(
            success=True,
            code=200,
            message=f"知识库读取成功，共 {result['total']} 条",
            data=result,
            timestamp=datetime.datetime.now()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"知识库读取失败: {str(e)}")
