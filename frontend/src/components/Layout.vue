<template>
  <div class="h-screen flex flex-col bg-gray-50 overflow-hidden">
    <!-- 导航栏 -->
    <nav class="bg-white border-b border-gray-200 flex-shrink-0 shadow-sm">
      <div class="max-w-full mx-auto px-8">
        <div class="flex items-center justify-between h-16">
          <!-- Logo -->
          <div class="flex items-center">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-gray-900 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
              </div>
              <h1 class="text-xl font-light text-gray-900">AI 智能平台</h1>
            </div>
          </div>

          <!-- 导航菜单 -->
          <div class="hidden md:block">
            <div class="flex items-center space-x-1">
              <router-link
                  to="/files"
                  class="flex items-center text-gray-600 hover:text-gray-900 px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200"
                  :class="{ 'text-gray-900 bg-gray-100': $route.path === '/files' }"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 5a2 2 0 012-2h4a2 2 0 012 2v4H8V5z"></path>
                </svg>
                文件管理
              </router-link>
              <router-link
                  to="/knowledge"
                  class="flex items-center text-gray-600 hover:text-gray-900 px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200"
                  :class="{ 'text-gray-900 bg-gray-100': $route.path === '/knowledge' }"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 011-1h6a1 1 0 011 1v2M7 7h10"/>
                </svg>
                知识库
              </router-link>
              <router-link
                  to="/chat"
                  class="flex items-center text-gray-600 hover:text-gray-900 px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200"
                  :class="{ 'text-gray-900 bg-gray-100': $route.path === '/chat' }"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                </svg>
                AI 对话
              </router-link>
            </div>
          </div>

          <!-- 右侧操作区域 -->
          <div class="hidden md:flex items-center space-x-4">
            <!-- 用户信息 -->
            <span class="text-sm text-gray-600">{{ username }}</span>

            <!-- 退出登录按钮 -->
            <button
                @click="handleLogout"
                class="text-gray-600 hover:text-gray-900 p-2 rounded-lg hover:bg-gray-100 transition-colors"
                title="退出登录"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
              </svg>
            </button>
          </div>

          <!-- 移动端菜单按钮 -->
          <div class="md:hidden">
            <button
                @click="toggleMobileMenu"
                class="text-gray-600 hover:text-gray-900 p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                    v-if="!showMobileMenu"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 6h16M4 12h16M4 18h16"
                />
                <path
                    v-else
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- 移动端菜单 -->
      <div
          v-show="showMobileMenu"
          class="md:hidden bg-white border-t border-gray-100"
      >
        <div class="px-4 pt-2 pb-3 space-y-1">
          <router-link
              to="/files"
              class="flex items-center text-gray-600 hover:text-gray-900 px-4 py-3 rounded-lg text-sm font-medium transition-colors duration-200 block"
              :class="{ 'text-gray-900 bg-gray-100': $route.path === '/files' }"
              @click="closeMobileMenu"
          >
            <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8 5a2 2 0 012-2h4a2 2 0 012 2v4H8V5z"></path>
            </svg>
            文件管理
          </router-link>
          <router-link
              to="/knowledge"
              class="flex items-center text-gray-600 hover:text-gray-900 px-4 py-3 rounded-lg text-sm font-medium transition-colors duration-200 block"
              :class="{ 'text-gray-900 bg-gray-100': $route.path === '/knowledge' }"
              @click="closeMobileMenu"
          >
            <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 011-1h6a1 1 0 011 1v2M7 7h10"/>
            </svg>
            知识库
          </router-link>
          <router-link
              to="/chat"
              class="flex items-center text-gray-600 hover:text-gray-900 px-4 py-3 rounded-lg text-sm font-medium transition-colors duration-200 block"
              :class="{ 'text-gray-900 bg-gray-100': $route.path === '/chat' }"
              @click="closeMobileMenu"
          >
            <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
            </svg>
            AI 对话
          </router-link>
        </div>
      </div>
    </nav>

    <!-- 主要内容区域 -->
    <main class="flex-1 min-h-0 overflow-hidden">
      <router-view/>
    </main>
  </div>
</template>

<script setup lang="ts">
import {onMounted, ref} from 'vue'
import {useRouter} from 'vue-router'
import {logoutApi} from '@/api/auth'

const router = useRouter()
const showMobileMenu = ref(false)
const username = ref('')


onMounted(() => {
  // 获取用户名
  username.value = localStorage.getItem('username') || ''
})

const handleLogout = async () => {
  try {
    await logoutApi()
  } catch (error) {
    console.error('登出失败:', error)
    // 即使API调用失败，也清除本地状态
  } finally {
    // 清除本地存储
    localStorage.removeItem('isAuthenticated')
    localStorage.removeItem('username')
    localStorage.removeItem('userInfo')
    localStorage.removeItem('authToken')

    // 跳转到登录页面
    await router.push('/login')
  }
}

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const closeMobileMenu = () => {
  showMobileMenu.value = false
}
</script> 