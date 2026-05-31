import { API_BASE_URL } from '@/config'

interface LoginRequest {
  username: string
  password: string
}

interface RegisterRequest {
  username: string
  password: string
  email?: string
}

interface UserInfo {
  username: string
  email?: string
  is_active: boolean
  avatar_url?: string
}

interface ApiResponse<T = any> {
  success: boolean
  message: string
  code: number
  data?: T
}

interface LoginData {
  token: string
  token_type: string
  expires_in: number
  user: UserInfo
}

const getAuthToken = (): string | null => {
  return localStorage.getItem('authToken')
}

const setAuthToken = (token: string): void => {
  localStorage.setItem('authToken', token)
}

const removeAuthToken = (): void => {
  localStorage.removeItem('authToken')
  localStorage.removeItem('isAuthenticated')
  localStorage.removeItem('userInfo')
}

const getUserInfo = (): UserInfo | null => {
  const info = localStorage.getItem('userInfo')
  if (info) {
    try {
      return JSON.parse(info)
    } catch {
      return null
    }
  }
  return null
}

const setUserInfo = (user: UserInfo): void => {
  localStorage.setItem('userInfo', JSON.stringify(user))
}

const getAuthHeaders = (): Record<string, string> => {
  const token = getAuthToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

const loginApi = async (data: LoginRequest): Promise<ApiResponse<LoginData>> => {
  const response = await fetch(`${API_BASE_URL}/users/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  const result = await response.json()

  if (!response.ok || !result.success) {
    throw new Error(result.detail || result.message || '登录失败')
  }

  if (result.data?.token) {
    setAuthToken(result.data.token)
    setUserInfo(result.data.user)
    localStorage.setItem('isAuthenticated', 'true')
  }

  return result
}

const registerApi = async (data: RegisterRequest): Promise<ApiResponse> => {
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

const logoutApi = (): void => {
  removeAuthToken()
}

const isAuthenticated = (): boolean => {
  return !!getAuthToken()
}

export {
  getAuthToken,
  setAuthToken,
  removeAuthToken,
  getUserInfo,
  setUserInfo,
  getAuthHeaders,
  loginApi,
  registerApi,
  logoutApi,
  isAuthenticated,
}

export type { UserInfo, LoginData, ApiResponse }
