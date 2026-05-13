<template>
  <div class="space-y-6">
    <!-- 知识库选择区域 -->
    <div class="bg-white border border-gray-200 rounded-xl p-6 shadow-sm">
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-gray-900 rounded-lg flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-medium text-gray-900">选择知识库</h3>
            <p class="text-sm text-gray-500">选择文件上传的目标知识库</p>
          </div>
        </div>

        <!-- 快捷操作 -->
        <div class="flex items-center space-x-2">
          <button
              @click="loadKnowledgeBases"
              class="text-gray-600 hover:text-gray-900 p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200"
              title="刷新知识库列表"
          >
            <svg class="w-4 h-4" :class="{ 'loading-spinner': isLoadingKnowledgeBases }" fill="none" stroke="currentColor"
                 viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
          </button>
          <router-link
              v-if="knowledgeBases.length === 0"
              to="/knowledge"
              class="text-gray-600 hover:text-gray-900 p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200"
              title="创建新知识库"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
          </router-link>
        </div>
      </div>

      <!-- 知识库选择器 -->
      <div class="relative">
        <select
            v-model="selectedKnowledgeBase"
            :disabled="isLoadingKnowledgeBases"
            class="w-full px-3 py-2.5 bg-gray-50 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-transparent transition-all duration-200 disabled:bg-gray-100 disabled:cursor-not-allowed"
            :class="{
            'border-red-300 bg-red-50': !selectedKnowledgeBase && knowledgeBases.length > 0,
            'border-gray-900 bg-white': selectedKnowledgeBase
          }"
        >
          <option value="" disabled>
            {{ isLoadingKnowledgeBases ? '加载中...' : (knowledgeBases.length === 0 ? '暂无可用知识库' : '请选择知识库') }}
          </option>
          <option
              v-for="kb in knowledgeBases"
              :key="kb.id"
              :value="kb.id"
          >
            {{ kb.name }}
          </option>
        </select>
        <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
          <svg
              v-if="isLoadingKnowledgeBases"
              class="w-4 h-4 text-gray-400 loading-spinner"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          <svg v-else class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
          </svg>
        </div>
      </div>

      <!-- 状态提示 -->
      <div v-if="knowledgeBases.length === 0" class="mt-2 text-xs text-red-600 flex items-center">
        <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M12 3v.01"/>
        </svg>
        暂无知识库，请先创建
      </div>
      <div v-else-if="selectedKnowledgeBase" class="mt-2 text-xs text-gray-600 flex items-center">
        <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
        </svg>
        已选择：{{ knowledgeBases.find(kb => kb.id === selectedKnowledgeBase)?.name }}
      </div>
    </div>

    <!-- 文件上传区域 -->
    <div class="space-y-4">
      <div
          ref="dropZone"
          class="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center transition-all duration-300 hover:border-gray-400 hover:bg-gray-50/30 relative overflow-hidden cursor-pointer bg-white"
          :class="{
          'border-gray-900 bg-gray-100/50 shadow-lg transform scale-[1.01]': isDragOver,
          'border-gray-400 bg-gray-50/50 shadow-md': files.length > 0 && !isDragOver
        }"
          @drop="handleDrop"
          @dragover="handleDragOver"
          @dragenter="handleDragEnter"
          @dragleave="handleDragLeave"
          @click="triggerFileInput"
      >
        <!-- 装饰背景 -->
        <div class="absolute inset-0 opacity-5">
          <div class="absolute top-4 left-4 w-8 h-8 bg-gray-400 rounded-full"></div>
          <div class="absolute bottom-4 right-4 w-6 h-6 bg-gray-500 rounded-full"></div>
        </div>

        <!-- 上传图标和文字 -->
        <div class="space-y-3 relative z-10">
          <div class="mx-auto w-12 h-12 transition-all duration-300"
               :class="isDragOver ? 'text-gray-900 animate-pulse scale-110' : 'text-gray-400'">
            <svg fill="none" stroke="currentColor" viewBox="0 0 48 48" aria-hidden="true">
              <path
                  d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                  stroke-width="1.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
              />
            </svg>
          </div>
          <div>
            <p class="text-base font-medium mb-2" :class="isDragOver ? 'text-gray-900' : 'text-gray-900'">
              <span v-if="isDragOver" class="animate-pulse">释放以添加文件</span>
              <span v-else>
                拖拽文件到此处或
                <button
                    type="button"
                    class="text-gray-900 hover:text-gray-700 font-semibold transition-colors duration-200 underline underline-offset-2"
                    @click.stop="triggerFileInput"
                >
                  点击选择
                </button>
              </span>
            </p>
            <div class="flex items-center justify-center space-x-4 text-sm text-gray-500">
              <div class="flex items-center space-x-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <span>多文件上传</span>
              </div>
              <div class="w-px h-4 bg-gray-300"></div>
              <div class="flex items-center space-x-1">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <span>最大100MB</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 隐藏的文件输入 -->
        <input
            ref="fileInput"
            type="file"
            multiple
            class="hidden"
            @change="handleFileSelect"
        />
      </div>

      <!-- 操作按钮区域 -->
      <div class="flex justify-center space-x-3">
        <button
            @click="triggerFileInput"
            class="bg-gray-900 hover:bg-gray-800 text-white px-6 py-2.5 rounded-lg font-medium transition-all duration-200 flex items-center space-x-2 shadow-sm hover:shadow-md"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
          </svg>
          <span>选择文件</span>
        </button>

        <button
            v-if="files.length > 0"
            @click="uploadAllFiles"
            :disabled="isUploading || !selectedKnowledgeBase"
            class="bg-gray-900 hover:bg-gray-800 disabled:bg-gray-400 text-white px-6 py-2.5 rounded-lg font-medium transition-all duration-200 flex items-center space-x-2 shadow-sm hover:shadow-md disabled:cursor-not-allowed disabled:hover:shadow-sm"
            :title="!selectedKnowledgeBase ? '请先选择知识库' : ''"
        >
          <svg
              v-if="isUploading"
              class="w-4 h-4 loading-spinner"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
          </svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
          </svg>
          <span>{{ isUploading ? '上传中...' : `上传全部 (${files.length})` }}</span>
        </button>

        <button
            v-if="files.length > 0"
            @click="clearFiles"
            class="bg-white hover:bg-gray-50 text-gray-700 border border-gray-200 px-6 py-2.5 rounded-lg font-medium transition-all duration-200 flex items-center space-x-2 shadow-sm hover:shadow-md"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
          </svg>
          <span>清空</span>
        </button>
      </div>
    </div>

    <!-- 文件列表 -->
    <div v-if="files.length > 0" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-gray-900 rounded-lg flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
          </div>
          <div>
            <h2 class="text-lg font-medium text-gray-900">待上传文件</h2>
            <p class="text-sm text-gray-500">共 {{ files.length }} 个文件等待上传</p>
          </div>
        </div>
        <div class="flex items-center space-x-2">
          <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
            {{ files.filter(f => f.status === 'pending').length }} 待处理
          </span>
          <span v-if="files.filter(f => f.status === 'success').length > 0"
                class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-700">
            {{ files.filter(f => f.status === 'success').length }} 已完成
          </span>
        </div>
      </div>

      <div class="space-y-3">
        <div
            v-for="file in files"
            :key="file.id"
            class="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200 hover:shadow-sm transition-all duration-200"
        >
          <div class="flex items-center space-x-4 flex-1">
            <!-- 文件图标 -->
            <div class="flex-shrink-0">
              <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
              </div>
            </div>

            <!-- 文件信息 -->
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">{{ file.name }}</p>
              <p class="text-sm text-gray-500">{{ formatFileSize(file.size) }}</p>
            </div>

            <!-- 进度条 -->
            <div v-if="file.status === 'uploading'" class="flex-1 max-w-32">
              <div class="bg-gray-200 rounded-full h-2">
                <div
                    class="bg-gray-900 h-2 rounded-full transition-all duration-300"
                    :style="{ width: `${file.progress}%` }"
                ></div>
              </div>
              <p class="text-xs text-gray-500 mt-1">{{ file.progress }}%</p>
            </div>

            <!-- 状态图标 -->
            <div class="flex-shrink-0">
              <div v-if="file.status === 'success'" class="text-green-500">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
              <div v-else-if="file.status === 'error'" class="text-red-500">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                </svg>
              </div>
              <div v-else-if="file.status === 'uploading'" class="text-gray-600">
                <svg class="w-6 h-6 loading-spinner" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
              </div>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div class="flex items-center space-x-2 ml-4">
            <button
                v-if="file.status === 'pending'"
                @click="uploadSingleFile(file)"
                :disabled="isUploading || !selectedKnowledgeBase"
                class="text-gray-600 hover:text-gray-900 disabled:text-gray-400 p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
                :title="!selectedKnowledgeBase ? '请先选择知识库' : '上传'"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
              </svg>
            </button>

            <button
                @click="removeFile(file.id)"
                :disabled="file.status === 'uploading'"
                class="text-gray-600 hover:text-gray-900 disabled:text-gray-400 p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
                title="删除"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 内嵌消息提示 -->
    <Transition name="message-slide">
      <div
          v-if="message.text"
          class="mt-4 p-4 rounded-xl border transition-all duration-300"
          :class="{
            'bg-green-50 border-green-200 text-green-800': message.type === 'success',
            'bg-red-50 border-red-200 text-red-800': message.type === 'error',
            'bg-blue-50 border-blue-200 text-blue-800': message.type === 'info'
          }"
      >
        <div class="flex items-center space-x-3">
          <div 
            class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center"
            :class="{
              'bg-green-100': message.type === 'success',
              'bg-red-100': message.type === 'error',
              'bg-blue-100': message.type === 'info'
            }"
          >
            <svg
                v-if="message.type === 'success'"
                class="w-5 h-5 text-green-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            <svg
                v-else-if="message.type === 'error'"
                class="w-5 h-5 text-red-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
            <svg
                v-else
                class="w-5 h-5 text-blue-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div class="flex-1">
            <p class="text-sm font-medium">{{ message.text }}</p>
          </div>
          <button
            @click="message.text = ''"
            class="flex-shrink-0 text-gray-400 hover:text-gray-600 transition-colors duration-200"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
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

    // 调试日志
    console.log('API响应:', response)

    // 检查响应格式并获取知识库数据
    if (response.success && response.data) {
      knowledgeBases.value = response.data.knowledge_bases || []
    } else {
      knowledgeBases.value = []
      console.warn('知识库数据格式异常:', response)
    }

    // 自动选择最后选择的知识库，如果没有则选择第一个
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