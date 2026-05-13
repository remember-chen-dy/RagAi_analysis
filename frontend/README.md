# AI智能平台前端

这是一个基于Vue 3 + TypeScript + Tailwind CSS的现代化前端应用，提供文件管理和AI对话功能。

## 功能特性

### 🗂️ 文件管理页面
- **文件上传**: 支持拖拽上传和点击选择文件
- **多文件上传**: 同时上传多个文件
- **上传进度**: 实时显示上传进度
- **文件管理**: 查看已上传文件列表
- **文件预览**: 支持文件大小显示和状态管理

### 💬 AI对话页面
- **智能对话**: 与AI助手进行多轮对话
- **实时响应**: 支持实时消息发送和接收
- **对话历史**: 显示完整的对话记录
- **清空功能**: 支持清空对话历史
- **API集成**: 支持真实API调用和模拟API fallback

## 技术栈

- **框架**: Vue 3 + Composition API
- **语言**: TypeScript
- **样式**: Tailwind CSS
- **路由**: Vue Router 4
- **构建工具**: Vite
- **包管理**: pnpm

## 项目结构

```
src/
├── api/                 # API接口
│   ├── chat.ts         # 聊天API
│   └── upload.ts       # 文件上传API
├── components/         # 组件
│   ├── FileUpload.vue  # 文件上传组件
│   └── Layout.vue      # 布局组件
├── views/              # 页面
│   ├── FileManager.vue # 文件管理页面
│   └── ChatBot.vue     # AI对话页面
├── router/             # 路由配置
│   └── index.ts        # 路由定义
├── types/              # 类型定义
│   └── index.ts        # 通用类型
├── App.vue             # 根组件
└── main.ts             # 入口文件
```

## 开发指南

### 安装依赖

```bash
pnpm install
```

### 启动开发服务器

```bash
pnpm dev
```

### 构建生产版本

```bash
pnpm build
```

### 预览生产构建

```bash
pnpm preview
```

## 页面导航

### 文件管理 (`/files`)
- 默认首页
- 文件上传和管理功能
- 支持拖拽上传
- 显示上传进度和文件状态

### AI对话 (`/chat`)
- 智能对话界面
- 多轮对话支持
- 实时消息显示
- 对话历史管理

## API集成

### 聊天API
- **发送消息**: `POST /api/chat`
- **获取历史**: `GET /api/chat/history`
- **清空历史**: `DELETE /api/chat/clear`

### 文件上传API
- **上传文件**: `POST /api/upload`
- **获取文件列表**: `GET /api/files`
- **删除文件**: `DELETE /api/files/:id`

## 配置说明

### API地址配置
在 `src/api/chat.ts` 中修改后端API地址：

```typescript
private static baseURL = 'http://localhost:8000' // 修改为实际的后端地址
```

### 路由配置
在 `src/router/index.ts` 中管理页面路由。

## 样式定制

项目使用Tailwind CSS，可以通过以下方式定制样式：

1. 修改 `tailwind.config.js` 配置
2. 在组件中使用Tailwind类名
3. 在 `src/style.css` 中添加全局样式

## 浏览器支持

- Chrome (推荐)
- Firefox
- Safari
- Edge

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

MIT License
