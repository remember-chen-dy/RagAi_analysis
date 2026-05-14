"""
Swagger 简洁配置
直接复制到项目中使用
"""
from fastapi.openapi.utils import get_openapi

# ============================================
# Swagger 配置参数
# ============================================

SWAGGER_CONFIG = {
    "title": "LlamaIndex 智能数据分析平台",
    "version": "1.0.0",
    "description": """
## 🚀 平台功能

- **智能对话**: 基于知识库的 AI 问答
- **文件管理**: 上传、下载、预览文件
- **知识库管理**: 构建企业知识体系
- **用户认证**: JWT 身份验证

### 快速开始
1. `/auth/register` - 注册账号
2. `/auth/login` - 登录获取 Token
3. 点击右上角 "Authorize" 输入 Token
4. 开始使用其他接口
    """,
    "contact": {
        "name": "技术支持",
        "email": "support@example.com",
    },
    "license_info": {
        "name": "MIT License",
    },
    "openapi_url": "/api/v1/openapi.json",
    "docs_url": "/docs",
    "redoc_url": "/redoc",
    "openapi_tags": [
        {"name": "Authentication", "description": "用户认证"},
        {"name": "chat", "description": "智能对话"},
        {"name": "文件管理", "description": "文件上传下载"},
        {"name": "知识库管理", "description": "知识库操作"},
    ],
    "swagger_ui_parameters": {
        "docExpansion": "none",  # 折叠所有接口
        "filter": True,  # 显示过滤框
        "persistAuthorization": True,  # 记住认证信息
    },
}


def setup_swagger(app):
    """配置 Swagger 文档"""

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
             title=SWAGGER_CONFIG["title"],           # API 标题
             version=SWAGGER_CONFIG["version"],       # 版本号
             description=SWAGGER_CONFIG["description"], # API 描述
             routes=app.routes,                       # 自动扫描所有路由
             contact=SWAGGER_CONFIG.get("contact"),   # 联系人信息
             license_info=SWAGGER_CONFIG.get("license_info"), # 许可证
             tags=SWAGGER_CONFIG["openapi_tags"],     # API 分组标签
        )

        # 添加全局认证
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
        openapi_schema["security"] = [{"BearerAuth": []}]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi