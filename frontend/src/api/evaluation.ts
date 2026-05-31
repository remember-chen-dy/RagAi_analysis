import { getAuthHeaders, removeAuthToken } from './auth'
import { API_BASE_URL } from '@/config'

export interface EvaluationRequest {
  knowledge_base_ids: string[]
  index_type: string
  testset_size: number
  similarity_top_k: number
  metrics: string[]
}

export interface SampleResult {
  question: string
  ground_truth: string
  answer: string
  contexts: string[]
  error?: string
}

export interface EvaluationResultData {
  samples: SampleResult[]
  aggregate_scores: Record<string, number>
  knowledge_base_ids: string[]
  index_type: string
  sample_count: number
}

export interface EvaluationResponse {
  success: boolean
  code: number
  message: string
  data: EvaluationResultData
  timestamp: string
}

export const evaluateRag = async (request: EvaluationRequest): Promise<EvaluationResponse> => {
  const response = await fetch(`${API_BASE_URL}/knowledge/evaluate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify(request),
  })

  if (response.status === 401) {
    removeAuthToken()
    window.location.href = '/login'
    throw new Error('登录已过期，请重新登录')
  }

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'RAG评估失败')
  }

  return await response.json()
}
