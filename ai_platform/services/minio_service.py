from minio import Minio
from urllib3 import response
from ai_platform.config.setting import settings
from io import BytesIO
from loguru import logger
from minio.error import S3Error
import uuid
import os
from datetime import datetime
from uuid import UUID
from datetime import timedelta

class MinioService:
    def __init__(self):
        """初始化Minio服务"""
        self.client = Minio(
            endpoint=settings.minio_endpoint,      # MinIO 服务地址（不含 http/https 前缀）
            access_key=settings.minio_access_key,   # 你的 Access Key
            secret_key=settings.minio_secret_key,  # 你的 Secret Key
            secure=settings.minio_secure                   # True 用 HTTPS，False 用 HTTP
        )

    #上传文件
    async def upload_file(self,knowledge_base_id: UUID, bucket_name: str, file_data: bytes, original_filename: str = None,content_type: str = "application/octet-stream"):
        """上传文件到Minio存储桶"""
        try:
                # 生成唯一文件名
            file_id = str(uuid.uuid4())
            file_extension = os.path.splitext(original_filename)[1]
            object_name = f"{datetime.now().strftime('%Y/%m/%d')}/{file_id}{file_extension}"

            file_stream = BytesIO(file_data)
                        
            self.client.put_object(
                bucket_name=bucket_name,
                object_name=object_name,
                data=file_stream,
                length=len(file_data),
                content_type=content_type,
            )
            
            #生成下载的url
            download_url = self.client.presigned_get_object(
                bucket_name=bucket_name,
                object_name=object_name,
                expires=timedelta(minutes=10),  # 10分钟过期
            )

            upload_info = {
                "file_id": file_id,
                "original_filename": original_filename,
                "object_name": object_name,
                "bucket_name": bucket_name,
                "download_url": download_url,
                "file_size": len(file_data),
                "content_type": content_type,
                "knowledge_base_id": knowledge_base_id,
                "upload_time": datetime.now().isoformat(),
            }
            logger.info(f"文件上传成功: {original_filename} -> {object_name}")

            return upload_info
        except S3Error as e:
            logger.exception(f"MinIO S3错误: {e}")
            # ✅ 抛出异常而不是返回 None
            raise Exception(f"MinIO上传失败: {e}")
        except Exception as e:
            logger.exception(f"文件上传失败: {e}")
            # ✅ 抛出异常而不是返回 None
            raise Exception(f"文件上传失败: {e}")


    async def list_files(self, bucket_name: str, prefix: str = "", limit: int = 50):
        """列出存储桶中的文件"""
        try:
            files = []
            objects = self.client.list_objects(
                bucket_name,
                prefix=prefix,
                recursive=True
            )
            
            # 同步迭代生成器
            for i, obj in enumerate(objects):
                if i >= limit:
                    break
                files.append({
                    "size": obj.size,
                    "last_modified": obj.last_modified.isoformat() if obj.last_modified else "",
                    "bucket_name": bucket_name,
                    "object_name": obj.object_name,
                    "etag": obj.etag,
                    "content_type": obj.object_name.split(".")[-1]
                })
            
            return files
        except Exception as e:
            logger.error(f"列出文件失败: {e}")
            return []

    #文件预览
    async def preview_file(self, bucket_name: str, object_name: str):
        """文件预览"""
        try:
            file_url = self.client.presigned_get_object(
                bucket_name=bucket_name,
                object_name=object_name,
                expires=timedelta(minutes=10),  # 10分钟过期
            )
            return file_url
        except Exception as e:
            logger.error(f"文件预览失败: {e}")
            return None

    #删除文件
    async def delete_file(self, bucket_name: str, object_name: str):
        """删除文件"""
        try:
            self.client.remove_object(
                bucket_name=bucket_name,
                object_name=object_name,
            )
            logger.info(f"文件删除成功: {object_name}")
            return True
        except Exception as e:
            logger.error(f"文件删除失败: {e}")
            return False

    async def read_file(self, bucket_name: str, object_name: str) -> Optional[bytes]:
        """
        读取文件内容
        """
        try:
            response = self.client.get_object(
                bucket_name=bucket_name,
                object_name=object_name
            )
            # 读取所有数据
            file_data = response.read()
            response.close()
            response.release_conn()

            logger.info(f"文件读取成功: {object_name}")
            return file_data

        except S3Error as e:
            logger.exception(f"文件读取失败: {e}")
            return None
minio_service = MinioService()
