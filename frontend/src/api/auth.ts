interface LoginRequest {
  username: string
  password: string
  remember_me: boolean
}

interface RegisterRequest {
  username: string
  password: string
  confirm_password: string
  email?: string
  full_name?: string
}

interface UserInfo {
  username: string
  email?: string
  full_name?: string
  is_active: boolean
  is_superuser: boolean
  created_at?: string
  last_login?: string
  avatar_url?: string
  bio?: string
}

interface LoginResponse {
  message: string
  user: UserInfo
  session_token: string
  expires_at: string
}

interface ApiResponse {
  success: boolean
  message: string
  data?: any
}

import { API_BASE_URL } from '@/config'

const getAuthToken = (): string | null => {
  return localStorage.getItem('authToken')
}

// 设置认证令牌
const setAuthToken = (token: string): void => {
  localStorage.setItem('authToken', token)
}

// 移除认证令牌
const removeAuthToken = (): void => {
  localStorage.removeItem('authToken')
}

// 获取认证头
const getAuthHeaders = (): Record<string, string> => {
  const token = getAuthToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

// 登录API
export const loginApi = async (data: LoginRequest): Promise<LoginResponse> => {
  const response = await fetch(`${API_BASE_URL}/users/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '登录失败')
  }

  const result = await response.json()
  
  // 存储认证令牌
  setAuthToken(result.session_token)
  
  return result
}

// 注册API
export const registerApi = async (data: RegisterRequest): Promise<ApiResponse> => {
  const response = await fetch(`${API_BASE_URL}/users/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '注册失败')
  }

  return await response.json()
}

// 登出API
export const logoutApi = async (): Promise<ApiResponse> => {
  const response = await fetch(`${API_BASE_URL}/auth/logout`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || '登出失败')
  }

  // 移除本地存储的令牌
  removeAuthToken()
  
  return await response.json()
}

// 工具函数
export const isAuthenticated = (): boolean => {
  return !!getAuthToken()
}

// 导出令牌管理函数供其他模块使用
export { getAuthToken, setAuthToken, removeAuthToken, getAuthHeaders } 