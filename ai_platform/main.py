import sys
from loguru import logger
import uvicorn
from contextlib import asynccontextmanager
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, HTTPException
from ai_platform.api.auth import router as auth_router
from ai_platform.api.knowledge import router as knowledge_router
from ai_platform.api.upload import router as upload_router
from ai_platform.config.setting import settings
from ai_platform.config.swagger_config import setup_swagger, SWAGGER_CONFIG
from fastapi.middleware.cors import CORSMiddleware
from ai_platform.models.user import user_manager
from ai_platform.services.konwledge_service import knowledge_service
from ai_platform.config.resource import init_resource
# 配置日志
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.log_level
)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("应用启动中...")
    # 初始化数据库表
    init_resource()
    await user_manager.init_tables()  # ← 添加 await
    await knowledge_service.init_knowledge_tables()  # ← 添加 await

    logger.info("应用启动完成")
    yield  # ← 必须有 yield

    # 关闭时的清理工作（可选）
    logger.info("应用关闭中...")

# 创建应用
app = FastAPI(
    title=SWAGGER_CONFIG["title"],
    version=SWAGGER_CONFIG["version"],
    lifespan=lifespan,  # ← 传入 lifespan
    description=SWAGGER_CONFIG["description"],
    openapi_url=SWAGGER_CONFIG["openapi_url"],
    docs_url=SWAGGER_CONFIG["docs_url"],
    redoc_url=SWAGGER_CONFIG["redoc_url"],
    openapi_tags=SWAGGER_CONFIG["openapi_tags"],
    swagger_ui_parameters=SWAGGER_CONFIG["swagger_ui_parameters"],
)

setup_swagger(app)

# 注册路由
app.include_router(auth_router, prefix="/users")
app.include_router(knowledge_router, prefix="/knowledge")
app.include_router(upload_router, prefix="/files")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
async def root():
    return {"message": "Hello World"}


def main():
    uvicorn.run(
        "ai_platform.main:app",
        port=8000,
        host="0.0.0.0",
        # reload=settings.debug,
        # log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    main()