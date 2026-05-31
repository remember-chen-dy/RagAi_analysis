<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div class="text-center">
        <div class="flex justify-center mb-6">
          <div class="w-16 h-16 bg-gray-900 rounded-xl flex items-center justify-center shadow-lg">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
        </div>
        <h2 class="text-3xl font-light text-gray-900 mb-2">欢迎回来</h2>
        <p class="text-gray-500">知识库管理分析平台</p>
      </div>

      <div class="bg-white rounded-xl border border-gray-200 shadow-sm">
        <div class="p-8">
          <a-form
            :model="formState"
            :rules="rules"
            ref="formRef"
            layout="vertical"
            @finish="handleLogin"
            hide-required-mark
          >
            <a-form-item name="username" label="用户名">
              <a-input
                v-model:value="formState.username"
                placeholder="请输入用户名"
                size="large"
                allow-clear
              />
            </a-form-item>

            <a-form-item name="password" label="密码">
              <a-input-password
                v-model:value="formState.password"
                placeholder="请输入密码"
                size="large"
              />
            </a-form-item>

            <div class="flex items-center justify-between mb-4">
              <a-checkbox v-model:checked="formState.rememberMe">记住登录状态</a-checkbox>
              <a class="text-sm text-gray-600 hover:text-gray-900 cursor-pointer">忘记密码？</a>
            </div>

            <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
              <p class="text-red-600 text-sm">{{ errorMessage }}</p>
            </div>

            <a-form-item>
              <a-button
                type="primary"
                html-type="submit"
                :loading="loading"
                :disabled="loading"
                block
                size="large"
                class="!bg-gray-900 !border-gray-900 hover:!bg-gray-800 hover:!border-gray-800"
              >
                {{ loading ? '登录中...' : '登录' }}
              </a-button>
            </a-form-item>
          </a-form>
        </div>

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

      <div class="text-center">
        <p class="text-sm text-gray-400">© 2026 remember - 知识库管理分析平台</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { loginApi } from '@/api/auth'
import { message } from 'ant-design-vue'
import type { FormInstance, Rule } from 'ant-design-vue/es/form'

const router = useRouter()
const loading = ref(false)
const errorMessage = ref('')
const formRef = ref<FormInstance>()

const formState = reactive({
  username: '',
  password: '',
  rememberMe: false
})

const validateUsername = async (_rule: Rule, value: string) => {
  if (!value || !value.trim()) {
    throw new Error('请输入用户名')
  }
  if (value.trim().length < 2) {
    throw new Error('用户名至少2个字符')
  }
  if (value.trim().length > 50) {
    throw new Error('用户名不能超过50个字符')
  }
}

const validatePassword = async (_rule: Rule, value: string) => {
  if (!value) {
    throw new Error('请输入密码')
  }
  if (value.length < 6) {
    throw new Error('密码至少6位')
  }
}

const rules: Record<string, Rule[]> = {
  username: [
    { required: true, validator: validateUsername, trigger: ['change', 'blur'] }
  ],
  password: [
    { required: true, validator: validatePassword, trigger: ['change', 'blur'] }
  ]
}

const handleLogin = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const result = await loginApi({
      username: formState.username,
      password: formState.password,
    })

    if (result.success && result.data?.token) {
      message.success('登录成功')
      await router.push('/files')
    } else {
      errorMessage.value = result.message || '登录失败，请重试'
    }
  } catch (error: any) {
    console.error('登录失败:', error)
    errorMessage.value = error.message || '登录失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>
