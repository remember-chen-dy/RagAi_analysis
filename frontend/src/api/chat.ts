import { getAuthHeaders } from './auth'
import { API_BASE_URL } from '@/config'

// 聊天消息类型
export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  session_id: string
}

// 会话类型
export interface ChatSession {
  id: string
  created_at: string
  last_activity: string
  message_count: number
  last_message?: string
  last_message_role?: string
  knowledge_base_ids?: string[]
}

// 聊天API响应类型
export interface ChatResponse {
  success: boolean
  message: string
  data?: {
    session_id: string
    timestamp: string
    user_message: string
    knowledge_base_ids?: string[]
  }
  timestamp?: string
}

// 会话列表响应类型
export interface SessionListResponse {
  success: boolean
  data: Array<{
    id: string
    created_at: string
    last_activity: string
    message_count: number
    last_message?: string
    last_message_role?: string
    knowledge_base_ids?: string[]
  }>
  total: number
  timestamp?: string
}

// 聊天历史响应类型
export interface ChatHistoryItem {
  id: number
  key: string
  timestamp: number
  role: 'user' | 'assistant'
  status: string
  data: {
    role: string
    additional_kwargs: Record<string, any>
    blocks: Array<{
      block_type: string
      text: string
    }>
  }
}

export interface ChatHistoryResponse {
  success: boolean
  message: string
  data: ChatHistoryItem[]
  timestamp?: string
}

function parseKnowledgeBaseIds(raw: any): string[] {
  if (!raw) return []
  if (Array.isArray(raw)) return raw
  try {
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

// 聊天API接口
export class ChatAPI {
  private static baseURL = API_BASE_URL
  private static currentSessionId: string | null = null

  // 设置当前会话ID
  static setCurrentSession(sessionId: string | null) {
    this.currentSessionId = sessionId
  }

  // 创建新会话
  static async createNewSession(knowledgeBaseIds?: string[]): Promise<string> {
    try {
      const payload: any = {}
      if (knowledgeBaseIds && knowledgeBaseIds.length > 0) {
        payload.knowledge_base_ids = knowledgeBaseIds
      }

      const response = await fetch(`${this.baseURL}/charts/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
        },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      if (!data.success) {
        throw new Error(data.message || '创建会话失败')
      }

      this.currentSessionId = data.data?.session_id
      return data.data?.session_id
    } catch (error) {
      console.error('创建新会话失败:', error)
      throw error
    }
  }

  // 发送消息到AI
  static async sendMessage(
    message: string, 
    sessionId?: string, 
    knowledgeBaseIds?: string[]
  ): Promise<string> {
    try {
      const useSessionId = sessionId || this.currentSessionId || await this.createNewSession()
      
      const response = await fetch(`${this.baseURL}/charts/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
        },
        body: JSON.stringify({
          message: message,
          session_id: useSessionId,
          knowledge_base_ids: knowledgeBaseIds,
          use_reranker: true,
          use_refiner: true,
          top_k: 5
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data: ChatResponse = await response.json()
      
      if (!data.success) {
        throw new Error(data.message || '发送消息失败')
      }

      // 更新当前会话ID
      this.currentSessionId = data.data?.session_id || useSessionId

      return data.message
    } catch (error) {
      console.error('发送消息到AI失败:', error)
      throw error
    }
  }

  // 获取会话列表
  static async getSessions(): Promise<ChatSession[]> {
    try {
      const response = await fetch(`${this.baseURL}/charts/all`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
        },
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()

      if (!data.success) {
        throw new Error('获取会话列表失败')
      }

      return (data.data || []).map((s: any) => ({
        id: s.id,
        created_at: s.created_at,
        last_activity: s.last_activity,
        message_count: s.message_count,
        last_message: s.last_message,
        last_message_role: s.last_message_role,
        knowledge_base_ids: parseKnowledgeBaseIds(s.knowledge_base_ids),
      }))
    } catch (error) {
      console.error('获取会话列表失败:', error)
      return []
    }
  }

  // 获取指定会话的聊天历史
  static async getChatHistory(sessionId: string): Promise<ChatMessage[]> {
    try {
      const response = await fetch(`${this.baseURL}/charts/history`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
        },
        body: JSON.stringify({
          session_id: sessionId
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data: ChatHistoryResponse = await response.json()
      
      if (!data.success) {
        throw new Error(data.message || '获取聊天历史失败')
      }

      return (data.data || []).map((item: ChatHistoryItem) => {
        const textBlock = item.data?.blocks?.find(b => b.block_type === 'text')
        const content = textBlock?.text || ''
        const timestampMs = item.timestamp / 1e6
        const timestamp = new Date(timestampMs).toISOString()
        
        return {
          id: item.id.toString(),
          role: item.role,
          content: content,
          timestamp: timestamp,
          session_id: item.key
        }
      })
    } catch (error) {
      console.error('获取聊天历史失败:', error)
      return []
    }
  }

  // 删除会话
  static async deleteSession(sessionId: string): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/charts/delete`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
        },
        body: JSON.stringify({
          session_id: sessionId
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      
      if (!data.success) {
        throw new Error(data.message || '删除会话失败')
      }

      if (sessionId === this.currentSessionId) {
        this.currentSessionId = null
      }
    } catch (error) {
      console.error('删除会话失败:', error)
      throw error
    }
  }

}

// 模拟API调用（当后端API不可用时使用）
export async function simulateChatAPI(question: string): Promise<string> {
  // 模拟网络延迟
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000))
  
  // 包含Markdown格式的模拟回复
  const responses = [
    `关于 **"${question}"** 这个问题，我需要基于您上传的文档来提供准确答案。

## 建议步骤：
1. 确保您已上传相关文档
2. 检查文档内容是否完整
3. 重新提问具体细节

> 💡 **提示**：更具体的问题能帮助我提供更精准的答案。`,

    `我理解您询问的是 \`${question}\`。根据我对文档的分析，这是一个很好的问题。

### 文档分析要点：
- **关键信息**：需要进一步核实
- **相关内容**：正在检索中
- **建议**：可以提供更多上下文

---

如需更详细的分析，请告诉我您希望了解的具体方面。`,

         `针对您的问题 **"${question}"**，我建议您可以从以下几个角度来思考：

### 🔍 分析维度：
* **技术层面**：核心概念和实现
* **应用场景**：实际使用情况
* **最佳实践**：推荐的做法

\`\`\`
示例代码或关键信息将在这里显示
\`\`\`

希望这个框架对您有帮助！`,

    `感谢您的提问。关于 **"${question}"**，我会根据文档内容为您提供详细解答。

## 📋 分析结果：

1. **主要观点**
   - 核心概念解释
   - 关键要素分析

2. **详细说明**
   - 具体实现方式
   - 注意事项

> **注意**：此分析基于当前可用的文档内容。`,

    `基于文档内容分析，关于 **"${question}"** 这个问题，我可以为您提供以下见解：

### ✨ 关键发现：

| 方面 | 说明 |
|------|------|
| 重要性 | 高优先级 |
| 复杂度 | 中等 |
| 建议 | 需要详细了解 |

**总结**：这是一个很有价值的问题，建议深入探讨相关细节。

---

如需了解更多，请随时追问！`,
  ]
  
  return responses[Math.floor(Math.random() * responses.length)]
} 