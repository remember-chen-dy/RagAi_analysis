# LlamaIndex 智能数据分析平台

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14+-blue.svg" alt="Python 3.14+">
  <img src="https://img.shields.io/badge/FastAPI-0.115+-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Vue.js-3.5+-4FC08D.svg" alt="Vue 3">
  <img src="https://img.shields.io/badge/LlamaIndex-0.12+-orange.svg" alt="LlamaIndex">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
</p>

<p align="center">
  基于 <strong>RAG（检索增强生成）</strong> 技术的企业级知识库管理与 AI 对话分析平台
</p>

---

## 目录

- [项目简介](#项目简介)
- [核心特性](#核心特性)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
- [项目结构](#项目结构)
- [功能详解](#功能详解)
- [API 文档](#api-文档)
- [环境配置](#环境配置)
- [开发指南](#开发指南)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## 项目简介

本项目是一个企业级 **RAG（Retrieval-Augmented Generation）** 智能数据分析平台，基于 **FastAPI + Vue 3 + LlamaIndex** 构建。平台支持多格式文档解析、向量知识库构建、混合检索（BM25 + 向量）、流式 AI 对话、以及完整的用户认证体系。

通过集成 **DashScope（阿里云通义千问）** 大语言模型和 **PGVector** 向量数据库，平台能够对企业文档进行深度理解和智能问答，同时支持基于检索结果的精准回答与直接生成回答的灵活切换。

### 适用场景

- 企业知识库构建与智能检索
- 文档问答与内容分析
- 多格式文件（PDF/DOCX/PPT/XLS/图片）智能解析
- 基于私有数据的 AI 助手

---

## 核心特性

### 智能文档解析
- **多格式支持**：PDF、DOCX、PPT、XLS、PNG、JPG、Markdown 等
- **图片 OCR**：基于多模态大模型的图片文字识别

### 知识库管理
- **向量存储**：基于 PostgreSQL + PGVector 的向量数据库
- **混合检索**：BM25 关键词检索 + 向量语义检索的融合方案
- **灵活配置**：分块大小、重叠度、分割策略、索引类型（向量/混合）可调
- **异步构建**：后台任务构建知识库，不阻塞前端操作

### AI 智能对话
- **流式输出**：基于 SSE（Server-Sent Events）的实时流式响应
- **上下文记忆**：多轮对话支持，自动关联历史会话
- **Empty Response 处理**：检索无结果时自动调用大模型直接生成，并明确标注
- **知识库绑定**：可选择特定知识库进行针对性问答

### 用户认证
- **JWT Token**：基于 PyJWT 的无状态认证机制
- **路由守卫**：前端基于 Token 的访问控制
- **自动过期处理**：401 响应自动跳转登录页

### 文件管理
- **MinIO 对象存储**：高可用的文件存储方案
- **上传下载**：支持大文件上传、预览链接生成
- **文件预览**：文本、图片、PDF 在线预览

---

## 技术架构

### 后端技术栈

| 组件 | 技术 | 用途 |
|------|------|------|
| Web 框架 | FastAPI | 高性能异步 API 服务 |
| RAG 框架 | LlamaIndex | 文档索引、检索、对话引擎 |
| LLM | DashScope (通义千问) | 大语言模型推理 |
| Embedding | DashScope Embedding | 文本向量嵌入 |
| 向量数据库 | PostgreSQL + PGVector | 向量存储与检索 |
| 对象存储 | MinIO | 文件存储 |
| ORM | SQLAlchemy 2.0 | 数据库操作 |
| 认证 | PyJWT | JWT Token 签发与验证 |
| 日志 | Loguru | 结构化日志输出 |

### 前端技术栈

| 组件 | 技术 | 用途 |
|------|------|------|
| 框架 | Vue 3 + Composition API | 响应式 UI 框架 |
| 路由 | Vue Router 4 | 单页应用路由 |
| UI 组件 | Ant Design Vue 4 | 企业级 UI 组件库 |
| 聊天组件 | ant-design-x-vue | AI 对话界面组件 |
| 样式 | Tailwind CSS 4 | 原子化 CSS 框架 |
| 构建 | Vite 6 | 快速构建工具 |
| 类型 | TypeScript 5.8 | 类型安全 |

### 架构图

```
┌─────────────────────────────────────────────────────────────┐
│                        前端 (Vue 3)                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ 登录/注册 │  │ 文件管理  │  │ 知识库   │  │ AI 对话  │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP / SSE
┌────────────────────────▼────────────────────────────────────┐
│                      后端 (FastAPI)                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ 认证服务  │  │ 文件服务  │  │ 知识库   │  │ 对话引擎  │    │
│  │ (JWT)    │  │ (MinIO)  │  │ 服务     │  │ (RAG)    │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              数据处理流水线 (Pipeline)                 │   │
│  │  文档加载 → 页眉页脚过滤 → 文本分割 → 向量嵌入 → 存储  │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
   ┌──────────┐   ┌──────────┐   ┌──────────┐
   │PostgreSQL│   │  MinIO   │   │DashScope │
   │+ PGVector│   │对象存储  │   │  大模型   │
   └──────────┘   └──────────┘   └──────────┘
```

---

## 快速开始

### 环境要求

- Python >= 3.14
- Node.js >= 18
- PostgreSQL >= 15（需启用 pgvector 扩展）
- MinIO Server
- DashScope API Key（阿里云百炼平台）

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/rag-ai-platform.git
cd rag-ai-platform
```

### 2. 配置环境变量

在项目根目录创建 `.env` 文件：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的配置：

```env
# ============================================
# 数据库配置
# ============================================
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=knowledge_base
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password

# ============================================
# MinIO 对象存储配置
# ============================================
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_SECURE=false

# ============================================
# JWT 认证配置
# ============================================
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=1440

# ============================================
# LLM API 配置（必填）
# ============================================
# 阿里云 DashScope（百炼）API Key
# 获取地址：https://help.aliyun.com/zh/dashscope/
DASHSCOPE_APIKEY=sk-your-dashscope-api-key-here

# ============================================
# 日志级别
# ============================================
LOG_LEVEL=INFO
```

### 3. 后端配置

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -e .

# 启动服务
python -m ai_platform.main
```

后端服务默认运行在 `http://localhost:8000`

### 4. 前端配置

```bash
cd frontend

# 安装依赖
npm install

# 配置 API 地址
# 修改 frontend/.env 文件：
# VITE_API_BASE_URL=http://localhost:8000

# 启动开发服务器
npm run dev
```

前端服务默认运行在 `http://localhost:5173`

### 5. 访问应用

- 前端页面：`http://localhost:5173`
- API 文档：`http://localhost:8000/docs`
- ReDoc 文档：`http://localhost:8000/redoc`

---

## 项目结构

```
rag-ai-platform/
├── ai_platform/                    # 后端主目录
│   ├── api/                        # API 路由层
│   │   ├── auth.py                 # 用户认证（登录/注册/Token）
│   │   ├── chart.py                # 聊天/对话接口（SSE 流式）
│   │   ├── knowledge.py            # 知识库管理接口
│   │   └── upload.py               # 文件上传/管理接口
│   ├── config/                     # 配置模块
│   │   ├── auth.py                 # JWT 工具函数
│   │   ├── resource.py             # 资源初始化（LLM/Embedding/向量库）
│   │   ├── setting.py              # 系统配置（数据库/MinIO/JWT）
│   │   └── swagger_config.py       # Swagger 文档配置
│   ├── models/                     # 数据模型（SQLAlchemy）
│   │   ├── user.py                 # 用户/会话模型
│   │   └── session.py              # 聊天记录模型
│   ├── pipeline/                   # 数据处理流水线
│   │   ├── dataPipeline.py         # 主流水线（下载→解析→分割→存储）
│   │   ├── data_filter.py          # 页眉页脚过滤器
│   │   ├── loader.py               # 文档加载器（多格式）
│   │   └── transformer.py          # 文本分割/转换组件
│   ├── query_engine/               # RAG 查询引擎
│   │   ├── rag_engine.py           # 混合检索 + 流式对话引擎
│   │   └── chat_instance.py        # 聊天实例管理
│   ├── services/                   # 业务服务层
│   │   ├── konwledge_service.py    # 知识库业务逻辑
│   │   └── minio_service.py        # MinIO 文件服务
│   ├── types/                      # 类型定义
│   ├── evaluation.py               # RAG 评估模块
│   └── main.py                     # FastAPI 应用入口
├── frontend/                       # 前端主目录
│   ├── src/
│   │   ├── api/                    # API 请求封装
│   │   │   ├── auth.ts             # 认证相关请求
│   │   │   ├── chat.ts             # 聊天/SSE 请求
│   │   │   ├── knowledge.ts        # 知识库请求
│   │   │   ├── upload.ts           # 文件上传请求
│   │   │   └── request.ts          # 通用请求工具
│   │   ├── components/             # 公共组件
│   │   │   ├── FileUpload.vue      # 文件上传组件
│   │   │   ├── Layout.vue          # 页面布局/导航栏
│   │   │   └── MarkdownRenderer.vue # Markdown 渲染
│   │   ├── router/                 # 路由配置
│   │   │   └── index.ts            # 路由定义 + 守卫
│   │   ├── views/                  # 页面视图
│   │   │   ├── Login.vue           # 登录页
│   │   │   ├── Register.vue        # 注册页
│   │   │   ├── FileManager.vue     # 文件管理页
│   │   │   ├── KnowledgeBase.vue   # 知识库管理页
│   │   │   ├── ChatBot.vue         # AI 对话页
│   │   │   └── Evaluation.vue      # 评估页
│   │   ├── App.vue                 # 根组件
│   │   └── main.ts                 # 入口文件
│   ├── package.json
│   └── vite.config.ts
├── pyproject.toml                  # Python 依赖配置
└── README.md                       # 本文件
```

---

## 功能详解

### 1. 用户认证

平台采用 **JWT（JSON Web Token）** 认证机制：

- 用户登录后，后端签发 JWT Token（默认有效期 24 小时）
- 前端将 Token 存储在 `localStorage`，每次请求自动携带 `Authorization: Bearer <token>`
- 后端通过 `HTTPBearer` 依赖注入验证 Token 有效性
- Token 过期或无效时，前端自动清除并跳转登录页

### 2. 文件管理

支持多种文件格式的上传、存储和管理：

- **存储**：文件上传至 MinIO 对象存储
- **预览**：支持文本、图片、PDF 在线预览
- **解析**：PDF/DOCX/图片等文件通过 MinerU API 解析为结构化 Markdown

### 3. 知识库构建

知识库构建采用异步流水线：

```
MinIO 下载文件 → 文档解析（MinerU）→ 页眉页脚过滤 → 
文本分割（Chunk）→ 向量嵌入 → PGVector 存储
```

构建过程在后台异步执行，前端可实时查看构建状态。

### 4. RAG 对话引擎

对话引擎基于 **LlamaIndex** 的 `CondensePlusContextChatEngine`：

- **检索阶段**：使用 `QueryFusionRetriever` 融合 BM25 + 向量检索结果
- **生成阶段**：将检索到的上下文送入 DashScope LLM 生成回答
- **流式输出**：通过 SSE 实时推送 Token 到前端
- **空响应处理**：当检索结果为空时，自动调用 LLM 直接生成，并标注"由 AI 大模型直接生成"

### 5. 混合检索

检索系统结合两种技术优势：

- **BM25 检索**：基于关键词的稀疏检索，擅长精确匹配
- **向量检索**：基于语义相似度的稠密检索，擅长理解意图
- **融合排序**：使用 Reciprocal Rank Fusion (RRF) 算法综合排序

---

## API 文档

启动后端后，可通过以下地址查看交互式 API 文档：

- **Swagger UI**：`http://localhost:8000/docs`
- **ReDoc**：`http://localhost:8000/redoc`

### 主要接口概览

| 方法 | 路径 | 说明 | 认证 |
|------|------|------|------|
| POST | `/users/login` | 用户登录 | 否 |
| POST | `/users/register` | 用户注册 | 否 |
| GET | `/users/me` | 获取当前用户信息 | 是 |
| GET | `/knowledge/list` | 获取知识库列表 | 是 |
| POST | `/knowledge/create` | 创建知识库 | 是 |
| POST | `/knowledge/build/{id}` | 构建知识库 | 是 |
| DELETE | `/knowledge/delete/{id}` | 删除知识库 | 是 |
| POST | `/files/upload` | 上传文件 | 是 |
| GET | `/files/filelist` | 获取文件列表 | 是 |
| POST | `/charts/chat` | AI 对话（SSE 流式） | 是 |
| GET | `/charts/history` | 获取聊天历史 | 是 |

---

## 环境配置

### 后端配置项

所有配置位于 `ai_platform/config/setting.py`，支持通过环境变量覆盖：

| 配置项 | 默认值 | 说明 | 必填 |
|--------|--------|------|------|
| `POSTGRES_HOST` | localhost | PostgreSQL 主机 | 是 |
| `POSTGRES_PORT` | 5432 | PostgreSQL 端口 | 是 |
| `POSTGRES_DB` | knowledge_base | 数据库名 | 是 |
| `POSTGRES_USER` | remember | 数据库用户 | 是 |
| `POSTGRES_PASSWORD` | ServBay.dev | 数据库密码 | 是 |
| `MINIO_ENDPOINT` | localhost:9000 | MinIO 服务端点 | 是 |
| `MINIO_ACCESS_KEY` | minioadmin | MinIO 访问密钥 | 是 |
| `MINIO_SECRET_KEY` | minioadmin | MinIO 秘密密钥 | 是 |
| `JWT_SECRET_KEY` | rag-ai-platform-jwt-secret-key-2026 | JWT 签名密钥 | 是 |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | 1440 | Token 过期时间（分钟）| 否 |
| `DASHSCOPE_APIKEY` | - | 阿里云 DashScope API Key | **是** |

### 前端配置项

创建 `frontend/.env` 文件：

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## 开发指南

### 后端开发

```bash
# 进入后端目录
cd ai_platform

# 运行主服务
python -m main

# 或使用 uvicorn 直接启动
uvicorn ai_platform.main:app --host 0.0.0.0 --port 8000 --reload
```

### 前端开发

```bash
cd frontend

# 启动开发服务器（热重载）
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

### 代码规范

- **后端**：遵循 PEP 8 规范，使用类型注解，异步函数优先
- **前端**：使用 Vue 3 Composition API，TypeScript 类型安全

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建功能分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -am 'Add some feature'`
4. 推送分支：`git push origin feature/your-feature`
5. 创建 Pull Request

---

## 许可证

本项目基于 [MIT License](LICENSE) 开源。

---

<p align="center">
  由 <strong>remember</strong> 构建 | 2026
</p>
