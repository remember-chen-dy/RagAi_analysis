from typing import Optional
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings as PydanticBaseSettings
load_dotenv()

class Setting(PydanticBaseSettings):
    #系统配置
    log_level: str = Field(default="INFO", description="日志级别")


    # 数据库配置
    postgres_host: str = Field(default="localhost", description="PostgreSQL主机")
    postgres_port: int = Field(default=5432, description="PostgreSQL端口")
    postgres_db: str = Field(default="knowledge_base", description="PostgreSQL数据库名")
    postgres_user: str = Field(default="remember", description="PostgreSQL用户名")
    postgres_password: str = Field(default="ServBay.dev", description="PostgreSQL密码")

    #知识库默认配置
    #Minio配置
    minio_endpoint: str = Field(default="192.168.1.5:9000", description="Minio端点")
    minio_access_key: str = Field(default="minioadmin", description="Minio访问密钥")
    minio_secret_key: str = Field(default="minioadmin", description="Minio秘密密钥")
    minio_secure: bool = Field(default=False, description="Minio是否使用HTTPS")
    minio_bucket: str = Field(default="remember", description="Minio存储桶")
    
    #获取数据库配置
    @property
    def async_postgres_url(self) -> str:
        """异步PostgreSQL连接字符串"""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = Setting()


