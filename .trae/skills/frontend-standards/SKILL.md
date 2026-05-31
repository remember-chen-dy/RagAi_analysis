---
name: frontend-standards
description: 前端代码规范，强制使用 Ant Design Vue 组件库。当用户要求编写 Vue 页面、组件、表单、表格或任何 UI 代码时自动应用。
---

# 前端代码规范（Vue 3 + Ant Design Vue）

你是一个资深前端工程师，编写的所有 Vue 3 代码必须遵循以下规范。

## 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue | 3.x | Composition API 优先 |
| Ant Design Vue | 4.x / 3.x | 唯一允许的 UI 组件库 |
| TypeScript | 5.x | 必须使用 |
| Vite | 5.x | 推荐构建工具 |

## 组件库限制

**唯一允许的 UI 组件库：Ant Design Vue (antdv)**

- ✅ 必须使用：`AButton`、`AInput`、`AForm`、`ATable`、`AModal`、`ASelect`、`ADatePicker` 等 antdv 组件
- ❌ 禁止使用：原生 HTML 按钮/输入框（除非无法替代）、其他组件库（Element Plus、Naive UI、Vuetify 等）
- ❌ 禁止自己封装基础组件（应直接使用 antdv 并做样式定制）

### 导入规范

```vue
<script setup lang="ts">
// ✅ 正确：按需导入
import { Button, Input, Form, Table, message } from 'ant-design-vue'
import type { TableColumnsType } from 'ant-design-vue'

// ✅ 或使用别名
import AButton from 'ant-design-vue/es/button'
import AInput from 'ant-design-vue/es/input'

// ❌ 错误：全量导入（除非必要）
import Antd from 'ant-design-vue'

// ❌ 错误：使用其他组件库
import { ElButton } from 'element-plus'
</script>