<template>
  <div class="flex flex-col h-screen overflow-hidden">
    <!-- 页面头部 -->
    <header class="bg-white border-b border-gray-200 flex-shrink-0">
      <div class="max-w-full mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <!-- 标题区域 -->
          <div>
            <h1 class="text-xl font-medium text-gray-900">文件管理</h1>
            <p class="text-sm text-gray-500">智能文档存储与管理</p>
          </div>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="flex-1 max-h-[calc(100vh-140px)] px-6 py-4 mb-4 overflow-hidden">
      <!-- 横向布局容器 -->
      <div class="grid grid-cols-12 gap-4 h-full">
        
        <!-- 左侧：文件上传区域 -->
        <div class="col-span-3 bg-white rounded-xl border border-gray-200 shadow-sm flex flex-col">
          <!-- 上传区域头部 -->
          <div class="px-4 py-3 border-b border-gray-100 flex-shrink-0">
            <h2 class="text-sm font-medium text-gray-900 mb-2">文件上传</h2>
            <div class="text-xs text-gray-500">
              <div class="flex flex-wrap gap-1">
                <span class="inline-flex items-center px-1.5 py-0.5 rounded text-xs bg-gray-100 text-gray-600">PDF</span>
                <span class="inline-flex items-center px-1.5 py-0.5 rounded text-xs bg-gray-100 text-gray-600">TXT</span>
                <span class="inline-flex items-center px-1.5 py-0.5 rounded text-xs bg-gray-100 text-gray-600">MD</span>
                <span class="inline-flex items-center px-1.5 py-0.5 rounded text-xs bg-gray-100 text-gray-600">DOCX</span>
              </div>
            </div>
          </div>

          <!-- 上传组件区域 -->
          <div class="flex-1 min-h-0 px-4 py-3">
            <FileUpload @files-updated="handleFilesUpdate" ref="fileUploadRef" />
          </div> 

          <!-- 底部操作区域 -->
          <div class="px-4 py-2 border-t border-gray-100 flex-shrink-0">
            <div class="flex items-center justify-between text-xs text-gray-400">
              <span>拖拽文件到此处</span>
              <span>或点击上方区域选择</span>
            </div>
          </div>
        </div>

        <!-- 中间：文件管理区域 -->
        <div class="col-span-6">
          <section class="bg-white rounded-xl border border-gray-200 shadow-sm h-full flex flex-col">
            
            <!-- 文件管理头部 -->
            <div class="px-4 py-3 border-b border-gray-100 flex-shrink-0">
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-2">
                  <div class="w-7 h-7 bg-gray-900 rounded-lg flex items-center justify-center">
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5a2 2 0 00-2-2H9a2 2 0 00-2 2v5a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <div>
                    <h2 class="text-sm font-medium text-gray-900">文件库</h2>
                    <p class="text-xs text-gray-500">管理和浏览已上传的文件</p>
                  </div>
                </div>
                
                <!-- 统计信息和操作 -->
                <div class="flex items-center space-x-4">
                  <!-- 文件统计 -->
                  <div class="flex items-center space-x-3 text-xs">
                    <div class="text-center">
                      <div class="text-base font-medium text-gray-900">{{ uploadedFilesCount }}</div>
                      <div class="text-gray-400 uppercase tracking-wide">文件</div>
                    </div>
                    <div class="text-center">
                      <div class="text-base font-medium text-gray-900">{{ totalStorageSize }}</div>
                      <div class="text-gray-400 uppercase tracking-wide">存储</div>
                    </div>
                  </div>
                  
                  <!-- 刷新按钮 -->
                  <button
                    @click="refreshFiles"
                    :disabled="isLoadingFiles"
                    class="text-gray-500 hover:text-gray-900 disabled:text-gray-300 p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
                    title="刷新列表"
                  >
                    <svg
                      class="w-4 h-4"
                      :class="{ 'loading-spinner': isLoadingFiles }"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- 文件列表内容 -->
            <div class="flex-1 min-h-0 overflow-y-auto px-4 pt-3 pb-6">
              <!-- 加载状态 -->
              <div v-if="isLoadingFiles" class="flex items-center justify-center h-full">
                <div class="inline-flex items-center space-x-2 text-gray-500">
                  <svg class="w-4 h-4 loading-spinner" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  <span class="text-xs">加载中...</span>
                </div>
              </div>

              <!-- 空状态 -->
              <div v-else-if="fileList.length === 0" class="flex flex-col items-center justify-center h-full">
                <div class="w-12 h-12 mb-3 bg-gray-100 rounded-xl flex items-center justify-center">
                  <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <p class="text-gray-500 text-sm font-medium mb-1">暂无上传文件</p>
                <p class="text-gray-400 text-xs">在左侧上传区域添加文件开始使用</p>
              </div>

              <!-- 文件网格 -->
              <div v-else class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
                <div
                  v-for="file in fileList"
                  :key="file.object_name"
                  class="bg-gray-50 rounded-lg border border-gray-200 p-2 hover:shadow-sm hover:bg-white transition-all group flex items-center justify-between"
                >
                  <div class="flex items-center gap-2 flex-1 min-w-0">
                    <svg class="w-4 h-4 text-gray-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getFileIcon(getFileName(file.object_name))" />
                    </svg>
                    <div class="min-w-0 flex-1">
                      <p class="text-xs font-medium text-gray-900 truncate" :title="getFileName(file.object_name)">
                        {{ getFileName(file.object_name) }}
                      </p>
                      <p class="text-xs text-gray-400">{{ formatFileSize(file.size) }}</p>
                    </div>
                  </div>
                  <div class="flex items-center gap-1 ml-2 flex-shrink-0">
                    <span class="inline-flex items-center px-1 py-0.5 rounded text-xs bg-gray-200 text-gray-600">
                      {{ getFileType(getFileName(file.object_name)).toUpperCase() }}
                    </span>
                    <button
                      v-if="UploadAPI.isSupportedForPreview(getFileName(file.object_name))"
                      @click="previewFileContent(file)"
                      class="text-gray-400 hover:text-gray-900 p-0.5 rounded hover:bg-gray-200 transition-colors"
                      title="预览"
                    >
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                    </button>
                    <button
                      @click="downloadFile(file.object_name)"
                      class="text-gray-400 hover:text-gray-900 p-0.5 rounded hover:bg-gray-200 transition-colors"
                      title="下载"
                    >
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-4-4m4 4l4-4m3 8H5a2 2 0 01-2-2V6a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2z" />
                      </svg>
                    </button>
                    <button
                      @click="deleteFile(file.object_name)"
                      class="text-gray-400 hover:text-red-500 p-0.5 rounded hover:bg-red-50 transition-colors"
                      title="删除"
                    >
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- 右侧：使用统计区域 -->
        <div class="col-span-3 bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden flex flex-col">
          <!-- 统计区域头部 -->
          <div class="px-4 py-3 border-b border-gray-100 flex-shrink-0">
            <h2 class="text-sm font-medium text-gray-900 mb-3">使用统计</h2>
            
            <!-- 快速统计卡片 -->
            <div class="grid grid-cols-2 gap-2">
              <div class="bg-gray-50 rounded-lg p-2">
                <p class="text-xs text-gray-500">总文件数</p>
                <p class="text-base font-medium text-gray-900">{{ uploadedFilesCount }}</p>
              </div>
              
              <div class="bg-gray-50 rounded-lg p-2">
                <p class="text-xs text-gray-500">存储大小</p>
                <p class="text-base font-medium text-gray-900">{{ totalStorageSize }}</p>
              </div>
            </div>
          </div>

          <!-- 详细统计内容 -->
          <div class="flex-1 min-h-0 overflow-y-auto px-4 py-3">
            <AnalyticsView />
          </div>

          <!-- 底部操作区域 -->
          <div class="px-4 py-2 border-t border-gray-100 flex-shrink-0">
            <div class="flex items-center justify-between text-xs text-gray-400">
              <span>存储使用情况</span>
              <button
                @click="refreshFiles"
                class="text-gray-500 hover:text-gray-900 transition-colors"
                title="刷新统计"
              >
                刷新
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 文件预览弹窗 -->
    <Transition name="modal">
      <div
        v-if="showPreview && previewFile"
        class="fixed inset-0 flex items-center justify-center z-50 bg-black/40 backdrop-blur-sm"
        @click="closePreview"
      >
        <div
          class="bg-white rounded-2xl shadow-2xl max-w-4xl w-full mx-4 max-h-[90vh] flex flex-col overflow-hidden"
          @click.stop
        >
          <!-- 预览头部 -->
          <div class="flex items-center justify-between p-6 border-b border-gray-100 flex-shrink-0">
            <div>
              <h3 class="text-lg font-medium text-gray-900">{{ getFileName(previewFile.object_name) }}</h3>
              <p class="text-sm text-gray-500 mt-1">{{ formatFileSize(previewFile.size) }} • {{ formatDate(previewFile.last_modified) }}</p>
            </div>
            <button
              @click="closePreview"
              class="text-gray-400 hover:text-gray-600 p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- 预览内容 -->
          <div class="flex-1 min-h-0 overflow-y-auto p-6 modal-scroll">
            <!-- 加载中状态 -->
            <div v-if="isLoadingPreview" class="text-center py-16">
              <div class="inline-flex items-center space-x-3 text-gray-500">
                <svg class="w-5 h-5 loading-spinner" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <span class="text-sm">加载预览中...</span>
              </div>
            </div>

            <!-- 图片预览 -->
            <div v-else-if="getFileType(getFileName(previewFile.object_name)) === 'image'" class="text-center">
              <img
                v-if="previewUrl"
                :src="previewUrl"
                :alt="getFileName(previewFile.object_name)"
                class="max-w-full max-h-96 mx-auto rounded-lg shadow-sm"
                @error="showMessage('图片加载失败', 'error')"
              />
              <div v-else class="text-gray-500 py-8">
                图片加载失败
              </div>
            </div>

            <!-- PDF预览 -->
            <div v-else-if="getFileType(getFileName(previewFile.object_name)) === 'pdf'" class="w-full">
              <iframe
                v-if="previewUrl"
                :src="previewUrl"
                class="w-full h-96 border border-gray-200 rounded-lg"
                title="PDF预览"
              ></iframe>
              <div v-else class="text-center py-8">
                <p class="text-gray-500 mb-4">PDF预览加载失败</p>
                <button
                  @click="downloadFile(previewFile.object_name)"
                  class="bg-gray-900 hover:bg-gray-800 text-white px-4 py-2 rounded-lg"
                >
                  下载PDF文件
                </button>
              </div>
            </div>

            <!-- Markdown 文件预览 -->
            <div v-else-if="isMarkdown" class="bg-white rounded-lg">
              <div v-if="previewContent" class="markdown-body p-4 overflow-auto max-h-96"
                   v-html="previewContent">
              </div>
              <div v-else class="text-center py-8 text-gray-500">
                Markdown 内容加载失败
              </div>
            </div>

            <!-- 文本文件预览 -->
            <div v-else-if="getFileType(getFileName(previewFile.object_name)) === 'text'" class="bg-gray-50 rounded-lg p-4">
              <div v-if="previewContent" class="relative">
                <div class="absolute top-2 right-2 text-xs text-gray-400">Text</div>
                <pre class="text-sm text-gray-800 whitespace-pre-wrap overflow-auto max-h-96 pt-6">{{ previewContent }}</pre>
              </div>
              <div v-else class="text-center py-8 text-gray-500">
                文本内容加载失败
              </div>
            </div>

            <!-- 不支持预览的文件类型 -->
            <div v-else class="text-center py-8">
              <div class="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <p class="text-gray-500 mb-2">不支持预览此文件类型</p>
              <p class="text-sm text-gray-400 mb-4">支持的格式: 图片 (JPG, PNG, GIF, WebP)、PDF、文本文件 (TXT, MD)</p>
              <button
                @click="downloadFile(previewFile.object_name)"
                class="bg-gray-900 hover:bg-gray-800 text-white px-4 py-2 rounded-lg"
              >
                下载文件
              </button>
            </div>
          </div>

          <!-- 预览底部操作 -->
          <div class="p-6 border-t border-gray-100 flex justify-end space-x-3 flex-shrink-0">
            <button
              @click="downloadFile(previewFile.object_name)"
              class="bg-gray-900 hover:bg-gray-800 text-white px-4 py-2 rounded-lg flex items-center space-x-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-4-4m4 4l4-4m3 8H5a2 2 0 01-2-2V6a2 2 0 012-2h6l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2z" />
              </svg>
              <span>下载</span>
            </button>
            <button
              @click="closePreview"
              class="text-gray-600 hover:text-gray-800 px-4 py-2 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
            >
              关闭
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- 消息提示 -->
    <Transition name="message">
      <div
        v-if="message.text"
        class="fixed bottom-4 right-4 max-w-sm p-4 rounded-lg shadow-lg z-50"
        :class="{
          'bg-green-500 text-white': message.type === 'success',
          'bg-red-500 text-white': message.type === 'error',
          'bg-blue-500 text-white': message.type === 'info'
        }"
      >
        <div class="flex items-center space-x-2">
          <svg
            v-if="message.type === 'success'"
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <svg
            v-else-if="message.type === 'error'"
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          <span>{{ message.text }}</span>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import FileUpload from '@/components/FileUpload.vue'
  import AnalyticsView from '@/components/AnalyticsView.vue'
  import UploadAPI from '@/api/upload'
  import { Modal } from 'ant-design-vue'
  import { marked } from 'marked'
  import type { FileInfo } from '@/types'

  // 响应式数据
  const uploadedFilesCount = ref(0)
  const totalStorageSize = ref('0 MB')
  const fileUploadRef = ref()
  const fileList = ref<FileInfo[]>([])
  const isLoadingFiles = ref(false)

  // 预览相关
  const previewFile = ref<FileInfo | null>(null)
  const showPreview = ref(false)
  const previewUrl = ref<string>('')
  const previewContent = ref<string>('')
  const isMarkdown = ref(false)
  const isLoadingPreview = ref(false)

  // 消息提示
  const message = ref({ text: '', type: 'info' })

  // 事件处理
  const handleFilesUpdate = () => {
    refreshFiles()
  }

  // 工具函数
  const showMessage = (text: string, type: 'success' | 'error' | 'info' = 'info') => {
    message.value.text = text
    message.value.type = type
    setTimeout(() => {
      message.value.text = ''
    }, 3000)
  }

  const getFileType = (fileName: string) => {
    const extension = fileName.split('.').pop()?.toLowerCase()
    if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(extension || '')) {
      return 'image'
    } else if (['pdf'].includes(extension || '')) {
      return 'pdf'
    } else if (extension === 'md') {
      return 'md'
    } else if (['txt'].includes(extension || '')) {
      return 'text'
    } else if (['mp4', 'webm', 'ogg'].includes(extension || '')) {
      return 'video'
    } else if (['mp3', 'wav', 'ogg'].includes(extension || '')) {
      return 'audio'
    }
    return 'other'
  }

  const getFileIcon = (fileName: string) => {
    const fileType = getFileType(fileName)
    switch (fileType) {
      case 'image':
        return 'M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z'
      case 'pdf':
        return 'M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z'
      case 'video':
        return 'M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z'
      case 'audio':
        return 'M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2z'
      default:
        return 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z'
    }
  }

  // 预览相关函数
  const previewFileContent = async (file: FileInfo) => {
    const fileName = getFileName(file.object_name)

    if (!UploadAPI.isSupportedForPreview(fileName)) {
      showMessage('不支持预览此文件类型', 'info')
      return
    }

    previewFile.value = file
    showPreview.value = true
    isLoadingPreview.value = true
    previewUrl.value = ''
    previewContent.value = ''
    isMarkdown.value = false

    try {
      const fileType = getFileType(fileName)
      const isMd = fileName.toLowerCase().endsWith('.md')

      switch (fileType) {
        case 'image':
        case 'pdf':
          previewUrl.value = await UploadAPI.getPreviewUrl(file.object_name)
          break

        case 'text':
          {
            const rawText = await UploadAPI.getTextContent(file.object_name)
            if (isMd) {
              previewContent.value = await marked.parse(rawText)
              isMarkdown.value = true
            } else {
              previewContent.value = rawText
            }
          }
          break

        default:
          throw new Error('不支持预览此文件类型')
      }
    } catch (error) {
      console.error('预览加载失败:', error)
      showMessage(error instanceof Error ? error.message : '预览加载失败', 'error')
    } finally {
      isLoadingPreview.value = false
    }
  }

  const closePreview = () => {
    showPreview.value = false
    previewFile.value = null
    previewUrl.value = ''
    previewContent.value = ''
    isMarkdown.value = false
    isLoadingPreview.value = false
  }

  // 文件管理相关方法
  const refreshFiles = async () => {
    isLoadingFiles.value = true
    try {
      const response = await UploadAPI.getFileList()
      if (response.success) {
        fileList.value = response.files
        uploadedFilesCount.value = response.files.length
        totalStorageSize.value = formatTotalSize(response.files)
      }
    } catch (error) {
      console.error('获取文件列表失败:', error)
      showMessage('获取文件列表失败', 'error')
    } finally {
      isLoadingFiles.value = false
    }
  }

  const getFileName = (objectName: string) => {
    return objectName.split('/').pop() || objectName
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('zh-CN')
  }

  const formatTotalSize = (files: any[]) => {
    const totalBytes = files.reduce((sum, file) => sum + file.size, 0)
    return formatFileSize(totalBytes)
  }

  const downloadFile = async (objectName: string) => {
    try {
      const response = await UploadAPI.getDownloadUrl(objectName)
      if (response.success) {
        window.open(response.data.download_url, '_blank')
      }
    } catch (error) {
      console.error('获取下载链接失败:', error)
      showMessage('获取下载链接失败', 'error')
    }
  }

  const deleteFile = (objectName: string) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个文件吗？此操作不可撤销。',
      okText: '确定删除',
      cancelText: '取消',
      okType: 'danger',
      onOk: async () => {
        try {
          const response = await UploadAPI.deleteFile(objectName)
          if (response.success) {
            showMessage('文件删除成功', 'success')
            await refreshFiles()
          }
        } catch (error) {
          console.error('删除文件失败:', error)
          showMessage('删除文件失败', 'error')
        }
      }
    })
  }

  // 生命周期
  onMounted(() => {
    refreshFiles()
  })
</script>

<style scoped>
.modal-scroll::-webkit-scrollbar {
  width: 5px;
}

.modal-scroll::-webkit-scrollbar-track {
  background: transparent;
}

.modal-scroll::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.5);
  border-radius: 10px;
}

.modal-scroll::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.8);
}

.markdown-body {
  line-height: 1.7;
  color: #1f2937;
}

.markdown-body :deep(h1) { font-size: 1.5rem; font-weight: 700; margin: 1rem 0 0.5rem; }
.markdown-body :deep(h2) { font-size: 1.25rem; font-weight: 600; margin: 0.75rem 0 0.5rem; padding-bottom: 0.25rem; border-bottom: 1px solid #e5e7eb; }
.markdown-body :deep(h3) { font-size: 1.1rem; font-weight: 600; margin: 0.5rem 0; }
.markdown-body :deep(p) { margin: 0.5rem 0; }
.markdown-body :deep(ul), .markdown-body :deep(ol) { padding-left: 1.5rem; margin: 0.5rem 0; }
.markdown-body :deep(li) { margin: 0.15rem 0; }
.markdown-body :deep(code) { background: #f3f4f6; padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-size: 0.85rem; font-family: ui-monospace, monospace; }
.markdown-body :deep(pre) { background: #1f2937; color: #e5e7eb; padding: 1rem; border-radius: 0.5rem; overflow-x: auto; margin: 0.75rem 0; }
.markdown-body :deep(pre code) { background: none; padding: 0; color: inherit; font-size: 0.85rem; }
.markdown-body :deep(blockquote) { border-left: 3px solid #d1d5db; padding-left: 1rem; margin: 0.5rem 0; color: #6b7280; }
.markdown-body :deep(a) { color: #3b82f6; text-decoration: underline; }
.markdown-body :deep(table) { width: 100%; border-collapse: collapse; margin: 0.75rem 0; }
.markdown-body :deep(th), .markdown-body :deep(td) { border: 1px solid #d1d5db; padding: 0.5rem 0.75rem; text-align: left; }
.markdown-body :deep(th) { background: #f9fafb; font-weight: 600; }
.markdown-body :deep(hr) { border: none; border-top: 1px solid #e5e7eb; margin: 1rem 0; }
.markdown-body :deep(strong) { font-weight: 600; }
.markdown-body :deep(img) { max-width: 100%; border-radius: 0.5rem; }

/* 自定义动画 */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}


/* 渐变背景动画 */
@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}


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

</style> 