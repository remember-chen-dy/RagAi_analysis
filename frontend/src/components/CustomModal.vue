<template>
  <div
    v-if="isVisible"
    class="fixed inset-0 z-50 flex items-center justify-center"
    @click.self="handleBackdropClick"
  >
    <!-- 背景遮罩 -->
    <div class="absolute inset-0 bg-black bg-opacity-50 transition-opacity duration-300" />
    
    <!-- 弹窗内容 -->
    <div class="relative bg-white rounded-lg shadow-xl max-w-md w-full mx-4 transform transition-all duration-300 scale-100">
      <!-- 头部 -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <h3 class="text-lg font-medium text-gray-900">{{ title }}</h3>
        <button
          @click="handleClose"
          class="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <!-- 内容区域 -->
      <div class="p-6">
        <div class="flex items-start space-x-3">
          <!-- 图标 -->
          <div class="flex-shrink-0">
            <div
              class="w-10 h-10 rounded-full flex items-center justify-center"
              :class="iconClasses"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="iconPath" />
              </svg>
            </div>
          </div>
          
          <!-- 消息内容 -->
          <div class="flex-1">
            <p class="text-sm text-gray-600 leading-relaxed">{{ message }}</p>
          </div>
        </div>
      </div>
      
      <!-- 底部按钮 -->
      <div class="flex justify-end space-x-3 p-6 border-t border-gray-200 bg-gray-50">
        <button
          v-if="type === 'confirm'"
          @click="handleCancel"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
        >
          {{ cancelText }}
        </button>
        <button
          @click="handleConfirm"
          class="px-4 py-2 text-sm font-medium text-white rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors"
          :class="confirmButtonClasses"
        >
          {{ confirmText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, watch } from 'vue'

interface Props {
  isVisible: boolean
  type: 'alert' | 'confirm' | 'success' | 'error' | 'warning'
  title: string
  message: string
  confirmText?: string
  cancelText?: string
  allowBackdropClose?: boolean
}

interface Emits {
  (e: 'update:isVisible', value: boolean): void
  (e: 'confirm'): void
  (e: 'cancel'): void
}

const props = withDefaults(defineProps<Props>(), {
  confirmText: '确定',
  cancelText: '取消',
  allowBackdropClose: true
})

const emit = defineEmits<Emits>()

// 图标配置
const iconConfig = computed(() => {
  switch (props.type) {
    case 'success':
      return {
        path: 'M5 13l4 4L19 7',
        classes: 'bg-green-100 text-green-600'
      }
    case 'error':
      return {
        path: 'M6 18L18 6M6 6l12 12',
        classes: 'bg-red-100 text-red-600'
      }
    case 'warning':
      return {
        path: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L5.268 16.5c-.77.833.192 2.5 1.732 2.5z',
        classes: 'bg-yellow-100 text-yellow-600'
      }
    case 'confirm':
      return {
        path: 'M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
        classes: 'bg-blue-100 text-blue-600'
      }
    default:
      return {
        path: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
        classes: 'bg-gray-100 text-gray-600'
      }
  }
})

const iconPath = computed(() => iconConfig.value.path)
const iconClasses = computed(() => iconConfig.value.classes)

// 确认按钮样式
const confirmButtonClasses = computed(() => {
  switch (props.type) {
    case 'success':
      return 'bg-green-600 hover:bg-green-700 focus:ring-green-500'
    case 'error':
      return 'bg-red-600 hover:bg-red-700 focus:ring-red-500'
    case 'warning':
      return 'bg-yellow-600 hover:bg-yellow-700 focus:ring-yellow-500'
    default:
      return 'bg-gray-900 hover:bg-gray-800 focus:ring-gray-500'
  }
})

const handleConfirm = () => {
  emit('confirm')
  emit('update:isVisible', false)
}

const handleCancel = () => {
  emit('cancel')
  emit('update:isVisible', false)
}

const handleClose = () => {
  emit('update:isVisible', false)
}

const handleBackdropClick = () => {
  if (props.allowBackdropClose) {
    emit('update:isVisible', false)
  }
}

// 监听键盘事件
watch(() => props.isVisible, (visible) => {
  if (visible) {
    nextTick(() => {
      const handleKeydown = (e: KeyboardEvent) => {
        if (e.key === 'Escape' && props.allowBackdropClose) {
          emit('update:isVisible', false)
        } else if (e.key === 'Enter') {
          handleConfirm()
        }
      }
      
      document.addEventListener('keydown', handleKeydown)
      
      // 清理事件监听器
      return () => {
        document.removeEventListener('keydown', handleKeydown)
      }
    })
  }
})
</script>

<style scoped>
/* 进入和离开动画 */
.v-enter-active,
.v-leave-active {
  transition: all 0.3s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
  transform: scale(0.9);
}
</style> 