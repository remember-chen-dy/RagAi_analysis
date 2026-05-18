<template>
  <div class="space-y-2">
    <!-- 知识库选择区域 -->
    <div class="bg-white border border-gray-200 rounded-lg p-3 shadow-sm">
      <div class="flex items-center justify-between mb-2">
        <div class="flex items-center space-x-2">
          <div class="w-6 h-6 bg-gray-900 rounded flex items-center justify-center">
            <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
            </svg>
          </div>
          <div>
            <h3 class="text-xs font-medium text-gray-900">知识库</h3>
            <p class="text-xs text-gray-400">选择上传目标</p>
          </div>
        </div>

        <button
            @click="loadKnowledgeBases"
            class="text-gray-400 hover:text-gray-900 p-1 rounded hover:bg-gray-100"
            title="刷新"
        >
          <svg class="w-3.5 h-3.5" :class="{ 'loading-spinner': isLoadingKnowledgeBases }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
        </button>
      </div>

      <select
          v-model="selectedKnowledgeBase"
          :disabled="isLoadingKnowledgeBases"
          class="w-full px-2 py-1.5 bg-gray-50 border border-gray-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-gray-500"
      >
        <option value="" disabled>
          {{ isLoadingKnowledgeBases ? '加载中...' : (knowledgeBases.length === 0 ? '暂无知识库' : '请选择') }}
        </option>
        <option v-for="kb in knowledgeBases" :key="kb.id" :value="kb.id">{{ kb.name }}</option>
      </select>
    </div>

    <!-- 文件上传区域 -->
    <div
        ref="dropZone"
        class="border-2 border-dashed border-gray-300 rounded-lg p-3 text-center transition-all cursor-pointer bg-white hover:bg-gray-50"
        :class="{ 'border-gray-900 bg-gray-50': isDragOver }"
        @drop="handleDrop"
        @dragover="handleDragOver"
        @dragenter="handleDragEnter"
        @dragleave="handleDragLeave"
        @click="triggerFileInput"
    >
      <input ref="fileInput" type="file" multiple class="hidden" @change="handleFileSelect" />
      <div class="flex flex-col items-center gap-1">
        <svg class="w-6 h-6 text-gray-400" :class="{ 'animate-pulse text-gray-900': isDragOver }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
        </svg>
        <p class="text-xs text-gray-700">
          <span v-if="isDragOver" class="text-gray-900 font-medium">释放添加</span>
          <span v-else>拖拽或<span class="text-gray-900 font-medium underline cursor-pointer" @click.stop="triggerFileInput">点击选择</span></span>
        </p>
        <p class="text-xs text-gray-400">多文件 · 最大15MB</p>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="flex gap-2">
      <button
          @click="triggerFileInput"
          class="flex-1 bg-gray-900 hover:bg-gray-800 text-white px-3 py-1.5 rounded text-xs font-medium flex items-center justify-center gap-1"
      >
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        <span>选择</span>
      </button>
      <button
          v-if="files.length > 0"
          @click="uploadAllFiles"
          :disabled="isUploading || !selectedKnowledgeBase"
          class="flex-1 bg-gray-900 hover:bg-gray-800 disabled:bg-gray-400 text-white px-3 py-1.5 rounded text-xs font-medium flex items-center justify-center gap-1"
      >
        <svg class="w-3 h-3" :class="{ 'loading-spinner': isUploading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
        </svg>
        <span>{{ isUploading ? '上传中' : `上传 (${files.length})` }}</span>
      </button>
      <button v-if="files.length > 0" @click="clearFiles" class="bg-white border border-gray-200 hover:bg-gray-50 text-gray-700 px-3 py-1.5 rounded text-xs font-medium">
        清空
      </button>
    </div>

    <!-- 文件列表 -->
    <div v-if="files.length > 0" class="bg-white rounded-lg shadow-sm border border-gray-200 p-3">
      <div class="flex items-center justify-between mb-2">
        <h2 class="text-xs font-medium text-gray-900">待上传 ({{ files.length }})</h2>
        <span class="text-xs text-gray-400">{{ files.filter(f => f.status === 'success').length }} 完成</span>
      </div>
      <div class="space-y-1.5 max-h-40 overflow-y-auto">
        <div
            v-for="file in files"
            :key="file.id"
            class="flex items-center justify-between p-2 bg-gray-50 rounded border border-gray-100"
        >
          <div class="flex items-center gap-2 flex-1 min-w-0">
            <svg class="w-3.5 h-3.5 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <div class="min-w-0 flex-1">
              <p class="text-xs font-medium text-gray-900 truncate">{{ file.name }}</p>
              <p class="text-xs text-gray-400">{{ formatFileSize(file.size) }}</p>
            </div>
          </div>
          <div class="flex items-center gap-1 ml-2">
            <div v-if="file.status === 'success'" class="text-green-500">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
            </div>
            <div v-else-if="file.status === 'error'" class="text-red-500">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
            </div>
            <div v-else-if="file.status === 'uploading'" class="text-gray-400">
              <svg class="w-4 h-4 loading-spinner" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
            </div>
            <button
                v-if="file.status !== 'uploading'"
                @click="removeFile(file.id)"
                class="text-gray-400 hover:text-red-500 p-0.5"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 内嵌消息提示 -->
    <Transition name="message-slide">
      <div v-if="message.text" class="p-2 rounded text-xs" :class="{
        'bg-green-50 text-green-800': message.type === 'success',
        'bg-red-50 text-red-800': message.type === 'error',
        'bg-blue-50 text-blue-800': message.type === 'info'
      }">
        {{ message.text }}
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import {onMounted, reactive, ref, watch} from 'vue'
import type {FileInfo, UploadFile} from '../types'
import { UploadAPI } from '../api/upload'

// 定义 emits
const emit = defineEmits<{
  'files-updated': [files: FileInfo[]]
}>()

// 响应式数据
const files = ref<UploadFile[]>([])
const isDragOver = ref(false)
const isUploading = ref(false)

// 知识库相关
const knowledgeBases = ref<any[]>([])
const selectedKnowledgeBase = ref<string>('')
const isLoadingKnowledgeBases = ref(false)

// DOM 引用
const dropZone = ref<HTMLElement>()
const fileInput = ref<HTMLInputElement>()

// 消息提示
const message = reactive({
  text: '',
  type: 'info' as 'success' | 'error' | 'info'
})

// 工具函数
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const generateFileId = (): string => {
  return Date.now() + '_' + Math.random().toString(36).substr(2, 9)
}

const showMessage = (text: string, type: 'success' | 'error' | 'info' = 'info') => {
  message.text = text
  message.type = type
  
  // 根据消息类型设置不同的显示时长
  const duration = type === 'success' ? 4000 : type === 'error' ? 5000 : 3000
  
  setTimeout(() => {
    message.text = ''
  }, duration)
}

// 知识库相关函数
const loadKnowledgeBases = async () => {
  try {
    isLoadingKnowledgeBases.value = true
    const response = await UploadAPI.getKnowledgeBases()

    if (response.success && response.data) {
      knowledgeBases.value = response.data
    } else {
      knowledgeBases.value = []
    }

    if (knowledgeBases.value.length > 0 && !selectedKnowledgeBase.value) {
      const lastSelectedId = localStorage.getItem('lastSelectedKnowledgeBase')

      if (lastSelectedId) {
        // 查找最后选择的知识库
        const targetKnowledgeBase = knowledgeBases.value.find(kb => kb.id === lastSelectedId)
        if (targetKnowledgeBase) {
          selectedKnowledgeBase.value = lastSelectedId
        } else {
          // 如果最后选择的知识库不存在了，选择第一个
          selectedKnowledgeBase.value = knowledgeBases.value[0].id
        }
      } else {
        // 如果没有记录，选择第一个
        selectedKnowledgeBase.value = knowledgeBases.value[0].id
      }
    }

    console.log('加载到的知识库:', knowledgeBases.value)
  } catch (error) {
    console.error('加载知识库失败:', error)
    knowledgeBases.value = []
    showMessage(`加载知识库失败: ${error instanceof Error ? error.message : '未知错误'}`, 'error')
  } finally {
    isLoadingKnowledgeBases.value = false
  }
}

// 文件操作函数
const triggerFileInput = () => {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    addFiles(Array.from(target.files))
  }
  // 清空 input 的值，确保可以重复选择相同文件
  target.value = ''
}

const addFiles = (newFiles: File[]) => {
  for (const file of newFiles) {
    if (file.size > 100 * 1024 * 1024) { // 100MB 限制
      showMessage(`文件 ${file.name} 超过大小限制（100MB）`, 'error')
      continue
    }

    const uploadFile: UploadFile = {
      id: generateFileId(),
      name: file.name,
      size: file.size,
      type: file.type,
      file: file,
      status: 'pending',
      progress: 0
    }

    files.value.push(uploadFile)
  }

  if (newFiles.length > 0) {
    showMessage(`成功添加 ${newFiles.length} 个文件，准备上传`, 'success')
  }
}

const removeFile = (fileId: string) => {
  const index = files.value.findIndex(f => f.id === fileId)
  if (index > -1) {
    files.value.splice(index, 1)
  }
}

const clearFiles = () => {
  files.value = []
  // 清空 input 的值，确保清空后可以重新选择文件
  if (fileInput.value) {
    fileInput.value.value = ''
  }
  // 清空操作不需要显示消息，用户已经通过UI得到反馈
}

// 拖拽相关函数
const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
}

const handleDragEnter = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
  isDragOver.value = true
}

const handleDragLeave = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
  if (e.target === dropZone.value) {
    isDragOver.value = false
  }
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  e.stopPropagation()
  isDragOver.value = false

  const droppedFiles = e.dataTransfer?.files
  if (droppedFiles) {
    addFiles(Array.from(droppedFiles))
  }
}

// 上传函数
const uploadSingleFile = async (file: UploadFile) => {
  if (!selectedKnowledgeBase.value) {
    showMessage('请先选择知识库', 'error')
    return
  }

  try {
    file.status = 'uploading'
    file.progress = 0

    // 调用实际的上传API
    const response = await UploadAPI.uploadFile(
      file.file,
      (progress) => {
        file.progress = progress
      },
      selectedKnowledgeBase.value
    )

    if (response.success) {
      file.status = 'success'
      file.progress = 100
      showMessage(`文件 "${file.name}" 上传成功并已加入知识库`, 'success')

      // 通知父组件文件已更新
      emit('files-updated', [])
    } else {
      throw new Error(response.message || '上传失败')
    }

  } catch (error) {
    file.status = 'error'
    console.error('上传失败:', error)
    const errorMessage = error instanceof Error ? error.message : '上传失败'
    showMessage(`文件 ${file.name} 上传失败: ${errorMessage}`, 'error')
  }
}

const uploadAllFiles = async () => {
  if (!selectedKnowledgeBase.value) {
    showMessage('请先选择知识库', 'error')
    return
  }

  const pendingFiles = files.value.filter(f => f.status === 'pending')
  if (pendingFiles.length === 0) {
    showMessage('没有需要上传的文件', 'info')
    return
  }

  isUploading.value = true

  for (const file of pendingFiles) {
    await uploadSingleFile(file)
  }

  isUploading.value = false
  showMessage(`批量上传完成！共上传 ${pendingFiles.length} 个文件到知识库`, 'success')
}

// 监听知识库选择变化
watch(selectedKnowledgeBase, (newValue) => {
  if (newValue) {
    localStorage.setItem('lastSelectedKnowledgeBase', newValue)
  }
})

// 生命周期
onMounted(() => {
  loadKnowledgeBases()
})

// 暴露给父组件的方法
defineExpose({
  loadKnowledgeBases,
  clearFiles
})
</script>

<style scoped>


/* 加载动画 */
.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 弹跳动画 */
@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
    animation-timing-function: cubic-bezier(0.8, 0, 1, 1);
  }
  50% {
    transform: translateY(-25%);
    animation-timing-function: cubic-bezier(0, 0, 0.2, 1);
  }
}


/* 脉冲动画增强 */
.animate-pulse {
  animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.1;
    transform: scale(1);
  }
  50% {
    opacity: 0.3;
    transform: scale(1.05);
  }
}

</style> 