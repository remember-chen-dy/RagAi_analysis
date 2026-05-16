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
          欢迎回来
        </h2>
        <p class="text-gray-500">知识库管理分析平台</p>
      </div>

      <!-- 登录卡片 -->
      <div class="bg-white rounded-xl border border-gray-200 shadow-sm">
        <div class="p-8">
          <form class="space-y-6" @submit.prevent="handleLogin">
            <!-- 用户名输入框 -->
            <div>
              <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
                用户名
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

            <!-- 密码输入框 -->
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                密码
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

            <!-- 记住登录状态 -->
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <input
                  id="remember-me"
                  v-model="form.rememberMe"
                  type="checkbox"
                  class="h-4 w-4 text-gray-600 focus:ring-gray-500 border-gray-300 rounded"
                />
                <label for="remember-me" class="ml-2 block text-sm text-gray-700">
                  记住登录状态
                </label>
              </div>
              <div class="text-sm">
                <a href="#" class="font-medium text-gray-600 hover:text-gray-900 transition-colors">
                  忘记密码？
                </a>
              </div>
            </div>

            <!-- 错误消息 -->
            <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-3">
              <p class="text-red-600 text-sm">{{ errorMessage }}</p>
            </div>

            <!-- 登录按钮 -->
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
                {{ loading ? '登录中...' : '登录' }}
              </button>
            </div>
          </form>
        </div>

        <!-- 底部分割线和注册链接 -->
        <div class="px-8 py-6 bg-gray-50 border-t border-gray-200 rounded-b-xl">
          <div class="text-center">
            <span class="text-sm text-gray-600">还没有账号？</span>
            <router-link
              to="/register"
              class="text-sm font-medium text-gray-900 hover:text-gray-700 ml-1 transition-colors duration-200"
            >
              立即注册
            </router-link>
          </div>
        </div>
      </div>

      <!-- 版权信息 -->
      <div class="text-center">
        <p class="text-sm text-gray-400">
          © 2026 remember - 知识库管理分析平台
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { loginApi } from '@/api/auth'
import { message } from 'ant-design-vue'

const router = useRouter()
const loading = ref(false)
const errorMessage = ref('')

const form = reactive({
  username: '',
  password: '',
  rememberMe: false
})

const handleLogin = async () => {
  if (!form.username || !form.password) {
    errorMessage.value = '请输入用户名和密码'
    return
  }

  loading.value = true
  errorMessage.value = ''
  
  try {
    const result = await loginApi({
      username: form.username,
      password: form.password,
      remember_me: form.rememberMe
    })
    console.log(result)
    // 存储用户信息到 localStorage（兼容现有代码）
    localStorage.setItem('isAuthenticated', 'true')
    // localStorage.setItem('username', result.user.username)
    // localStorage.setItem('userInfo', JSON.stringify(result.user))
    console.log(result)
    if(result.code==200){
     // 登录成功后跳转到主页
     message.success('登录成功')
    await router.push('/files') 
    }else{
      
      errorMessage.value = result.detail || '登录失败，请重试'
    }
    
  } catch (error: any) {
    console.error('登录失败:', error)
    errorMessage.value = error.message || '登录失败，请重试'
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