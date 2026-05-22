// 知识库管理API客户端

import { getAuthHeaders } from './auth'
import { API_BASE_URL } from '@/config'

// 知识库类型定义
export interface KnowledgeBase {
  id: string
  name: string
  description?: string
  status: string
  settings?: Record<string, any>
  create_time: string
  update_time?: string
  document_count?: number
  size?: number
}

// 知识库文档类型
export interface KnowledgeDocument {
  id: string
  knowledge_base_id: string
  title: string
  content: string
  file_path?: string
  created_at: string
  updated_at: string
  metadata?: Record<string, any>
}

// API响应类型
export interface ApiResponse<T = any> {
  success: boolean
  code: number
  message: string
  data?: T
  timestamp: string
}

export interface KnowledgeBaseResponse {
  success: boolean
  message: string
  data?: KnowledgeBase
}

export interface KnowledgeBaseListResponse {
  success: boolean
  code: number
  message: string
  data: KnowledgeBase[]
  timestamp: string
}

export interface KnowledgeDocumentListResponse {
  success: boolean
  data: KnowledgeDocument[]
  total: number
}

// 创建知识库请求
export interface CreateKnowledgeBaseRequest {
  name: string
  description?: string
  initial_settings?: {
    chunk_size?: number
    chunk_overlap?: number
    text_split_strategy?: string
    split_chars?: string[]
    index_type?: 'vector' | 'knowledge_graph' | 'long_document'
  }
}

// 更新知识库请求
export interface UpdateKnowledgeBaseRequest {
  name?: string
  description?: string
  metadata?: Record<string, any>
}

// 知识库设置类型
export interface KnowledgeBaseSettings {
  chunk_size: number
  chunk_overlap: number
  text_split_strategy: 'fixed_chars' | 'semantic'
  split_chars: string[]
  index_type: 'vector' | 'knowledge_graph' | 'long_document'
}

// 知识库设置响应
export interface KnowledgeBaseSettingsResponse {
  success: boolean
  message: string
  data?: KnowledgeBaseSettings
}



// 获取知识库列表
export const getKnowledgeBases = async (): Promise<KnowledgeBaseListResponse> => {
  const response = await fetch(`${API_BASE_URL}/knowledge/list`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '获取知识库列表失败')
  }

  return await response.json()
}

// 获取知识库详情
export const getKnowledgeBase = async (kbId: string): Promise<KnowledgeBaseResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/knowledge/bases/${kbId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '获取知识库详情失败')
  }

  return await response.json()
}

// 创建知识库
export const createKnowledgeBase = async (data: CreateKnowledgeBaseRequest): Promise<KnowledgeBaseResponse> => {
  const response = await fetch(`${API_BASE_URL}/knowledge/create`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '创建知识库失败')
  }

  return await response.json()
}

// 更新知识库设置
export const updateKnowledgeBase = async (kbId: string, data: UpdateKnowledgeBaseRequest): Promise<KnowledgeBaseResponse> => {
  const response = await fetch(`${API_BASE_URL}/knowledge/update/${kbId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '更新知识库失败')
  }

  return await response.json()
}

// 构建知识库
export const buildKnowledgeBase = async (kbId: string): Promise<{ success: boolean; message: string; data?: any }> => {
  const response = await fetch(`${API_BASE_URL}/knowledge/build/${kbId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '构建知识库失败')
  }

  return await response.json()
}

// 删除知识库
export const deleteKnowledgeBase = async (kbId: string): Promise<{ success: boolean; message: string }> => {
  const response = await fetch(`${API_BASE_URL}/knowledge/delete/${kbId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '删除知识库失败')
  }

  return await response.json()
}

// 获取知识库文件列表
export const getKnowledgeBaseFiles = async (kbId: string, limit: number = 20, offset: number = 0, status?: string): Promise<{ success: boolean; data: { files: any[]; total: number; limit: number; offset: number }; message: string }> => {
  const params = new URLSearchParams({ limit: limit.toString(), offset: offset.toString() })
  if (status) params.append('status', status)

  const response = await fetch(`${API_BASE_URL}/api/knowledge/bases/${kbId}/files?${params}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '获取知识库文件列表失败')
  }

  return await response.json()
}

// 添加文件到知识库
export const addFilesToKnowledgeBase = async (kbId: string, fileIds: string[]): Promise<{ success: boolean; message: string; added_count: number }> => {
  const response = await fetch(`${API_BASE_URL}/api/knowledge/bases/${kbId}/files`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify({ file_ids: fileIds }),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '添加文件到知识库失败')
  }

  return await response.json()
}

// 从知识库移除文件
export const removeFileFromKnowledgeBase = async (kbId: string, fileId: string): Promise<{ success: boolean; message: string }> => {
  const response = await fetch(`${API_BASE_URL}/api/knowledge/bases/${kbId}/files/${fileId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '从知识库移除文件失败')
  }

  return await response.json()
}

// 搜索知识库
export const searchKnowledgeBase = async (kbId: string, query: string, limit: number = 10): Promise<{ success: boolean; data: { results: any[]; query: string; total: number }; message: string }> => {
  const params = new URLSearchParams({ query, limit: limit.toString() })

  const response = await fetch(`${API_BASE_URL}/api/knowledge/bases/${kbId}/search?${params}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '搜索知识库失败')
  }

  return await response.json()
}

// 获取知识库统计信息
export const getKnowledgeBaseStatistics = async (kbId: string): Promise<{ success: boolean; data: { statistics: any }; message: string }> => {
  const response = await fetch(`${API_BASE_URL}/api/knowledge/bases/${kbId}/statistics`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '获取知识库统计信息失败')
  }

  return await response.json()
}

// 知识库内容片段类型
export interface KnowledgeChunk {
  node_id: string
  text: string
  metadata: Record<string, any>
}

// 知识库内容分页响应
export interface KnowledgeChunkListResponse {
  items: KnowledgeChunk[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

/**
 * 读取知识库内容 — 分页获取向量数据库中的文件片段
 */
export const readKnowledgeBaseContent = async (
  knowledgeBaseId: string,
  page: number = 1,
  pageSize: number = 20
): Promise<KnowledgeChunkListResponse> => {
  const response = await fetch(
    `${API_BASE_URL}/knowledge/read/${knowledgeBaseId}?page=${page}&page_size=${pageSize}`,
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders(),
      },
    }
  )

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '读取知识库内容失败')
  }

  const result = await response.json()
  return result.data as KnowledgeChunkListResponse
}

// 知识库API类
export class KnowledgeAPI {
  /**
   * 获取知识库数据片段
   */
  static async getKnowledgeBaseData(
    knowledgeBaseId: string, 
    limit: number = 50, 
    offset: number = 0, 
    search?: string
  ): Promise<{ success: boolean; data: { chunks: any[]; total: number; limit: number; offset: number }; message: string }> {
    try {
      const params = new URLSearchParams({
        limit: limit.toString(),
        offset: offset.toString()
      })
      
      if (search) {
        params.append('search', search)
      }

      const response = await fetch(`${API_BASE_URL}/api/knowledge/bases/${knowledgeBaseId}/data?${params}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
        },
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('获取知识库数据失败:', error)
      throw error
    }
  }

  /**
   * 获取知识库中的文档列表
   */
  static async getKnowledgeDocuments(
    knowledgeBaseId: string, 
    limit: number = 20, 
    offset: number = 0
  ): Promise<KnowledgeDocumentListResponse> {
    try {
      const params = new URLSearchParams({
        limit: limit.toString(),
        offset: offset.toString()
      })

      const response = await fetch(
        `${API_BASE_URL}/api/knowledge/bases/${knowledgeBaseId}/documents?${params}`, 
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            ...getAuthHeaders(),
          },
        }
      )

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('获取知识库文档列表失败:', error)
      throw error
    }
  }

  /**
   * 获取知识库设置
   */
  static async getKnowledgeBaseSettings(id: string): Promise<KnowledgeBaseSettingsResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/knowledge/bases/${id}/settings`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
        },
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('获取知识库设置失败:', error)
      throw error
    }
  }

  /**
   * 更新知识库设置
   */
  static async updateKnowledgeBaseSettings(id: string, settings: KnowledgeBaseSettings): Promise<KnowledgeBaseSettingsResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/knowledge/update_settings`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...getAuthHeaders(),
        },
        body: JSON.stringify({
          knowledge_base_id: id,
          settings: settings
        }),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('更新知识库设置失败:', error)
      throw error
    }
  }
} 