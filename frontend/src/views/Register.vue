<template>
  <div class="h-screen bg-gray-50 flex items-center justify-center overflow-hidden">
    <div class="max-w-md w-full px-6">
      <div class="text-center mb-6">
        <div class="flex justify-center mb-4">
          <div class="w-12 h-12 bg-gray-900 rounded-xl flex items-center justify-center shadow-lg">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
        </div>
        <h2 class="text-2xl font-medium text-gray-900 mb-1">创建账号</h2>
        <p class="text-sm text-gray-500">加入 AI知识库管理分析平台</p>
      </div>

      <div class="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div class="p-6">
          <a-form
            :model="formState"
            :rules="rules"
            ref="formRef"
            layout="vertical"
            @finish="handleRegister"
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

            <a-form-item name="email" label="邮箱地址">
              <a-input
                v-model:value="formState.email"
                placeholder="请输入邮箱地址（可选）"
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

            <a-form-item name="confirmPassword" label="确认密码">
              <a-input-password
                v-model:value="formState.confirmPassword"
                placeholder="请再次输入密码"
                size="large"
              />
            </a-form-item>

            <a-form-item name="agreeTerms" :rules="[{ validator: validateAgreeTerms }]" value-prop-name="checked">
              <a-checkbox v-model:checked="formState.agreeTerms">
                <span class="text-xs text-gray-600">
                  我已阅读并同意
                  <a class="font-medium text-gray-900 hover:text-gray-700">服务条款</a>
                  和
                  <a class="font-medium text-gray-900 hover:text-gray-700">隐私政策</a>
                </span>
              </a-checkbox>
            </a-form-item>

            <div v-if="errorMessage" class="bg-red-50 border border-red-200 rounded-lg p-2.5 mb-4">
              <p class="text-red-600 text-xs">{{ errorMessage }}</p>
            </div>

            <div v-if="successMessage" class="bg-green-50 border border-green-200 rounded-lg p-2.5 mb-4">
              <p class="text-green-600 text-xs">{{ successMessage }}</p>
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
                创建账号
              </a-button>
            </a-form-item>
          </a-form>
        </div>

        <div class="px-6 py-4 bg-gray-50 border-t border-gray-200">
          <div class="text-center">
            <span class="text-xs text-gray-500">已有账号？</span>
            <router-link
              to="/login"
              class="text-xs font-medium text-gray-900 hover:text-gray-700 ml-1 transition-colors"
            >
              立即登录
            </router-link>
          </div>
        </div>
      </div>

      <div class="text-center mt-4">
        <p class="text-xs text-gray-400">© 2026 AI知识库管理分析平台</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { registerApi } from '@/api/auth'
import type { FormInstance, Rule } from 'ant-design-vue/es/form'

const router = useRouter()
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const formRef = ref<FormInstance>()

const formState = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false
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
  if (!/^[a-zA-Z0-9_\u4e00-\u9fa5]+$/.test(value)) {
    throw new Error('用户名只能包含字母、数字、下划线和中文')
  }
}

const validateEmail = async (_rule: Rule, value: string) => {
  if (!value) return
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
    throw new Error('请输入有效的邮箱地址')
  }
}

const validatePassword = async (_rule: Rule, value: string) => {
  if (!value) {
    throw new Error('请输入密码')
  }
  if (value.length < 6) {
    throw new Error('密码至少6位')
  }
  if (value.length > 100) {
    throw new Error('密码不能超过100个字符')
  }
}

const validateConfirmPassword = async (_rule: Rule, value: string) => {
  if (!value) {
    throw new Error('请再次输入密码')
  }
  if (value !== formState.password) {
    throw new Error('两次输入的密码不一致')
  }
}

const validateAgreeTerms = async (_rule: Rule, value: boolean) => {
  if (!value) {
    throw new Error('请同意服务条款和隐私政策')
  }
}

const rules: Record<string, Rule[]> = {
  username: [
    { required: true, validator: validateUsername, trigger: ['change', 'blur'] }
  ],
  email: [
    { validator: validateEmail, trigger: ['change', 'blur'] }
  ],
  password: [
    { required: true, validator: validatePassword, trigger: ['change', 'blur'] }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: ['change', 'blur'] }
  ]
}

const handleRegister = async () => {
  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    await registerApi({
      username: formState.username,
      password: formState.password,
      email: formState.email || undefined,
    })

    successMessage.value = '注册成功！正在跳转到登录页面...'
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
