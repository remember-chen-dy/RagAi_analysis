import { API_BASE_URL } from '@/config'
import { getAuthToken, removeAuthToken } from '@/api/auth'

interface RequestOptions extends RequestInit {
  params?: Record<string, string>
}

async function request<T = any>(url: string, options: RequestOptions = {}): Promise<T> {
  const { params, headers: customHeaders, ...restOptions } = options

  let fullUrl = `${API_BASE_URL}${url}`
  if (params) {
    const searchParams = new URLSearchParams(params)
    fullUrl += `?${searchParams.toString()}`
  }

  const token = getAuthToken()
  const headers: Record<string, string> = {
    ...(customHeaders as Record<string, string>),
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  if (!(restOptions.body instanceof FormData)) {
    headers['Content-Type'] = headers['Content-Type'] || 'application/json'
  }

  const response = await fetch(fullUrl, {
    ...restOptions,
    headers,
  })

  if (response.status === 401) {
    removeAuthToken()
    window.location.href = '/login'
    throw new Error('登录已过期，请重新登录')
  }

  const result = await response.json()

  if (!response.ok) {
    throw new Error(result.detail || result.message || '请求失败')
  }

  return result
}

export function get<T = any>(url: string, params?: Record<string, string>): Promise<T> {
  return request<T>(url, { method: 'GET', params })
}

export function post<T = any>(url: string, data?: any): Promise<T> {
  return request<T>(url, {
    method: 'POST',
    body: data instanceof FormData ? data : JSON.stringify(data),
  })
}

export function put<T = any>(url: string, data?: any): Promise<T> {
  return request<T>(url, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
}

export function del<T = any>(url: string): Promise<T> {
  return request<T>(url, { method: 'DELETE' })
}

export default request
