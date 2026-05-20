import os
from llama_index.core import Document
# from ai_platform.config.setting import settings
from ai_platform.config.resource import get_minio_service
from pathlib import Path
import tempfile
from loguru import logger
from ai_platform.pipeline.loader import DataLoader
from ai_platform.pipeline.transformer import CleanTextTransformComponent


class FileDataPipeline:
    """文件数据管道"""
    def __init__(self, file_path: list[str]):
        self.file_path = file_path
        self.bucket_name ='remember'
        self.minio_service = get_minio_service()
    
    async def process_minio_file(self):
        """处理MinIO文件"""
        # 下载所有文件，返回文件路径列表
        file_paths = []
        for object_name in self.file_path:
            file_path = await self._download_from_minio(object_name)
            file_paths.append(file_path)

        #处理文件
        documents=DataLoader.load_file_dir(file_paths)

        #转换器
        



    async def _download_from_minio(self, object_name: str) -> str:
        """从MinIO下载文件到临时目录，返回完整文件路径"""
        try:
            temp_dir = tempfile.mkdtemp(prefix="minio_pipeline_")
            file_data = await self.minio_service.read_file(self.bucket_name, object_name)
            if not file_data:
                raise ValueError(f"无法从MinIO读取文件: {object_name}")

            file_name = Path(object_name).name
            temp_file_path = Path(temp_dir) / file_name

            with open(temp_file_path, 'wb') as f:
                f.write(file_data)

            logger.info(f"文件下载到: {temp_file_path}")
            return str(temp_file_path)  # 返回完整文件路径

        except Exception as e:
            logger.exception(f"从MinIO下载文件失败: {e}")
            raise


