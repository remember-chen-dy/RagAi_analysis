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
    

    #获取数据库配置
    @property
    def async_postgres_url(self) -> str:
        """异步PostgreSQL连接字符串"""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


settings = Setting()


