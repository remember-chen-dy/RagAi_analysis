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
              <router-link
                  to="/evaluation"
                  class="flex items-center text-gray-600 hover:text-gray-900 px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-200"
                  :class="{ 'text-gray-900 bg-gray-100': $route.path === '/evaluation' }"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                </svg>
                RAG 评估
              </router-link>
            </div>
          </div>

          <!-- 右侧操作区域 -->
          <div class="hidden md:flex items-center space-x-4">
            <!-- 用户下拉菜单 -->
            <div class="relative" ref="userMenuRef">
              <button
                  @click="toggleUserMenu"
                  class="flex items-center space-x-2 text-gray-600 hover:text-gray-900 p-2 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div class="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                  <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                  </svg>
                </div>
                <span class="text-sm">{{ username }}</span>
                <svg class="w-4 h-4" :class="{ 'rotate-180': showUserMenu }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                </svg>
              </button>

              <!-- 下拉菜单 -->
              <div
                  v-if="showUserMenu"
                  class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-100 py-1 z-50"
              >
                <!-- <button
                    @click="handleSettings"
                    class="w-full flex items-center px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  <svg class="w-4 h-4 mr-3 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.065 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.065c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.065-2.573c-.94-1.543.826-3.31 2.37-2.37.996.458 1.876.99 2.572 1.065.426.122.84.316 1.065.572.225.256.426.572.572.99.146.418.316.84.572 1.065.256.225.572.426.99.572.418.146.84.316 1.065.572z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                  </svg>
                  设置
                </button> -->
                <div class="border-t border-gray-100 my-1"></div>
                <button
                    @click="handleLogout"
                    class="w-full flex items-center px-4 py-2.5 text-sm text-red-600 hover:bg-red-50 transition-colors"
                >
                  <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                  </svg>
                  退出登录
                </button>
              </div>
            </div>
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
          <router-link
              to="/evaluation"
              class="flex items-center text-gray-600 hover:text-gray-900 px-4 py-3 rounded-lg text-sm font-medium transition-colors duration-200 block"
              :class="{ 'text-gray-900 bg-gray-100': $route.path === '/evaluation' }"
              @click="closeMobileMenu"
          >
            <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
            </svg>
            RAG 评估
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
import {onMounted, onUnmounted, ref} from 'vue'
import {useRouter} from 'vue-router'
import {logoutApi} from '@/api/auth'
import {Modal} from 'ant-design-vue'

const router = useRouter()
const showMobileMenu = ref(false)
const showUserMenu = ref(false)
const username = ref('')
const userMenuRef = ref<HTMLElement | null>(null)

onMounted(() => {
  username.value = localStorage.getItem('username') || ''
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

const handleClickOutside = (event: MouseEvent) => {
  if (userMenuRef.value && !userMenuRef.value.contains(event.target as Node)) {
    showUserMenu.value = false
  }
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const handleSettings = () => {
  showUserMenu.value = false
  router.push('/settings')
}

const handleLogout = () => {
  showUserMenu.value = false
  Modal.confirm({
    title: '确认退出',
    content: '确定要退出登录吗？',
    okText: '确定',
    cancelText: '取消',
    onOk: async () => {
      try {
        await logoutApi()
      } catch (error) {
        console.error('登出失败:', error)
      } finally {
        localStorage.removeItem('isAuthenticated')
        localStorage.removeItem('username')
        localStorage.removeItem('userInfo')
        localStorage.removeItem('authToken')
        await router.push('/login')
      }
    }
  })
}

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const closeMobileMenu = () => {
  showMobileMenu.value = false
}
</script> 