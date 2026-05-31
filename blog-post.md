# 从零构建企业级 RAG 知识库平台：FastAPI + Vue 3 + LlamaIndex 实战

> 本文将详细介绍如何基于 FastAPI、Vue 3 和 LlamaIndex 构建一套完整的企业级 RAG（检索增强生成）知识库管理与 AI 对话平台。涵盖架构设计、核心功能实现、以及多个生产级 Bug 的修复经验。

---

## 目录

1. [项目概述](#1-项目概述)
2. [技术架构选型](#2-技术架构选型)
3. [核心功能实现](#3-核心功能实现)
4. [生产环境踩坑记录](#4-生产环境踩坑记录)
5. [项目结构](#5-项目结构)
6. [快速开始](#6-快速开始)
7. [总结与展望](#7-总结与展望)

---

## 1. 项目概述

在日常工作中，企业积累了大量的文档资料——产品手册、技术文档、会议纪要、规章制度等。如何让这些沉睡的文档"活"起来，成为一个能听懂人话、能回答问题的智能助手？这就是 RAG（Retrieval-Augmented Generation，检索增强生成）技术的核心价值。

本项目是一套**完整的企业级 RAG 平台**，实现了从文档上传、知识库构建、到 AI 智能对话的全流程。用户可以将 PDF、Word、PPT、图片等多种格式的文档上传至平台，系统自动解析、分块、向量化并存储，随后即可通过自然语言与知识库进行对话。

### 核心能力

- **多格式文档解析**：PDF、DOCX、PPT、XLS、PNG、JPG、Markdown
- **混合检索**：BM25 关键词检索 + 向量语义检索双管齐下
- **流式对话**：基于 SSE 的实时流式响应，体验媲美 ChatGPT
- **JWT 认证**：完整的用户登录、Token 鉴权、路由守卫体系
- **异步构建**：知识库构建不阻塞前端，后台静默完成

---

## 2. 技术架构选型

### 后端技术栈

| 组件 | 选型 | 理由 |
|------|------|------|
| Web 框架 | **FastAPI** | 原生异步支持、自动 API 文档、类型安全 |
| RAG 框架 | **LlamaIndex** | 业界最成熟的 RAG 框架，索引、检索、对话引擎一应俱全 |
| LLM | **DashScope（通义千问）** | 国内稳定可用，支持流式输出，Embedding 质量优秀 |
| 向量数据库 | **PostgreSQL + PGVector** | 关系型数据库 + 向量扩展，一库两用 |
| 对象存储 | **MinIO** | 兼容 S3 API，私有化部署首选 |
| ORM | **SQLAlchemy 2.0** | 异步支持完善，类型提示友好 |

### 前端技术栈

| 组件 | 选型 | 理由 |
|------|------|------|
| 框架 | **Vue 3 + Composition API** | 响应式系统优秀，组合式 API 逻辑复用方便 |
| UI 组件 | **Ant Design Vue 4** | 企业级组件库，聊天场景组件丰富 |
| 样式 | **Tailwind CSS 4** | 原子化 CSS，开发效率极高 |
| 构建 | **Vite 6** | 冷启动秒开，HMR 极速 |

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

## 3. 核心功能实现

### 3.1 文档解析流水线

文档解析是整个 RAG 系统的第一道关卡。不同格式的文档需要不同的解析策略：

**文本文件** → 直接读取内容

解析后的文本会经过**页眉页脚过滤器**（基于正则匹配高频重复文本），去除无关内容，保留有效信息。

```python
# 数据处理流水线核心逻辑
class FileDataPipeline:
    async def process_minio_file(self):
        # 1. 从 MinIO 下载文件
        file_path = await self._download_from_minio(object_name)
        
        # 2. 文档解析（MinerU / 原生 Reader）
        documents = DataLoader.load_file_dir([file_path])
        
        # 3. 页眉页脚过滤
        filter_component = AdvancedHeaderFooterFilter()
        documents = filter_component.filter_documents(documents)
        
        # 4. 文本分割（Chunk）
        transformer = TransformerComponent(self.settings)
        pipeline = transformer.create_pipeline(documents)
        nodes = pipeline.run()
        
        # 5. 存入向量数据库
        await self._store_to_vector_db(nodes, self.settings.index_type)
```

### 3.2 混合检索引擎

单一检索方式各有短板：
- **BM25** 擅长精确关键词匹配，但无法理解语义
- **向量检索** 擅长语义理解，但对专有名词拼写敏感

我们的方案是**两者融合**，使用 LlamaIndex 的 `QueryFusionRetriever`：

```python
# 混合检索：BM25 + 向量检索
retriever = QueryFusionRetriever(
    [vector_retriever, bm25_retriever],
    similarity_top_k=5,
    num_queries=1,
    mode=FUSION_MODES.RECIPROCAL_RANK,
)
```

BM25 从 PGVector 中直接拉取节点（而非内存 docstore），解决了分布式部署时的状态一致性问题。

### 3.3 流式对话实现

流式输出是提升用户体验的关键。我们采用 **SSE（Server-Sent Events）** 实现：

**后端**：FastAPI 的 `StreamingResponse` + `async_response_gen()` 异步生成器

```python
@router.post("/chat")
async def chat(request: ChatRequest):
    async def event_stream():
        engine = await get_chat_engine(request.knowledge_base_id)
        streaming_response = await engine.astream_chat(request.message)
        
        # 缓冲 token，判断 Empty Response 后再决定发送策略
        async for token in streaming_response.async_response_gen():
            yield f"data: {json.dumps({'token': token})}\n\n"
    
    return StreamingResponse(event_stream(), media_type="text/event-stream")
```

**前端**：`fetch` + `ReadableStream` 逐段解析

```typescript
const response = await fetch('/charts/chat', { method: 'POST', body })
const reader = response.body!.getReader()
const decoder = new TextDecoder()

while (true) {
    const { done, value } = await reader.read()
    if (done) break
    const chunk = decoder.decode(value)
    // 解析 SSE 格式：data: {"token": "xxx"}\n\n
    const lines = chunk.split('\n\n')
    for (const line of lines) {
        if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6))
            displayToken(data.token)
        }
    }
}
```

### 3.4 JWT 认证体系

平台采用无状态的 JWT 认证，前后端分离设计：

**后端**：PyJWT 签发 Token，FastAPI `HTTPBearer` 依赖注入验证

```python
# JWT 工具
security = HTTPBearer()

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=1440)
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm="HS256")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = decode_access_token(credentials.credentials)
    return {"username": payload.get("sub")}
```

**前端**：`localStorage` 存储 Token，请求自动携带，401 自动跳转

```typescript
// 请求拦截
const token = localStorage.getItem('authToken')
const headers = token ? { Authorization: `Bearer ${token}` } : {}

// 401 处理
if (response.status === 401) {
    localStorage.removeItem('authToken')
    window.location.href = '/login'
}
```

---

## 4. 生产环境踩坑记录

项目开发过程中遇到了大量"书本上学不到"的问题，以下是几个典型：

### 4.1 事件循环死锁

**现象**：在 FastAPI 的异步环境中调用同步的 LlamaIndex API 时，程序卡住不动。

**根因**：`asyncio.run()` 在已有事件循环的线程中调用会报错，而 `future.result()` 会阻塞当前线程。

**修复**：使用 `ThreadPoolExecutor` 在新线程中运行同步代码：

```python
def asyncio_get_or_run(coro):
    try:
        loop = asyncio.get_running_loop()
        # 已有事件循环，在新线程中运行
        with ThreadPoolExecutor() as pool:
            return pool.submit(asyncio.run, coro).result()
    except RuntimeError:
        # 没有事件循环，直接运行
        return asyncio.run(coro)
```

### 4.2 DashScope 流式输出重复

**现象**：SSE 流式输出时，每个 token 都包含了之前所有的文本，导致内容不断重复叠加。

**根因**：DashScope 的 `astream_complete` 返回的是**累积文本**而非增量文本。

**修复**：计算 delta 差值：

```python
previous_text = ""
async for token in streaming_response.async_response_gen():
    token_text = str(token)
    delta = token_text[len(previous_text):]  # 只取新增部分
    previous_text = token_text
    yield f"data: {json.dumps({'token': delta})}\n\n"
```

### 4.3 BM25 检索器数据源为空

**现象**：`Please pass exactly one of index, nodes, or docstore.`

**根因**：PGVectorStore 的节点存储在 PostgreSQL 中，不在内存 docstore，BM25 初始化时找不到数据源。

**修复**：从 PGVector 直接拉取节点：

```python
nodes = await vector_store.get_nodes(filters=filters)
bm25_retriever = BM25Retriever.from_defaults(nodes=nodes, similarity_top_k=5)
```

### 4.4 协程对象被当作数据使用

**现象**：`a bytes-like object is required, not 'coroutine'`

**根因**：`async def` 方法调用时缺少 `await`，返回的是 coroutine 对象而非实际数据。

**修复**：梳理整个调用链，确保每个 async 方法都有对应的 `await`：

```python
# 错误
documents = filter_component.filter_documents(documents)  # 返回 coroutine！

# 正确
documents = await filter_component.filter_documents(documents)
```


---

## 5. 项目结构

```
rag-ai-platform/
├── ai_platform/                    # 后端主目录
│   ├── api/                        # API 路由层
│   │   ├── auth.py                 # JWT 认证（登录/注册/Token 验证）
│   │   ├── chart.py                # SSE 流式对话接口
│   │   ├── knowledge.py            # 知识库 CRUD + 构建
│   │   └── upload.py               # 文件上传/列表/删除/预览
│   ├── config/                     # 配置模块
│   │   ├── auth.py                 # JWT 签发与解码工具
│   │   ├── resource.py             # LLM/Embedding/向量库初始化
│   │   ├── setting.py              # 系统配置（数据库/MinIO/JWT）
│   │   └── swagger_config.py       # Swagger 文档配置
│   ├── models/                     # SQLAlchemy 数据模型
│   │   ├── user.py                 # 用户/密码哈希/会话管理
│   │   └── session.py              # 聊天记录/历史会话
│   ├── pipeline/                   # 数据处理流水线
│   │   ├── dataPipeline.py         # 主流程：下载→解析→分割→存储
│   │   ├── data_filter.py          # 页眉页脚过滤器
│   │   ├── loader.py               # 多格式文档加载器（MinerU 集成）
│   │   └── transformer.py          # 文本分割/节点转换
│   ├── query_engine/               # RAG 查询引擎
│   │   ├── rag_engine.py           # 混合检索 + 流式生成引擎
│   │   └── chat_instance.py        # 聊天实例生命周期管理
│   ├── services/                   # 业务服务层
│   │   ├── konwledge_service.py    # 知识库业务逻辑（含后台任务）
│   │   └── minio_service.py        # MinIO 文件操作封装
│   └── main.py                     # FastAPI 应用入口
├── frontend/                       # 前端主目录
│   ├── src/
│   │   ├── api/                    # API 请求封装（含 401 拦截）
│   │   ├── components/             # 公共组件（上传/布局/Markdown）
│   │   ├── router/                 # Vue Router + Token 路由守卫
│   │   └── views/                  # 页面视图
│   │       ├── Login.vue           # 登录（表单校验）
│   │       ├── Register.vue        # 注册（表单校验）
│   │       ├── FileManager.vue     # 文件管理
│   │       ├── KnowledgeBase.vue   # 知识库管理
│   │       └── ChatBot.vue         # AI 对话（SSE 解析）
│   └── package.json
├── .env.example                    # 环境变量模板
├── pyproject.toml                  # Python 依赖
└── README.md                       # 项目文档
```

---

## 6. 快速开始

### 环境要求

- Python >= 3.14
- Node.js >= 18
- PostgreSQL >= 15（启用 pgvector 扩展）
- MinIO Server
- DashScope API Key

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/rag-ai-platform.git
cd rag-ai-platform
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入数据库、MinIO、DashScope API Key 等配置
```

### 3. 启动后端

```bash
python -m venv venv
source venv/bin/activate
pip install -e .
python -m ai_platform.main
```

### 4. 启动前端

```bash
cd frontend
npm install
npm run dev
```

访问 `http://localhost:5173` 即可使用。

---

## 7. 总结与展望

本项目从 0 到 1 构建了一套完整的企业级 RAG 平台，涵盖了文档解析、知识库管理、混合检索、流式对话、用户认证等核心能力。开发过程中踩过的坑——从 asyncio 事件循环死锁到 DashScope 累积文本的 delta 计算——都是生产环境中真实会遇到的问题。

### 后续可扩展方向

- **多租户支持**：企业级 SaaS 化，数据隔离
- **更丰富的评估指标**：基于 Ragas 的自动化评估
- **Agent 能力**：支持工具调用、多步推理
- **多模态对话**：图片理解、图表生成

如果你也在构建 RAG 系统，希望本文的经验能帮你少走一些弯路。欢迎 Star 和 Fork！

---

> 项目地址：https://github.com/yourusername/rag-ai-platform
> 技术栈：FastAPI | Vue 3 | LlamaIndex | PostgreSQL | MinIO | DashScope
