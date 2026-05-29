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

  // 发送消息到AI（SSE 流式）
  static async sendMessageStream(
    message: string,
    onToken: (token: string) => void,
    onDone: (fullResponse: string, sources: any[]) => void,
    onError: (error: string) => void,
    sessionId?: string,
    knowledgeBaseIds?: string[]
  ): Promise<void> {
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
      }),
    })

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}))
      throw new Error(errData.detail || `HTTP error! status: ${response.status}`)
    }

    this.currentSessionId = useSessionId

    const reader = response.body?.getReader()
    if (!reader) {
      throw new Error('无法获取响应流')
    }

    const decoder = new TextDecoder()
    let buffer = ''

    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              if (data.error) {
                onError(data.error)
                return
              }
              if (data.done) {
                onDone(data.response || '', data.source || [])
                return
              }
              if (data.token) {
                onToken(data.token)
              }
            } catch {
              // ignore parse errors
            }
          }
        }
      }
    } catch (error) {
      onError((error as Error).message || '流式读取中断')
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
