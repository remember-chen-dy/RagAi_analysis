from typing import Optional, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings as PydanticBaseSettings
load_dotenv()

class Setting(PydanticBaseSettings):
    #系统配置
    log_level: str = Field(default="INFO", description="日志级别")

    # JWT 配置
    jwt_secret_key: str = Field(default="rag-ai-platform-jwt-secret-key-2026", description="JWT签名密钥")
    jwt_algorithm: str = Field(default="HS256", description="JWT加密算法")
    jwt_access_token_expire_minutes: int = Field(default=1440, description="Access Token过期时间(分钟)")

    # 数据库配置
    postgres_host: str = Field(default="localhost", description="PostgreSQL主机")
    postgres_port: int = Field(default=5432, description="PostgreSQL端口")
    postgres_db: str = Field(default="knowledge_base", description="PostgreSQL数据库名")
    postgres_user: str = Field(default="remember", description="PostgreSQL用户名")
    postgres_password: str = Field(default="ServBay.dev", description="PostgreSQL密码")

    #知识库默认配置
    #Minio配置
    minio_endpoint: str = Field(default="localhost:9000", description="Minio端点")
    minio_access_key: str = Field(default="minioadmin", description="Minio访问密钥")
    minio_secret_key: str = Field(default="minioadmin", description="Minio秘密密钥")
    minio_secure: bool = Field(default=False, description="Minio是否使用HTTPS")
    minio_bucket: str = Field(default="remember", description="Minio存储桶")
    
    #获取数据库配置
    @property
    def async_postgres_url(self) -> str:
        """异步PostgreSQL连接字符串"""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


class KnowledgeBaseSettings(BaseModel):
    """知识库构建设置"""
    chunk_size: int = Field(default=1000, ge=100, le=4000, description="分块大小")
    chunk_overlap: int = Field(default=200, ge=0, le=500, description="分块重叠大小")
    text_split_strategy: str = Field(default="fixed_chars", description="文本分割策略: fixed_chars, semantic")
    split_chars: List[str] = Field(default=["\n\n", "\n", "。", "！", "？", "；"], description="分割字符列表")
    index_type: str = Field(default="vector", description="索引类型: vector, knowledge_graph, long_document")


settings = Setting()


