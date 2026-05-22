import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple

from loguru import logger
from sqlalchemy import select, func, and_,delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from ..models import KnowledgeBase, KnowledgeBaseFile, Base
from ai_platform.config.resource import create_engine
from pydantic import BaseModel, Field
from uuid import UUID
from fastapi import HTTPException
from ai_platform.pipeline.dataPipeline import FileDataPipeline
from ai_platform.config.setting import KnowledgeBaseSettings
from ai_platform.config.resource import get_vector_store
from llama_index.core.vector_stores.types import MetadataFilters, MetadataFilter, FilterOperator
class KnowledgeBaseFileCreate(BaseModel):
    """知识库文件创建模型"""
    knowledge_base_id: UUID = Field(description="知识库ID")
    file_path: str = Field(description="文件路径")
    original_filename: str = Field(description="原始文件名")
    file_size: int = Field(description="文件大小")
    file_type: str = Field(description="文件类型")
    mime_type: str = Field(description="文件MIME类型")
    filename: str = Field(description="文件名")


class KnowledgeService:
    """知识库服务"""
    def __init__(self):
        self.engine = None
        self.session = None
        self.knowledge_base_service = None

    async def _get_engine(self):
            """获取数据库引擎 创建适量123"""
            if self.engine is None:
                self.engine = create_engine()
            return self.engine

    async def init_knowledge_tables(self):
        """初始化数据库表"""
        try:
            engine = await self._get_engine()
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            # 创建默认知识库
            # await self.create_default_knowledge_base() 
            logger.info("知识库表初始化完成")
        except Exception as e:
            logger.exception(f"知识库表初始化失败: {e}")
            raise

    #创建知识库
    async def create_knowledge_base(self, name: str, description: str = None,initial_settings: Dict[str, Any] = None):
        """创建知识库"""
        try:
            await self._get_engine()
            async with AsyncSession(self.engine) as session:
                new_knowledge_base = KnowledgeBase(
                    id=uuid.uuid4(),
                    name=name,
                    description=description,
                    create_time=datetime.now(),
                    update_time=datetime.now(),
                    status="building",
                    settings=initial_settings or {}
                )
                
                session.add(new_knowledge_base)
                await session.commit()
                session.refresh(new_knowledge_base)
                return new_knowledge_base
        except Exception as e:
            logger.exception(f"创建知识库失败: {e}")
            raise        
    
    # 获取知识库列表
    async def get_knowledge_base_list(self):
        """获取知识库列表"""
        try:
                await self._get_engine()
                async with AsyncSession(self.engine) as session:
                    query = select(KnowledgeBase).order_by(KnowledgeBase.create_time.desc())
                    knowledge_base_list = await session.execute(query)
                    return knowledge_base_list.scalars().all()
        except Exception as e:
            logger.exception(f"获取知识库列表失败: {e}")
            raise

    #删除知识库
    async def delete_knowledge_base(self, knowledge_base_id: UUID):
        """删除知识库"""
        try:
            await self._get_engine()
            async with AsyncSession(self.engine) as session:

                await session.execute(delete(KnowledgeBase).where(KnowledgeBase.id == knowledge_base_id))
                await session.commit()
                return True
        except Exception as e:
            logger.exception(f"删除知识库失败: {e}")
            raise
    
    #修改知识库
    async def update_knowledge_base(self, knowledge_base_id: UUID, name: str = None, description: str = None):
        """修改知识库"""
        try:
            await self._get_engine()
            async with AsyncSession(self.engine) as session:
                knowledge_base = await session.get(KnowledgeBase, knowledge_base_id)
                if knowledge_base is None:
                    raise ValueError(f"知识库 {knowledge_base_id} 不存在")
                if name:
                    knowledge_base.name = name
                if description:
                    knowledge_base.description = description
                await session.commit()
                return knowledge_base
        except Exception as e:
            logger.exception(f"修改知识库失败: {e}")
            raise

    #修改知识库设置
    async def update_knowledge_base_settings(self, knowledge_base_id: UUID, settings: Dict[str, Any] = None):
        """修改知识库设置"""
        try:
            await self._get_engine()    
            async with AsyncSession(self.engine) as session:
                knowledge_base = await session.get(KnowledgeBase, knowledge_base_id)
                if knowledge_base is None:
                    raise ValueError(f"知识库 {knowledge_base_id} 不存在")
                if settings:
                    knowledge_base.settings = settings
                else:
                    knowledge_base.settings = {}
                knowledge_base.status = "building"
                knowledge_base.update_time = datetime.now()
                await session.commit()
                return knowledge_base
        except Exception as e:
            logger.exception(f"修改知识库设置失败: {e}")
            raise
    
    #获取知识库详情
    async def get_knowledge_base_detail(self, knowledge_base_id: UUID):
        """获取知识库详情"""
        try:
            await self._get_engine()
            async with AsyncSession(self.engine) as session:
                knowledge_base = await session.get(KnowledgeBase, knowledge_base_id)
                if knowledge_base is None:
                    raise HTTPException(status_code=400, detail={
                        "message": "知识库不存在",
                        "code": 400
                    })
                return knowledge_base
        except Exception as e:
            logger.exception(f"获取知识库详情失败: {e}")
            raise

    async def build_knowledge_base(self, knowledge_base_id: UUID):
        """构建知识库"""
        try:
            await self._get_engine()
            async with AsyncSession(self.engine) as session:
                # 1. 获取知识库基本信息
                knowledge_base = await session.get(KnowledgeBase, knowledge_base_id)
                if knowledge_base is None:
                    raise ValueError(f"知识库 {knowledge_base_id} 不存在")
                
                # 2. 获取知识库设置
                kb_settings = KnowledgeBaseSettings(**(knowledge_base.settings or {}))

                # 3. 获取知识库所有文件的路径
                query = select(KnowledgeBaseFile.file_path).where(
                    KnowledgeBaseFile.knowledge_base_id == knowledge_base_id
                )
                file_records = await session.execute(query)
                file_paths = file_records.scalars().all()
                
                # # 3. 记录日志便于调试
                # logger.info(f"知识库 {knowledge_base_id} 关联了 {len(file_paths)} 个文件: {file_paths}")
                
                # 4. TODO: 在这里调用文件处理逻辑
                # 例如：解析文件、分块、生成向量、存入向量数据库等
                # await self._process_files(file_paths, knowledge_base_id)
                file_pipeline = FileDataPipeline(file_paths, kb_settings,knowledge_base_id)
                await file_pipeline.process_minio_file()
                # # 5. 更新状态（无论是否有文件，都标记为 active？根据业务决定）
                stmt = update(KnowledgeBaseFile).where(
                    KnowledgeBaseFile.knowledge_base_id == knowledge_base_id
                ).values(status="active")
                await session.execute(stmt)
                
                knowledge_base.status = "active"
                knowledge_base.update_time = datetime.now()
                await session.commit()
                await session.refresh(knowledge_base)

                return {
                    "knowledge_base_id": str(knowledge_base_id),
                    "status": "active",
                    "file_paths": file_paths,
                    "file_count": len(file_paths)  # 增加文件数量字段
                }
                
        except Exception as e:
            logger.exception(f"构建知识库失败: {e}")
    #读取知识库内容
    async def read_knowledge_base(self, knowledge_base_id: UUID, page: int = 1, page_size: int = 20):
        """读取知识库内容 — 从 data_vector_store 表中按 knowledge_base_id 过滤并分页"""
        try:
            vector_store = get_vector_store()
            filters = MetadataFilters(
                filters=[
                    MetadataFilter(
                        key="knowledge_base_id",
                        value=str(knowledge_base_id),
                        operator=FilterOperator.EQ,
                    )
                ]
            )
            all_nodes = await vector_store.aget_nodes(filters=filters)
            total = len(all_nodes)

            start = (page - 1) * page_size
            end = start + page_size
            page_nodes = all_nodes[start:end]

            items = []
            for node in page_nodes:
                items.append({
                    "node_id": node.node_id,
                    "text": node.get_content(),
                    "metadata": node.metadata,
                })

            logger.info(f"读取知识库 {knowledge_base_id}: 共 {total} 个节点, 第 {page} 页返回 {len(items)} 条")
            return {
                "items": items,
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": max(1, (total + page_size - 1) // page_size),
            }
        except Exception as e:
            logger.exception(f"读取知识库内容失败: {e}")
            raise

    #文件管理
    async def create_file_record(self, file_create: KnowledgeBaseFileCreate):
        """创建文件记录"""
        try:
            await self._get_engine()
            async with AsyncSession(self.engine) as session:
                new_file_record = KnowledgeBaseFile(
                    id=str(uuid.uuid4()),
                    knowledge_base_id=file_create.knowledge_base_id,
                    original_filename=file_create.original_filename,
                    file_path=file_create.file_path,
                    filename=file_create.filename,
                    file_size=file_create.file_size,
                    file_type=file_create.file_type,
                    mime_type=file_create.mime_type,
                    status="building",
                )
                session.add(new_file_record)

                #更改知识库状态
                knowledge_base = await session.get(KnowledgeBase, file_create.knowledge_base_id)
                if knowledge_base is None:
                    raise ValueError(f"知识库 {file_create.knowledge_base_id} 不存在")
                knowledge_base.status = "building"
                knowledge_base.update_time = datetime.now()

                await session.commit()
                session.refresh(new_file_record)
                return new_file_record
        except Exception as e:
            logger.exception(f"创建文件记录失败: {e}")
            raise

    #删除文件记录
    async def delete_file_record(self, object_name: str):
        """删除文件记录"""
        try:
            await self._get_engine()
            async with AsyncSession(self.engine) as session:
                smt=select(KnowledgeBaseFile).where(KnowledgeBaseFile.file_path == object_name)
                result = await session.execute(smt)
                file_record = result.scalar()
                if file_record is None:
                    raise ValueError(f"文件记录 {object_name} 不存在")
                await session.delete(file_record)
                await session.commit()
                return True
        except Exception as e:
            logger.exception(f"删除文件记录失败: {e}")
            raise


knowledge_service =KnowledgeService()