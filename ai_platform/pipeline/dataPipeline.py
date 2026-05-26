import os
from llama_index.core import Document
from typing import List, Optional
from ai_platform.config.setting import KnowledgeBaseSettings
from ai_platform.services.minio_service import minio_service
from pathlib import Path
import tempfile
from loguru import logger
from ai_platform.pipeline.loader import DataLoader
from ai_platform.pipeline.transformer import TransformerComponent
from ai_platform.config.resource import get_vector_index

class FileDataPipeline:
    """文件数据管道"""
    def __init__(self, file_path: List[str], settings: Optional[KnowledgeBaseSettings] = None, knowledge_base_id: str = None):
        self.bucket_name = 'remember'
        self.file_path = file_path
        self.settings = settings or KnowledgeBaseSettings()
        self.knowledge_base_id = knowledge_base_id
    
    async def process_minio_file(self):
        """处理MinIO文件"""
        file_paths = []
        node_data=[]
        for object_name in self.file_path:
            file_path = await self._download_from_minio(object_name)
            file_paths.append(file_path)
        
        documents = DataLoader.load_file_dir(file_paths)
        logger.info(f"开始处理 {file_paths} 个文件")

        transformer_component = TransformerComponent(self.settings)
        pipeline = transformer_component.create_pipeline(documents)
        nodes = pipeline.run()

        logger.info(f"转换完成，共 {len(nodes)} 个节点")
        for node in nodes:
            if node.text and len(node.text.strip()) > 10:
                node.metadata['knowledge_base_id'] = self.knowledge_base_id
                node_data.append(node)


        await self._store_to_vector_db(node_data, self.settings.index_type)
        
        return node_data

    async def _download_from_minio(self, object_name: str) -> str:

        """从MinIO下载文件到临时目录，返回完整文件路径"""
        try:
            temp_dir = tempfile.mkdtemp(prefix="minio_pipeline_")
            file_data = await minio_service.read_file(self.bucket_name, object_name)
            if not file_data:
                raise ValueError(f"无法从MinIO读取文件: {object_name}")
                
            file_name = Path(object_name).name
            temp_file_path = Path(temp_dir) / file_name

            with open(temp_file_path, 'wb') as f:
                f.write(file_data)

            logger.info(f"文件下载到: {temp_file_path}")
            return str(temp_file_path)

        except Exception as e:
            logger.exception(f"从MinIO下载文件失败: {e}")
            raise

    async def _store_to_vector_db(self, nodes: List[Document], index_type: str):
        """异步插入节点到向量数据库"""
        try:
            if not nodes:
                logger.info("节点列表为空，无需插入")
                return
            logger.info(f"开始插入 {len(nodes)} 个节点到向量数据库")
            if index_type == 'vector':
                await get_vector_index().ainsert_nodes(nodes)
                logger.info(f"成功插入 {len(nodes)} 个节点到向量数据库")
            
        except Exception as e:
            logger.exception(f"插入向量数据库失败: {e}")
            raise
