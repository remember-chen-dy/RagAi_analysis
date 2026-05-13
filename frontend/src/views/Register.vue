<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo和标题区域 -->
      <div class="text-center">
        <div class="flex justify-center mb-6">
          <div class="w-16 h-16 bg-gray-900 rounded-xl flex items-center justify-center shadow-lg">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
        </div>
        <h2 class="text-3xl font-light text-gray-900 mb-2">
          创建账号
        </h2>
        <p class="text-gray-500">加入 妙码AI知识库管理分析平台</p>
      </div>

      <!-- 注册卡片 -->
      <div class="bg-white rounded-xl border border-gray-200 shadow-sm">
        <div class="p-8">
          <form class="space-y-6" @submit.prevent="handleRegister">
            <!-- 用户名输入框 -->
            <div>
              <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
                用户名 *
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <input
                  id="username"
                  v-model="form.username"
                  type="text"
                  required
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-transparent placeholder-gray-400 text-gray-900 transition-colors"
                  placeholder="请输入用户名"
                />
              </div>
            </div>

            <!-- 邮箱输入框 -->
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
                邮箱地址（可选）
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                </div>
                <input
                  id="email"
                  v-model="form.email"
                  type="email"
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-transparent placeholder-gray-400 text-gray-900 transition-colors"
                  placeholder="请输入邮箱地址"
                />
              </div>
            </div>

            <!-- 真实姓名输入框 -->
            <div>
              <label for="fullName" class="block text-sm font-medium text-gray-700 mb-2">
                真实姓名（可选）
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <input
                  id="fullName"
                  v-model="form.fullName"
                  type="text"
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-transparent placeholder-gray-400 text-gray-900 transition-colors"
                  placeholder="请输入真实姓名"
                />
              </div>
            </div>

            <!-- 密码输入框 -->
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                密码 *
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <input
                  id="password"
                  v-model="form.password"
                  type="password"
                  required
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-transparent placeholder-gray-400 text-gray-900 transition-colors"
                  placeholder="请输入密码"
                />
              </div>
            </div>

            <!-- 确认密码输入框 -->
            <div>
              <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
                确认密码 *
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <input
                  id="confirmPassword"
                  v-model="form.confirmPassword"
                  type="password"
                  required
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-transparent placeholder-gray-400 text-gray-900 transition-colors"
                  placeholder="请再次输入密码"
                />
              </div>
            </div>

            <!-- 服务条款 -->
            <div class="flex items-center">
              <input
                id="agree-terms"
                v-model="form.agreeTerms"
                type="checkbox"
                required
                class="h-4 w-4 text-gray-600 focus:ring-gray-500 border-gray-300 rounded"
              />
              <label for="agree-terms" class="ml-2 block text-sm text-gray-700">
                我已阅读并同意
                <a href="#" class="font-medium text-gray-900 hover:text-gray-700">服务条款</a>
                和
                <a href="#" class="font-medium text-gray-900 hover:text-gray-700">隐私政策</a>
              </label>
            </div>

            <!-- 错误/成功消息 -->
            <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-3">
              <p class="text-red-600 text-sm">{{ errorMessage }}</p>
            </div>
            
            <div v-if="successMessage" class="bg-green-50 border border-green-200 rounded-lg p-3">
              <p class="text-green-600 text-sm">{{ successMessage }}</p>
            </div>

            <!-- 注册按钮 -->
            <div>
              <button
                type="submit"
                :disabled="loading"
                class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-gray-900 hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
              >
                <span v-if="loading" class="absolute left-0 inset-y-0 flex items-center pl-3">
                  <svg class="h-5 w-5 text-white animate-spin" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </span>
                {{ loading ? '注册中...' : '创建账号' }}
              </button>
            </div>
          </form>
        </div>

        <!-- 底部分割线和登录链接 -->
        <div class="px-8 py-6 bg-gray-50 border-t border-gray-200 rounded-b-xl">
          <div class="text-center">
            <span class="text-sm text-gray-600">已有账号？</span>
            <router-link
              to="/login"
              class="text-sm font-medium text-gray-900 hover:text-gray-700 ml-1 transition-colors duration-200"
            >
              立即登录
            </router-link>
          </div>
        </div>
      </div>

      <!-- 版权信息 -->
      <div class="text-center">
        <p class="text-sm text-gray-400">
          © 2025 行明 - AI知识库管理分析平台
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { registerApi } from '@/api/auth'

const router = useRouter()
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const form = reactive({
  username: '',
  email: '',
  fullName: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false
})

const handleRegister = async () => {
  // 基本验证
  if (!form.username || !form.password || !form.confirmPassword) {
    errorMessage.value = '请填写所有必填字段'
    return
  }

  if (form.password !== form.confirmPassword) {
    errorMessage.value = '两次输入的密码不一致'
    return
  }

  if (form.password.length < 6) {
    errorMessage.value = '密码长度至少为6位'
    return
  }

  if (!form.agreeTerms) {
    errorMessage.value = '请同意服务条款和隐私政策'
    return
  }

  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''
  
  try {
    await registerApi({
      username: form.username,
      password: form.password,
      confirm_password: form.confirmPassword,
      email: form.email || undefined,
      full_name: form.fullName || undefined
    })
    
    successMessage.value = '注册成功！正在跳转到登录页面...'
    
    // 3秒后跳转到登录页面
    setTimeout(() => {
      router.push('/login')
    }, 2000)
    
  } catch (error: any) {
    console.error('注册失败:', error)
    errorMessage.value = error.message || '注册失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* 确保与整体风格一致的额外样式 */
.transition-colors {
  transition-property: color, background-color, border-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}
</style> 