<template>
  <div class="flex flex-col h-full">
    <!-- 页面头部 -->
    <header class="bg-white border-b border-gray-200 flex-shrink-0">
      <div class="max-w-full mx-auto px-8 py-6">
        <div class="flex items-center justify-between">
          <!-- 标题区域 -->
          <div>
            <h1 class="text-3xl font-light text-gray-900 mb-2">知识库</h1>
            <p class="text-gray-500">构建和管理您的知识体系</p>
          </div>

          <!-- 统计和操作区域 -->
          <div class="flex items-center space-x-8">
            <div class="flex items-center space-x-6 text-sm">
              <div class="text-center">
                <div class="text-2xl font-light text-gray-900">{{ knowledgeBases.length }}</div>
                <div class="text-gray-400 uppercase tracking-wide text-xs">知识库</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-light text-gray-900">{{ totalDocuments }}</div>
                <div class="text-gray-400 uppercase tracking-wide text-xs">文档</div>
              </div>
            </div>
            <button
                @click="showCreateModal = true"
                class="bg-gray-900 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-gray-800 transition-colors flex items-center space-x-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
              </svg>
              <span>新建知识库</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- 主内容区域 -->
    <main class="flex-1 px-8 py-8 min-h-0 overflow-hidden">
      <div class="grid grid-cols-12 gap-6 h-full">

        <!-- 左侧：知识库列表 -->
        <div class="col-span-2 bg-white rounded-xl border border-gray-200 shadow-sm flex flex-col max-h-full">
          <!-- 左侧头部 -->
          <div class="p-6 border-b border-gray-100 flex-shrink-0">
            <h2 class="text-lg font-medium text-gray-900 mb-4">知识库列表</h2>
            <div class="relative">
              <input
                  v-model="knowledgeBaseSearchQuery"
                  type="text"
                  placeholder="搜索知识库..."
                  class="w-full px-4 py-2.5 pl-10 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-transparent outline-none bg-gray-50 focus:bg-white transition-colors"
              />
              <svg class="w-4 h-4 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" fill="none"
                   stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
          </div>

          <!-- 知识库列表 -->
          <div class="flex-1 min-h-0 overflow-y-auto">
            <div v-if="isLoading" class="text-center py-16">
              <div class="inline-flex items-center space-x-3 text-gray-500">
                <svg class="w-5 h-5 loading-spinner" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                </svg>
                <span class="text-sm">加载中...</span>
              </div>
            </div>

            <div v-else-if="filteredKnowledgeBases.length === 0" class="text-center py-16 px-6">
              <div class="w-12 h-12 mx-auto mb-4 bg-gray-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 011-1h6a1 1 0 011 1v2M7 7h10"/>
                </svg>
              </div>
              <p class="text-gray-500 text-sm">{{ knowledgeBaseSearchQuery ? '未找到匹配的知识库' : '暂无知识库' }}</p>
              <p class="text-gray-400 text-xs mt-1">{{
                  knowledgeBaseSearchQuery ? '尝试其他搜索词' : '点击上方按钮创建您的第一个知识库'
                }}</p>
            </div>

            <div v-else class="p-4 space-y-3">
              <div
                  v-for="kb in filteredKnowledgeBases"
                  :key="kb.id"
                  class="group p-4 rounded-lg border-l-4 border-t border-r border-b border-gray-100 hover:border-gray-300 hover:shadow-sm transition-all duration-200 cursor-pointer"
                  :class="selectedKnowledgeBase?.id === kb.id ? 'bg-gray-900 text-white border-gray-900' : ''"
                  :style="selectedKnowledgeBase?.id !== kb.id ? {
                    borderLeftColor: getKnowledgeBaseTypeInfo(kb.id).color === 'blue' ? '#60a5fa' : 
                                     getKnowledgeBaseTypeInfo(kb.id).color === 'purple' ? '#a78bfa' : '#4ade80'
                  } : {}"
                  @click="selectKnowledgeBase(kb)"
              >
                <div class="flex items-start justify-between mb-3">
                  <div class="flex items-center space-x-2 min-w-0 flex-1">
                    <!-- 知识库类型图标 -->
                    <div 
                      class="flex-shrink-0 w-5 h-5 rounded flex items-center justify-center"
                      :class="selectedKnowledgeBase?.id === kb.id ? 'bg-white/20' : getKnowledgeBaseTypeInfo(kb.id).bgClass"
                    >
                      <svg class="w-3 h-3" 
                           :class="selectedKnowledgeBase?.id === kb.id ? 'text-white' : getKnowledgeBaseTypeInfo(kb.id).textClass"
                           fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                              :d="getKnowledgeBaseTypeInfo(kb.id).icon"/>
                      </svg>
                    </div>
                    <h3 class="font-medium text-sm truncate"
                        :class="selectedKnowledgeBase?.id === kb.id ? 'text-white' : 'text-gray-900'"
                        :title="kb.name">
                      {{ kb.name }}
                    </h3>
                  </div>
                  <div class="flex items-center space-x-1 ml-2 flex-shrink-0">
                    <!-- 知识库类型标签 -->
                    <span
                        class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                        :class="selectedKnowledgeBase?.id === kb.id ? 'bg-white/20 text-white' : `${getKnowledgeBaseTypeInfo(kb.id).bgClass} ${getKnowledgeBaseTypeInfo(kb.id).textClass}`"
                        :title="`类型：${getKnowledgeBaseTypeInfo(kb.id).name}`"
                    >
                      {{ getKnowledgeBaseTypeInfo(kb.id).name }}
                    </span>
                    <!-- 状态标签 -->
                    <span
                        class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                        :class="{
                        'bg-green-100 text-green-700': kb.status === 'active' && selectedKnowledgeBase?.id !== kb.id,
                        'bg-yellow-100 text-yellow-700': kb.status === 'building' && selectedKnowledgeBase?.id !== kb.id,
                        'bg-gray-100 text-gray-700': kb.status === 'inactive' && selectedKnowledgeBase?.id !== kb.id,
                        'bg-white/20 text-white': selectedKnowledgeBase?.id === kb.id
                      }"
                    >
                      {{ getStatusText(kb.status) }}
                    </span>
                  </div>
                </div>
                <p class="text-xs mb-3 line-clamp-2"
                   :class="selectedKnowledgeBase?.id === kb.id ? 'text-gray-300' : 'text-gray-500'"
                   :title="kb.description">
                  {{ kb.description || '暂无描述' }}
                </p>
                <div class="flex items-center justify-between text-xs"
                     :class="selectedKnowledgeBase?.id === kb.id ? 'text-gray-400' : 'text-gray-400'">
                  <span>{{ kb.document_count }} 个文档</span>
                  <div class="flex items-center space-x-2">
                    <span>{{ formatDate(kb.updated_at) }}</span>
                    <!-- 操作按钮 -->
                    <div class="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button
                        @click.stop="editKnowledgeBase(kb)"
                        class="p-1 rounded hover:bg-gray-100 hover:bg-opacity-20 transition-colors"
                        :class="selectedKnowledgeBase?.id === kb.id ? 'text-gray-300 hover:text-white' : 'text-gray-400 hover:text-gray-600'"
                        title="编辑知识库"
                      >
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                      </button>
                      <button
                        @click.stop="deleteKnowledgeBase(kb)"
                        class="p-1 rounded hover:bg-red-100 hover:bg-opacity-20 transition-colors"
                        :class="selectedKnowledgeBase?.id === kb.id ? 'text-gray-300 hover:text-red-300' : 'text-gray-400 hover:text-red-600'"
                        title="删除知识库"
                      >
                        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 中间：数据内容 -->
        <div class="col-span-7 bg-white rounded-xl border border-gray-200 shadow-sm flex flex-col max-h-full">
          <div v-if="!selectedKnowledgeBase" class="flex-1 flex items-center justify-center">
            <div class="text-center">
              <div class="w-16 h-16 mx-auto mb-6 bg-gray-100 rounded-lg flex items-center justify-center">
                <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
              </div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">请选择知识库</h3>
              <p class="text-gray-500 text-sm">在左侧选择一个知识库以查看其数据内容</p>
            </div>
          </div>

          <div v-else class="flex-1 flex flex-col min-h-0">
            <!-- 数据内容头部 -->
            <div class="p-6 border-b border-gray-100 flex-shrink-0">
              <div class="flex items-center justify-between">
                <div>
                  <h2 class="text-lg font-medium text-gray-900 mb-1">数据内容</h2>
                  <p class="text-sm text-gray-500">{{ selectedKnowledgeBase.name }}</p>
                </div>
                <div class="flex items-center space-x-3">
                  <!-- 搜索框 -->
                  <div class="flex items-center space-x-2">
                    <div class="relative">
                      <input
                          v-model="dataContentSearchQuery"
                          type="text"
                          placeholder="搜索内容..."
                          class="w-56 px-4 py-2 pl-10 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-transparent outline-none bg-gray-50 focus:bg-white transition-colors"
                          @blur="() => performSearch(1)"
                          @keyup.enter="() => performSearch(1)"
                      />
                      <svg class="w-4 h-4 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" fill="none"
                           stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 数据内容区域 - 关键修改：添加了更好的滚动控制 -->
            <div class="flex-1 min-h-0 overflow-hidden">
              <div class="h-full flex flex-col">
                <!-- 数据内容 -->
                <div class="flex-1 overflow-y-auto p-6" style="max-height: calc(100vh - 400px);">
                  <div v-if="isLoadingDocuments" class="text-center py-16">
                    <div class="inline-flex items-center space-x-3 text-gray-500">
                      <svg class="w-5 h-5 loading-spinner" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                      </svg>
                      <span class="text-sm">加载数据中...</span>
                    </div>
                  </div>

                  <div v-else-if="displayedData.length === 0" class="text-center py-16">
                    <div class="w-12 h-12 mx-auto mb-4 bg-gray-100 rounded-lg flex items-center justify-center">
                      <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
                      </svg>
                    </div>
                    <p class="text-gray-500 text-sm">{{
                        dataContentSearchQuery ? '未找到匹配的数据' : '该知识库中暂无数据'
                      }}</p>
                    <p class="text-gray-400 text-xs mt-1">{{
                        dataContentSearchQuery ? '尝试其他搜索词' : '请上传文件并处理后查看数据'
                      }}</p>
                  </div>

                  <!-- 数据片段列表 -->
                  <div v-else class="space-y-6">
                    <div
                        v-for="(item, index) in displayedData"
                        :key="item.id || index"
                        class="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200"
                    >
                      <!-- 片段头部 -->
                      <div class="flex items-start justify-between mb-4">
                        <div class="flex items-center space-x-3">
                          <div class="w-8 h-8 bg-gray-900 rounded-lg flex items-center justify-center">
                            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                            </svg>
                          </div>
                          <div>
                            <h3 class="font-medium text-gray-900">
                              {{ item.title || `数据片段 #${(currentPage - 1) * pageSize + index + 1}` }}</h3>
                            <p class="text-sm text-gray-500">来源：{{ item.source || '未知来源' }}</p>
                          </div>
                        </div>
                        <div class="flex items-center space-x-2">
                          <span v-if="item.score" class="px-3 py-1 bg-green-50 text-green-700 rounded-full text-xs font-medium">
                            {{ (item.score * 100).toFixed(1) }}%
                          </span>
                          <span class="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-medium">
                            {{ item.type || 'TEXT' }}
                          </span>
                        </div>
                      </div>

                      <!-- 内容区域 -->
                      <div class="mb-4">
                        <div class="bg-gray-50 rounded-lg p-4 border-l-4 border-gray-900">
                          <p class="text-gray-800 text-sm leading-relaxed whitespace-pre-wrap">
                            {{ item.content || item.text || '暂无内容' }}
                          </p>
                        </div>
                      </div>

                      <!-- 元信息和操作 -->
                      <div class="flex items-center justify-between text-xs text-gray-500">
                        <div class="flex items-center space-x-4">
                          <span v-if="item.created_at">{{ formatDate(item.created_at) }}</span>
                          <span v-if="item.chunk_index">块索引：{{ item.chunk_index }}</span>
                          <span v-if="item.word_count">{{ item.word_count }} 字</span>
                        </div>
                        <div class="flex items-center space-x-2">
                          <button
                              @click="viewDataDetail(item)"
                              class="text-gray-600 hover:text-gray-900 p-1.5 rounded-lg hover:bg-gray-100 transition-colors"
                              title="查看详情"
                          >
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                            </svg>
                          </button>
                          <button
                              @click="removeDataItem(item)"
                              class="text-red-500 hover:text-red-700 p-1.5 rounded-lg hover:bg-red-50 transition-colors"
                              title="删除数据"
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
                </div>

                <!-- 分页控件 -->
                <div v-if="totalPages > 1 && !isLoadingDocuments"
                     class="border-t border-gray-100 px-6 py-4 flex-shrink-0 pagination-container">
                  <div class="flex items-center justify-between pagination-controls">
                    <!-- 分页信息 -->
                    <div class="text-sm text-gray-700 pagination-info">
                      显示第 {{ (currentPage - 1) * pageSize + 1 }} - {{ Math.min(currentPage * pageSize, totalItems) }} 条，
                      共 {{ totalItems }} 条{{ dataContentSearchQuery.trim() ? '搜索结果' : '数据' }}
                    </div>

                    <!-- 分页控件 -->
                    <div class="flex items-center space-x-2">
                      <!-- 每页显示数量选择 -->
                      <div class="flex items-center space-x-2 mr-4">
                        <span class="text-sm text-gray-600">每页</span>
                        <select
                            v-model="pageSize"
                            @change="currentPage = 1; dataContentSearchQuery.trim() ? performSearch(1) : refreshDocuments(1)"
                            class="text-sm rounded px-2 py-1 outline-none page-size-selector"
                        >
                          <option :value="5">5</option>
                          <option :value="10">10</option>
                          <option :value="20">20</option>
                          <option :value="50">50</option>
                        </select>
                        <span class="text-sm text-gray-600">条</span>
                      </div>

                      <!-- 第一页 -->
                      <button
                          @click="goToFirstPage"
                          :disabled="currentPage === 1"
                          class="px-3 py-1 text-sm border border-gray-200 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed page-button"
                          title="第一页"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M11 19l-7-7 7-7m8 14l-7-7 7-7"/>
                        </svg>
                      </button>

                      <!-- 上一页 -->
                      <button
                          @click="goToPrevPage"
                          :disabled="currentPage === 1"
                          class="px-3 py-1 text-sm border border-gray-200 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed page-button"
                          title="上一页"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
                        </svg>
                      </button>

                      <!-- 页码 -->
                      <div class="flex items-center space-x-1">
                        <template v-for="page in getVisiblePages()" :key="page">
                          <button
                              v-if="page !== '...'"
                              @click="goToPage(page as number)"
                              :class="{
                              'bg-gray-900 text-white active': page === currentPage,
                              'border-gray-200 hover:bg-gray-50': page !== currentPage
                            }"
                              class="px-3 py-1 text-sm border rounded page-button"
                          >
                            {{ page }}
                          </button>
                          <span v-else class="px-2 text-gray-400">...</span>
                        </template>
                      </div>

                      <!-- 下一页 -->
                      <button
                          @click="goToNextPage"
                          :disabled="currentPage === totalPages"
                          class="px-3 py-1 text-sm border border-gray-200 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed page-button"
                          title="下一页"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
                        </svg>
                      </button>

                      <!-- 最后一页 -->
                      <button
                          @click="goToLastPage"
                          :disabled="currentPage === totalPages"
                          class="px-3 py-1 text-sm border border-gray-200 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed page-button"
                          title="最后一页"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 5l7 7-7 7M5 5l7 7-7 7"/>
                        </svg>
                      </button>

                      <!-- 跳转到指定页 -->
                      <div class="flex items-center space-x-2 ml-4">
                        <span class="text-sm text-gray-600">跳转到</span>
                        <input
                            type="number"
                            :min="1"
                            :max="totalPages"
                            v-model.number="jumpToPageNumber"
                            @keyup.enter="goToPage(jumpToPageNumber)"
                            class="w-16 px-2 py-1 text-sm rounded outline-none jump-input"
                            placeholder="页码"
                        />
                        <button
                            @click="goToPage(jumpToPageNumber)"
                            class="px-3 py-1 text-sm bg-gray-900 text-white rounded hover:bg-gray-800 page-button"
                        >
                          跳转
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧：知识库设置 -->
        <div class="col-span-3 bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden flex flex-col max-h-full">
          <div v-if="!selectedKnowledgeBase" class="flex-1 flex items-center justify-center">
            <div class="text-center px-4">
              <div class="w-12 h-12 mx-auto mb-4 bg-gray-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
              </div>
              <p class="text-gray-500 text-sm">知识库设置</p>
              <p class="text-gray-400 text-xs mt-1">选择知识库以查看设置选项</p>
            </div>
          </div>

          <div v-else class="flex-1 flex flex-col min-h-0">
            <!-- 设置头部 -->
            <div class="p-6 border-b border-gray-100 flex-shrink-0">
              <h2 class="text-lg font-medium text-gray-900 mb-1">设置</h2>
              <p class="text-sm text-gray-500">{{ selectedKnowledgeBase.name }}</p>
            </div>

            <!-- 设置内容 -->
            <div class="flex-1 overflow-y-auto p-6 space-y-8">
              <!-- 基本信息 -->
              <div>
                <h3 class="text-sm font-medium text-gray-900 mb-4">基本信息</h3>
                <div class="space-y-4">
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-1">名称</label>
                    <p class="text-sm text-gray-900">{{ selectedKnowledgeBase.name }}</p>
                  </div>
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-1">描述</label>
                    <p class="text-sm text-gray-600">{{ selectedKnowledgeBase.description || '暂无描述' }}</p>
                  </div>
                </div>
              </div>

              <!-- 统计信息 -->
              <div>
                <h3 class="text-sm font-medium text-gray-900 mb-4">统计信息</h3>
                <div class="space-y-3">
                  <div class="flex justify-between items-center py-2">
                    <span class="text-xs text-gray-600">文档数量</span>
                    <span class="text-sm font-medium text-gray-900">{{ selectedKnowledgeBase.document_count }}</span>
                  </div>
                  <div class="flex justify-between items-center py-2">
                    <span class="text-xs text-gray-600">存储大小</span>
                    <span class="text-sm font-medium text-gray-900">{{ formatFileSize(selectedKnowledgeBase.size) }}</span>
                  </div>
                  <div class="flex justify-between items-center py-2">
                    <span class="text-xs text-gray-600">创建时间</span>
                    <span class="text-sm font-medium text-gray-900">{{ formatDate(selectedKnowledgeBase.created_at) }}</span>
                  </div>
                  <div class="flex justify-between items-center py-2">
                    <span class="text-xs text-gray-600">更新时间</span>
                    <span class="text-sm font-medium text-gray-900">{{ formatDate(selectedKnowledgeBase.updated_at) }}</span>
                  </div>
                </div>
              </div>

              <!-- 操作按钮 -->
              <div class="space-y-3">
                <button
                    @click="openKnowledgeBaseSettings(selectedKnowledgeBase)"
                    class="w-full bg-gray-900 text-white px-4 py-2.5 rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors"
                >
                  配置设置
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 创建知识库模态框 -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-medium text-gray-900">创建新知识库</h3>
          <button
              @click="showCreateModal = false"
              class="text-gray-400 hover:text-gray-600 p-1 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <form @submit.prevent="createKnowledgeBase">
          <div class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">名称</label>
              <input
                  v-model="newKnowledgeBase.name"
                  type="text"
                  required
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-transparent outline-none transition-colors"
                  placeholder="输入知识库名称"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">描述</label>
              <textarea
                  v-model="newKnowledgeBase.description"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-transparent outline-none transition-colors resize-none"
                  rows="4"
                  placeholder="输入知识库描述"
              ></textarea>
            </div>
            
            <!-- 知识库类型选择 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-4">知识库类型</label>
              <div class="grid grid-cols-1 gap-4">
                <label class="relative cursor-pointer">
                  <input
                      v-model="newKnowledgeBase.index_type"
                      type="radio"
                      value="vector"
                      class="sr-only"
                  />
                  <div
                      class="border-2 rounded-lg p-4 transition-all duration-200"
                      :class="newKnowledgeBase.index_type === 'vector' ? 'border-gray-900 bg-gray-50' : 'border-gray-200 hover:border-gray-300'"
                  >
                    <div class="flex items-start space-x-3">
                      <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center mt-0.5"
                           :class="newKnowledgeBase.index_type === 'vector' ? 'border-gray-900 bg-gray-900' : 'border-gray-300'">
                        <div v-if="newKnowledgeBase.index_type === 'vector'"
                             class="w-2 h-2 bg-white rounded-full"></div>
                      </div>
                      <div class="flex-1">
                        <h5 class="font-medium text-gray-900 mb-1">常规向量索引</h5>
                        <p class="text-sm text-gray-600">
                          使用向量嵌入技术构建索引，适用于大多数文档检索场景，检索速度快，准确性高。推荐用于一般的问答和文档搜索。
                        </p>
                      </div>
                    </div>
                  </div>
                </label>

                <label class="relative cursor-pointer">
                  <input
                      v-model="newKnowledgeBase.index_type"
                      type="radio"
                      value="knowledge_graph"
                      class="sr-only"
                  />
                  <div
                      class="border-2 rounded-lg p-4 transition-all duration-200"
                      :class="newKnowledgeBase.index_type === 'knowledge_graph' ? 'border-gray-900 bg-gray-50' : 'border-gray-200 hover:border-gray-300'"
                  >
                    <div class="flex items-start space-x-3">
                      <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center mt-0.5"
                           :class="newKnowledgeBase.index_type === 'knowledge_graph' ? 'border-gray-900 bg-gray-900' : 'border-gray-300'">
                        <div v-if="newKnowledgeBase.index_type === 'knowledge_graph'"
                             class="w-2 h-2 bg-white rounded-full"></div>
                      </div>
                      <div class="flex-1">
                        <h5 class="font-medium text-gray-900 mb-1">知识图谱索引</h5>
                        <p class="text-sm text-gray-600">
                          构建实体关系图谱，适用于需要理解实体间关系的复杂查询场景，支持推理查询。适合结构化数据和关系分析。
                        </p>
                      </div>
                    </div>
                  </div>
                </label>

                <label class="relative cursor-pointer">
                  <input
                      v-model="newKnowledgeBase.index_type"
                      type="radio"
                      value="long_document"
                      class="sr-only"
                  />
                  <div
                      class="border-2 rounded-lg p-4 transition-all duration-200"
                      :class="newKnowledgeBase.index_type === 'long_document' ? 'border-gray-900 bg-gray-50' : 'border-gray-200 hover:border-gray-300'"
                  >
                    <div class="flex items-start space-x-3">
                      <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center mt-0.5"
                           :class="newKnowledgeBase.index_type === 'long_document' ? 'border-gray-900 bg-gray-900' : 'border-gray-300'">
                        <div v-if="newKnowledgeBase.index_type === 'long_document'"
                             class="w-2 h-2 bg-white rounded-full"></div>
                      </div>
                      <div class="flex-1">
                        <h5 class="font-medium text-gray-900 mb-1">长文档索引</h5>
                        <p class="text-sm text-gray-600">
                          专为长文档优化的检索索引，保持上下文连续性，适用于学术论文、技术文档、书籍等长内容的分析和检索。
                        </p>
                      </div>
                    </div>
                  </div>
                </label>
              </div>
              
              <!-- 提示信息 -->
              <div class="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <div class="flex items-start space-x-3">
                  <svg class="w-5 h-5 text-blue-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                  </svg>
                  <div>
                    <h5 class="text-sm font-medium text-blue-900 mb-1">选择建议</h5>
                    <p class="text-sm text-blue-800">
                      • <strong>向量索引</strong>：适合日常文档问答，响应快速<br>
                      • <strong>知识图谱</strong>：适合需要关系分析的复杂查询<br>
                      • <strong>长文档索引</strong>：适合学术论文、技术文档等长内容
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="flex items-center justify-end space-x-4 mt-8">
            <button
                type="button"
                @click="showCreateModal = false"
                class="px-6 py-2.5 text-gray-600 hover:text-gray-800 transition-colors"
            >
              取消
            </button>
            <button
                type="submit"
                :disabled="isCreating"
                class="bg-gray-900 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-gray-800 transition-colors disabled:opacity-50"
            >
              {{ isCreating ? '创建中...' : '创建知识库' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 编辑知识库模态框 -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md mx-4">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-medium text-gray-900">编辑知识库</h3>
          <button
              @click="showEditModal = false"
              class="text-gray-400 hover:text-gray-600 p-1 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <form @submit.prevent="updateKnowledgeBase">
          <div class="space-y-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">名称</label>
              <input
                  v-model="editingKnowledgeBase.name"
                  type="text"
                  required
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-transparent outline-none transition-colors"
                  placeholder="输入知识库名称"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">描述</label>
              <textarea
                  v-model="editingKnowledgeBase.description"
                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-transparent outline-none transition-colors resize-none"
                  rows="4"
                  placeholder="输入知识库描述"
              ></textarea>
            </div>
          </div>

          <div class="flex items-center justify-end space-x-4 mt-8">
            <button
                type="button"
                @click="showEditModal = false"
                class="px-6 py-2.5 text-gray-600 hover:text-gray-800 transition-colors"
            >
              取消
            </button>
            <button
                type="submit"
                :disabled="isUpdating"
                class="bg-gray-900 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-gray-800 transition-colors disabled:opacity-50"
            >
              {{ isUpdating ? '更新中...' : '更新知识库' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- 知识库设置模态框 -->
    <Teleport to="body">
      <Transition name="drawer" appear>
        <div v-if="showSettingsModal" class="fixed inset-0 z-50 overflow-hidden">
          <!-- 背景遮罩 -->
          <div class="absolute inset-0 overflow-hidden">
            <div class="absolute inset-0 bg-black bg-opacity-50" @click="showSettingsModal = false"></div>

            <!-- 抽屉容器 -->
            <section class="absolute inset-y-0 right-0 pl-10 max-w-full flex">
              <div class="relative w-screen max-w-2xl">
                <div class="h-full flex flex-col bg-white shadow-xl overflow-y-scroll">
                  <!-- 模态框头部 -->
                  <div class="flex items-center justify-between p-6 border-b border-gray-200 flex-shrink-0">
                    <h3 class="text-xl font-medium text-gray-900">知识库设置</h3>
                    <button
                        @click="showSettingsModal = false"
                        class="text-gray-400 hover:text-gray-600 p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                      </svg>
                    </button>
                  </div>

                  <!-- 模态框内容区域 -->
                  <div class="flex-1 overflow-y-auto">
                    <form @submit.prevent="saveKnowledgeBaseSettings" class="p-6">
                      <div class="space-y-8">

                        <!-- 文本分块设置 -->
                        <div>
                          <h4 class="text-lg font-medium text-gray-900 mb-4">文本分块设置</h4>
                          <div class="space-y-4">
                            <!-- Chunk Size -->
                            <div>
                              <label class="block text-sm font-medium text-gray-700 mb-2">
                                分块大小 (chunk_size)
                                <span class="text-xs text-gray-500 ml-1">范围: 100-4000</span>
                              </label>
                              <input
                                  v-model.number="knowledgeBaseSettings.chunk_size"
                                  type="number"
                                  min="100"
                                  max="4000"
                                  required
                                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-transparent outline-none transition-colors"
                                  placeholder="输入分块大小"
                              />
                              <p class="text-xs text-gray-500 mt-1">每个文本块的最大字符数</p>
                            </div>

                            <!-- Chunk Overlap -->
                            <div>
                              <label class="block text-sm font-medium text-gray-700 mb-2">
                                分块重叠 (chunk_overlap)
                                <span class="text-xs text-gray-500 ml-1">范围: 0-500，且不能大于分块大小</span>
                              </label>
                              <input
                                  v-model.number="knowledgeBaseSettings.chunk_overlap"
                                  type="number"
                                  min="0"
                                  :max="Math.min(500, knowledgeBaseSettings.chunk_size - 1)"
                                  required
                                  class="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-transparent outline-none transition-colors"
                                  placeholder="输入重叠字符数"
                              />
                              <p class="text-xs text-gray-500 mt-1">相邻文本块之间的重叠字符数</p>
                            </div>
                          </div>
                        </div>

                        <!-- 文本拆分策略 -->
                        <div>
                          <h4 class="text-lg font-medium text-gray-900 mb-4">文本拆分策略</h4>
                          <div class="space-y-4">
                            <div class="flex items-center space-x-4">
                              <label class="flex items-center">
                                <input
                                    v-model="knowledgeBaseSettings.text_split_strategy"
                                    type="radio"
                                    value="fixed_chars"
                                    class="w-4 h-4 text-gray-900 border-gray-300 focus:ring-gray-900"
                                />
                                <span class="ml-2 text-sm text-gray-700">按固定字符拆分</span>
                              </label>
                              <label class="flex items-center">
                                <input
                                    v-model="knowledgeBaseSettings.text_split_strategy"
                                    type="radio"
                                    value="semantic"
                                    class="w-4 h-4 text-gray-900 border-gray-300 focus:ring-gray-900"
                                />
                                <span class="ml-2 text-sm text-gray-700">按语义自动切分</span>
                              </label>
                            </div>

                            <!-- 固定字符拆分设置 -->
                            <div v-if="knowledgeBaseSettings.text_split_strategy === 'fixed_chars'" class="mt-4">
                              <label class="block text-sm font-medium text-gray-700 mb-2">拆分字符</label>
                              <div class="space-y-2">
                                <div
                                    v-for="(_, index) in knowledgeBaseSettings.split_chars"
                                    :key="index"
                                    class="flex items-center space-x-2"
                                >
                                  <span class="text-sm text-gray-500 w-8">{{ index + 1 }}.</span>
                                  <input
                                      :value="displaySplitChar(knowledgeBaseSettings.split_chars[index])"
                                      @input="updateSplitChar(index, ($event.target as HTMLInputElement).value)"
                                      type="text"
                                      class="flex-1 px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-gray-900 focus:border-transparent outline-none transition-colors text-sm font-mono"
                                      placeholder="输入拆分字符"
                                  />
                                  <button
                                      type="button"
                                      @click="removeSplitChar(index)"
                                      class="text-red-600 hover:text-red-700 p-1 rounded-lg hover:bg-red-50 transition-colors"
                                      title="删除"
                                  >
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                                    </svg>
                                  </button>
                                </div>
                                <button
                                    type="button"
                                    @click="addSplitChar"
                                    class="flex items-center space-x-2 text-sm text-gray-600 hover:text-gray-900 p-2 rounded-lg hover:bg-gray-50 transition-colors"
                                >
                                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                                  </svg>
                                  <span>添加拆分字符</span>
                                </button>
                              </div>
                              <p class="text-xs text-gray-500 mt-2">
                                按优先级顺序设置拆分字符，系统会按顺序尝试使用这些字符进行文本拆分。<br>
                                特殊字符输入方式：换行符输入 <code class="bg-gray-100 px-1 rounded">\\n</code>，双换行符输入 <code class="bg-gray-100 px-1 rounded">\\n\\n</code>，制表符输入 <code class="bg-gray-100 px-1 rounded">\\t</code>
                              </p>
                            </div>

                            <!-- 语义拆分说明 -->
                            <div v-if="knowledgeBaseSettings.text_split_strategy === 'semantic'" class="mt-4">
                              <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                                <div class="flex items-start space-x-3">
                                  <svg class="w-5 h-5 text-blue-600 mt-0.5" fill="none" stroke="currentColor"
                                       viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                  </svg>
                                  <div>
                                    <h5 class="text-sm font-medium text-blue-900 mb-1">语义自动切分</h5>
                                    <p class="text-sm text-blue-700">
                                      系统将使用AI模型自动识别文本的语义边界进行切分，确保每个文本块在语义上完整。这种方式可能会产生长度不均匀但语义更完整的文本块。</p>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>

                        <!-- 知识库索引类型 -->
                        <div>
                          <h4 class="text-lg font-medium text-gray-900 mb-4">知识库索引类型</h4>
                          <div class="space-y-4">
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                              <label class="relative cursor-pointer">
                                <input
                                    v-model="knowledgeBaseSettings.index_type"
                                    type="radio"
                                    value="vector"
                                    class="sr-only"
                                />
                                <div
                                    class="border-2 rounded-lg p-4 transition-all duration-200"
                                    :class="knowledgeBaseSettings.index_type === 'vector' ? 'border-gray-900 bg-gray-50' : 'border-gray-200 hover:border-gray-300'"
                                >
                                  <div class="flex items-start space-x-3">
                                    <div class="w-6 h-6 rounded-full border-2 flex items-center justify-center mt-0.5"
                                         :class="knowledgeBaseSettings.index_type === 'vector' ? 'border-gray-900 bg-gray-900' : 'border-gray-300'">
                                      <div v-if="knowledgeBaseSettings.index_type === 'vector'"
                                           class="w-2 h-2 bg-white rounded-full"></div>
                                    </div>
                                    <div>
                                      <h5 class="font-medium text-gray-900 mb-1">常规向量索引</h5>
                                      <p class="text-sm text-gray-600">
                                        使用向量嵌入技术构建索引，适用于大多数文档检索场景，检索速度快，准确性高。</p>
                                    </div>
                                  </div>
                                </div>
                              </label>

                              <label class="relative cursor-pointer">
                                <input
                                    v-model="knowledgeBaseSettings.index_type"
                                    type="radio"
                                    value="knowledge_graph"
                                    class="sr-only"
                                />
                                <div
                                    class="border-2 rounded-lg p-4 transition-all duration-200"
                                    :class="knowledgeBaseSettings.index_type === 'knowledge_graph' ? 'border-gray-900 bg-gray-50' : 'border-gray-200 hover:border-gray-300'"
                                >
                                  <div class="flex items-start space-x-3">
                                    <div class="w-6 h-6 rounded-full border-2 flex items-center justify-center mt-0.5"
                                         :class="knowledgeBaseSettings.index_type === 'knowledge_graph' ? 'border-gray-900 bg-gray-900' : 'border-gray-300'">
                                      <div v-if="knowledgeBaseSettings.index_type === 'knowledge_graph'"
                                           class="w-2 h-2 bg-white rounded-full"></div>
                                    </div>
                                    <div>
                                      <h5 class="font-medium text-gray-900 mb-1">知识图谱索引</h5>
                                      <p class="text-sm text-gray-600">
                                        构建实体关系图谱，适用于需要理解实体间关系的复杂查询场景，支持推理查询。</p>
                                    </div>
                                  </div>
                                </div>
                              </label>

                              <label class="relative cursor-pointer">
                                <input
                                    v-model="knowledgeBaseSettings.index_type"
                                    type="radio"
                                    value="long_document"
                                    class="sr-only"
                                />
                                <div
                                    class="border-2 rounded-lg p-4 transition-all duration-200"
                                    :class="knowledgeBaseSettings.index_type === 'long_document' ? 'border-gray-900 bg-gray-50' : 'border-gray-200 hover:border-gray-300'"
                                >
                                  <div class="flex items-start space-x-3">
                                    <div class="w-6 h-6 rounded-full border-2 flex items-center justify-center mt-0.5"
                                         :class="knowledgeBaseSettings.index_type === 'long_document' ? 'border-gray-900 bg-gray-900' : 'border-gray-300'">
                                      <div v-if="knowledgeBaseSettings.index_type === 'long_document'"
                                           class="w-2 h-2 bg-white rounded-full"></div>
                                    </div>
                                    <div>
                                      <h5 class="font-medium text-gray-900 mb-1">长文档索引</h5>
                                      <p class="text-sm text-gray-600">
                                        专为长文档优化的检索索引，保持上下文连续性，适用于学术论文、技术文档等长内容。</p>
                                    </div>
                                  </div>
                                </div>
                              </label>
                            </div>
                          </div>
                        </div>

                      </div>

                      <div class="flex items-center justify-end space-x-4 mt-8 pt-6 border-t border-gray-200">
                        <button
                            type="button"
                            @click="showSettingsModal = false"
                            class="px-6 py-2.5 text-gray-600 hover:text-gray-800 transition-colors"
                        >
                          取消
                        </button>
                        <button
                            type="submit"
                            :disabled="isSavingSettings"
                            class="bg-gray-900 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-gray-800 transition-colors disabled:opacity-50"
                        >
                          {{ isSavingSettings ? '保存中...' : '保存设置' }}
                        </button>
                      </div>
                    </form>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- 自定义弹窗组件 -->
    <CustomModal
      v-model:isVisible="modal.isVisible"
      :type="modal.type"
      :title="modal.title"
      :message="modal.message"
      :confirmText="modal.confirmText"
      :cancelText="modal.cancelText"
      @confirm="handleModalConfirm"
      @cancel="handleModalCancel"
    />
  </div>
</template>

<script setup lang="ts">
import {computed, onMounted, ref} from 'vue'
import {
  createKnowledgeBase as createKnowledgeBaseAPI,
  deleteKnowledgeBase as deleteKnowledgeBaseAPI,
  type CreateKnowledgeBaseRequest,
  getKnowledgeBases,
  KnowledgeAPI,
  type KnowledgeBase,
  type KnowledgeBaseSettings,
  type KnowledgeDocument,
  updateKnowledgeBase as updateKnowledgeBaseAPI,
  type UpdateKnowledgeBaseRequest
} from '@/api/knowledge'
import CustomModal from '@/components/CustomModal.vue'

// 响应式数据
const knowledgeBases = ref<KnowledgeBase[]>([])
const knowledgeData = ref<any[]>([])
const searchResults = ref<any[]>([])
const knowledgeBaseSearchQuery = ref('') // 知识库列表搜索
const dataContentSearchQuery = ref('') // 知识库数据内容搜索
const isLoading = ref(false)
const isLoadingDocuments = ref(false)
const isCreating = ref(false)
const isUpdating = ref(false)

// 模态框控制
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showSettingsModal = ref(false)

// 表单数据
const newKnowledgeBase = ref<CreateKnowledgeBaseRequest>({
  name: '',
  description: '',
  index_type: 'vector' // 默认选择向量索引
})

const editingKnowledgeBase = ref<UpdateKnowledgeBaseRequest>({
  name: '',
  description: ''
})

const selectedKnowledgeBase = ref<KnowledgeBase | null>(null)
const editingKnowledgeBaseId = ref<string>('')

// 知识库设置数据

const knowledgeBaseSettings = ref<KnowledgeBaseSettings>({
  chunk_size: 1000,
  chunk_overlap: 100,
  text_split_strategy: 'fixed_chars',
  split_chars: ['\n\n', '\n', '。', '！', '？', ';', '；'],
  index_type: 'vector'
})

const settingsKnowledgeBaseId = ref<string>('')
const isSavingSettings = ref(false)

// 存储知识库类型信息的Map
const knowledgeBaseTypes = ref<Map<string, string>>(new Map())

// 自定义弹窗控制
const modal = ref({
  isVisible: false,
  type: 'alert' as 'alert' | 'confirm' | 'success' | 'error' | 'warning',
  title: '',
  message: '',
  confirmText: '确定',
  cancelText: '取消',
  onConfirm: null as (() => void) | null,
  onCancel: null as (() => void) | null
})

// 在script setup部分添加分页相关的响应式变量
const currentPage = ref(1)
const pageSize = ref(10) // 每页显示的数据条数
const totalItems = ref(0)
const totalPages = computed(() => {
  // 统一基于totalItems计算总页数
  return Math.ceil(totalItems.value / pageSize.value)
})
const jumpToPageNumber = ref<number | null>(null)

// 计算属性
const filteredKnowledgeBases = computed(() => {
  if (!knowledgeBaseSearchQuery.value) return knowledgeBases.value

  const query = knowledgeBaseSearchQuery.value.toLowerCase()
  return knowledgeBases.value.filter(kb =>
      kb.name.toLowerCase().includes(query) ||
      kb.description.toLowerCase().includes(query)
  )
})

const totalDocuments = computed(() => {
  return knowledgeBases.value.reduce((total, kb) => total + kb.document_count, 0)
})

const displayedData = computed(() => {
  // 统一使用knowledgeData，无论是搜索还是正常浏览状态
  return knowledgeData.value
})

// 获取可见的页码列表
const getVisiblePages = () => {
  const total = totalPages.value
  const current = currentPage.value
  const pages: (number | string)[] = []

  if (total <= 7) {
    // 如果总页数不超过7页，显示所有页码
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    // 复杂分页逻辑
    if (current <= 4) {
      // 当前页在前面
      for (let i = 1; i <= 5; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(total)
    } else if (current >= total - 3) {
      // 当前页在后面
      pages.push(1)
      pages.push('...')
      for (let i = total - 4; i <= total; i++) {
        pages.push(i)
      }
    } else {
      // 当前页在中间
      pages.push(1)
      pages.push('...')
      for (let i = current - 1; i <= current + 1; i++) {
        pages.push(i)
      }
      pages.push('...')
      pages.push(total)
    }
  }

  return pages
}

// 自定义弹窗方法
const showAlert = (message: string, title: string = '提示', type: 'alert' | 'success' | 'error' | 'warning' = 'alert') => {
  modal.value = {
    isVisible: true,
    type,
    title,
    message,
    confirmText: '确定',
    cancelText: '取消',
    onConfirm: null,
    onCancel: null
  }
}

const showConfirm = (message: string, title: string = '确认', onConfirm?: () => void, onCancel?: () => void) => {
  modal.value = {
    isVisible: true,
    type: 'confirm',
    title,
    message,
    confirmText: '确定',
    cancelText: '取消',
    onConfirm: onConfirm || null,
    onCancel: onCancel || null
  }
}

const handleModalConfirm = () => {
  if (modal.value.onConfirm) {
    modal.value.onConfirm()
  }
}

const handleModalCancel = () => {
  if (modal.value.onCancel) {
    modal.value.onCancel()
  }
}

// 添加分页相关方法
const goToPage = async (page: number | null) => {
  if (!page || page < 1 || page > totalPages.value || page === currentPage.value) return

  if (dataContentSearchQuery.value.trim()) {
    // 如果是搜索状态，使用搜索分页
    await performSearch(page)
  } else {
    // 如果不是搜索状态，重新获取数据
    await refreshDocuments(page)
  }
}

const goToFirstPage = () => goToPage(1)
const goToLastPage = () => goToPage(totalPages.value)
const goToPrevPage = () => goToPage(currentPage.value - 1)
const goToNextPage = () => goToPage(currentPage.value + 1)

// 获取知识库类型
const getKnowledgeBaseType = async (kbId: string): Promise<string> => {
  try {
    const response = await KnowledgeAPI.getKnowledgeBaseSettings(kbId)
    if (response.success && response.data) {
      const indexType = response.data.index_type || 'vector'
      knowledgeBaseTypes.value.set(kbId, indexType)
      return indexType
    }
  } catch (error) {
    console.error(`获取知识库 ${kbId} 类型失败:`, error)
  }
  
  // 默认返回向量索引
  knowledgeBaseTypes.value.set(kbId, 'vector')
  return 'vector'
}

// 批量获取知识库类型
const loadKnowledgeBaseTypes = async () => {
  const promises = knowledgeBases.value.map(kb => getKnowledgeBaseType(kb.id))
  await Promise.allSettled(promises)
}

// 方法
const refreshKnowledgeBases = async () => {
  isLoading.value = true
  try {
    const response = await getKnowledgeBases()
    if (response.success) {
      knowledgeBases.value = response.data

      // 批量获取知识库类型信息
      await loadKnowledgeBaseTypes()

      // 自动选择最后选择的知识库，如果没有则选择第一个
      if (knowledgeBases.value.length > 0) {
        const lastSelectedId = localStorage.getItem('lastSelectedKnowledgeBase')
        let targetKnowledgeBase: KnowledgeBase | null = null

        if (lastSelectedId) {
          // 查找最后选择的知识库
          targetKnowledgeBase = knowledgeBases.value.find(kb => kb.id === lastSelectedId) || null
        }

        // 如果没找到最后选择的知识库，则选择第一个
        if (!targetKnowledgeBase) {
          targetKnowledgeBase = knowledgeBases.value[0]
        }

        // 只有在没有已选择的知识库时才自动选择
        if (!selectedKnowledgeBase.value && targetKnowledgeBase) {
          await selectKnowledgeBase(targetKnowledgeBase)
        }
      }
    }
  } catch (error) {
    console.error('刷新知识库列表失败:', error)
    // 这里可以添加错误提示
  } finally {
    isLoading.value = false
  }
}

const createKnowledgeBase = async () => {
  if (!newKnowledgeBase.value.name.trim()) return

  isCreating.value = true
  try {
    const response = await createKnowledgeBaseAPI(newKnowledgeBase.value)
    if (response.success) {
      showCreateModal.value = false
      
      // 显示成功信息
      const indexTypeNames = {
        'vector': '向量索引',
        'knowledge_graph': '知识图谱索引', 
        'long_document': '长文档索引'
      }
      const typeName = indexTypeNames[newKnowledgeBase.value.index_type as keyof typeof indexTypeNames] || '向量索引'
      console.log(`知识库"${newKnowledgeBase.value.name}"创建成功！类型：${typeName}`)
      
      newKnowledgeBase.value = {name: '', description: '', index_type: 'vector'}
      await refreshKnowledgeBases()
      
      // 为新创建的知识库设置类型信息
      if (response.data && response.data.id) {
        knowledgeBaseTypes.value.set(response.data.id, newKnowledgeBase.value.index_type || 'vector')
      }
    }
  } catch (error) {
    console.error('创建知识库失败:', error)
    showAlert('创建知识库失败: ' + (error as Error).message, '错误', 'error')
  } finally {
    isCreating.value = false
  }
}

const editKnowledgeBase = (kb: KnowledgeBase, event?: Event) => {
  if (event) {
    event.stopPropagation()
  }
  editingKnowledgeBaseId.value = kb.id
  editingKnowledgeBase.value = {
    name: kb.name,
    description: kb.description
  }
  showEditModal.value = true
}

const updateKnowledgeBase = async () => {
  if (!editingKnowledgeBase.value.name?.trim()) return

  isUpdating.value = true
  try {
    const response = await updateKnowledgeBaseAPI(
        editingKnowledgeBaseId.value,
        editingKnowledgeBase.value
    )
    if (response.success) {
      showEditModal.value = false
      await refreshKnowledgeBases()
      // 这里可以添加成功提示
    }
  } catch (error) {
    console.error('更新知识库失败:', error)
    // 这里可以添加错误提示
  } finally {
    isUpdating.value = false
  }
}

const deleteKnowledgeBase = async (kb: KnowledgeBase, event?: Event) => {
  if (event) {
    event.stopPropagation()
  }

  showConfirm(
    `确定要删除知识库"${kb.name}"吗？此操作不可恢复。`,
    '确认删除',
    async () => {
      try {
        const response = await deleteKnowledgeBaseAPI(kb.id)
        if (response.success) {
          // 如果删除的是当前选中的知识库，清除选择状态
          if (selectedKnowledgeBase.value?.id === kb.id) {
            selectedKnowledgeBase.value = null
            localStorage.removeItem('lastSelectedKnowledgeBase')
          }

          // 如果删除的是localStorage中记录的知识库，也要清除记录
          const lastSelectedId = localStorage.getItem('lastSelectedKnowledgeBase')
          if (lastSelectedId === kb.id) {
            localStorage.removeItem('lastSelectedKnowledgeBase')
          }

          await refreshKnowledgeBases()
          showAlert('知识库删除成功', '提示', 'success')
        } else {
          showAlert('删除知识库失败: ' + response.message, '错误', 'error')
        }
      } catch (error) {
        console.error('删除知识库失败:', error)
        showAlert('删除知识库失败: ' + (error as Error).message, '错误', 'error')
      }
    }
  )
}

const selectKnowledgeBase = async (kb: KnowledgeBase) => {
  selectedKnowledgeBase.value = kb
  // 保存最后选择的知识库ID到localStorage
  localStorage.setItem('lastSelectedKnowledgeBase', kb.id)
  // 重置分页状态
  currentPage.value = 1
  dataContentSearchQuery.value = ''
  searchResults.value = []
  await refreshDocuments(1)
}

// 知识库设置相关函数
const openKnowledgeBaseSettings = async (kb: KnowledgeBase) => {
  settingsKnowledgeBaseId.value = kb.id

  try {
    // 尝试加载现有设置
    const response = await KnowledgeAPI.getKnowledgeBaseSettings(kb.id)
    if (response.success && response.data) {
      knowledgeBaseSettings.value = response.data
    } else {
      // 如果没有现有设置，使用默认值
      knowledgeBaseSettings.value = {
        chunk_size: 1000,
        chunk_overlap: 100,
        text_split_strategy: 'fixed_chars',
        split_chars: ['\n\n', '\n', '。', '！', '？', ';', '；'],
        index_type: 'vector'
      }
    }
  } catch (error) {
    console.error('加载知识库设置失败:', error)
    // 使用默认设置
    knowledgeBaseSettings.value = {
      chunk_size: 1000,
      chunk_overlap: 100,
      text_split_strategy: 'fixed_chars',
      split_chars: ['\n\n', '\n', '。', '！', '？', ';', '；'],
      index_type: 'vector'
    }
  }

  showSettingsModal.value = true
}

const saveKnowledgeBaseSettings = async () => {
  if (!settingsKnowledgeBaseId.value) return

  // 验证设置参数
  if (knowledgeBaseSettings.value.chunk_size < 100 || knowledgeBaseSettings.value.chunk_size > 4000) {
    showAlert('chunk_size 必须在 100-4000 之间', '参数错误', 'warning')
    return
  }

  if (knowledgeBaseSettings.value.chunk_overlap < 0 || knowledgeBaseSettings.value.chunk_overlap > 500) {
    showAlert('chunk_overlap 必须在 0-500 之间', '参数错误', 'warning')
    return
  }

  if (knowledgeBaseSettings.value.chunk_overlap >= knowledgeBaseSettings.value.chunk_size) {
    showAlert('chunk_overlap 不能大于或等于 chunk_size', '参数错误', 'warning')
    return
  }

  isSavingSettings.value = true
  try {
    const response = await KnowledgeAPI.updateKnowledgeBaseSettings(
        settingsKnowledgeBaseId.value,
        knowledgeBaseSettings.value
    )

    if (response.success) {
      showSettingsModal.value = false
      showAlert('设置保存成功', '成功', 'success')
    } else {
      showAlert('保存设置失败: ' + response.message, '错误', 'error')
    }
  } catch (error) {
    console.error('保存设置失败:', error)
    showAlert('保存设置失败: ' + (error as Error).message, '错误', 'error')
  } finally {
    isSavingSettings.value = false
  }
}

const addSplitChar = () => {
  knowledgeBaseSettings.value.split_chars.push('')
}

const removeSplitChar = (index: number) => {
  knowledgeBaseSettings.value.split_chars.splice(index, 1)
}

// 显示拆分字符的可读形式
const displaySplitChar = (char: string) => {
  if (char === '\n') return '\\n'
  if (char === '\n\n') return '\\n\\n'
  if (char === '\t') return '\\t'
  if (char === '\r') return '\\r'
  if (char === '\r\n') return '\\r\\n'
  return char
}

// 更新拆分字符，将可读形式转换回实际字符
const updateSplitChar = (index: number, value: string) => {
  let actualChar = value
  if (value === '\\n') actualChar = '\n'
  else if (value === '\\n\\n') actualChar = '\n\n'
  else if (value === '\\t') actualChar = '\t'
  else if (value === '\\r') actualChar = '\r'
  else if (value === '\\r\\n') actualChar = '\r\n'
  
  knowledgeBaseSettings.value.split_chars[index] = actualChar
}

const refreshDocuments = async (page: number = 1) => {
  if (!selectedKnowledgeBase.value) return

  console.log('正在刷新知识库数据...', {
    knowledgeBaseId: selectedKnowledgeBase.value.id,
    knowledgeBaseName: selectedKnowledgeBase.value.name,
    page: page,
    pageSize: pageSize.value
  })

  isLoadingDocuments.value = true

  try {
    // 计算API请求的offset
    const offset = (page - 1) * pageSize.value

    // 使用KnowledgeAPI获取知识库数据片段，只获取当前页需要的数据
    console.log('调用API:', `KnowledgeAPI.getKnowledgeBaseData(${selectedKnowledgeBase.value.id}, ${pageSize.value}, ${offset})`)
    const response = await KnowledgeAPI.getKnowledgeBaseData(
        selectedKnowledgeBase.value.id,
        pageSize.value, // 只获取当前页的数据量
        offset
    )
    console.log('知识库数据API响应:', response)

    if (response.success && response.data && response.data.chunks) {
      knowledgeData.value = response.data.chunks
      totalItems.value = response.data.total || response.data.chunks.length
      currentPage.value = page

      console.log('✓ 成功从API加载数据:', {
        count: knowledgeData.value.length,
        total: totalItems.value,
        currentPage: currentPage.value,
        totalPages: totalPages.value,
        firstItem: knowledgeData.value[0]
      })
    } else {
      console.warn('API响应格式不正确，使用模拟数据', response)
      // 生成分页的模拟数据
      const allMockData = generateMockData()
      const startIndex = (page - 1) * pageSize.value
      const endIndex = startIndex + pageSize.value
      knowledgeData.value = allMockData.slice(startIndex, endIndex)
      totalItems.value = allMockData.length
      currentPage.value = page
      console.log('使用模拟数据:', knowledgeData.value.length, '个片段，总计:', totalItems.value)
    }
  } catch (error) {
    console.error('获取知识库数据失败，使用模拟数据:', error)
    // 生成分页的模拟数据
    const allMockData = generateMockData()
    const startIndex = (page - 1) * pageSize.value
    const endIndex = startIndex + pageSize.value
    knowledgeData.value = allMockData.slice(startIndex, endIndex)
    totalItems.value = allMockData.length
    currentPage.value = page
    console.log('备用模拟数据:', knowledgeData.value.length, '个片段，总计:', totalItems.value)
  } finally {
    isLoadingDocuments.value = false
    console.log('数据加载完成，当前数据数量:', knowledgeData.value.length)
  }
}

// 生成模拟数据用于演示
const generateMockData = () => {
  if (!selectedKnowledgeBase.value) return []

  const baseData = [
    {
      title: '产品功能介绍',
      content: '这是一个重要的知识点，包含了关于产品功能的详细描述。它解释了如何使用系统的核心功能，包括用户界面导航、数据输入验证、以及常见问题的解决方案。',
      source: '产品手册.pdf',
      type: 'TEXT'
    },
    {
      title: '用户操作指南',
      content: '用户指南中提到的重要操作步骤，包括登录、设置和基本操作流程。这些步骤对新用户尤其重要，能够帮助他们快速上手使用系统。',
      source: '用户指南.docx',
      type: 'TEXT'
    },
    {
      title: '系统技术架构',
      content: '系统架构的详细技术说明，包括数据库设计、API接口规范和安全配置要求。这部分内容主要面向技术人员，提供了系统实现的详细信息。',
      source: '技术文档.md',
      type: 'TECHNICAL'
    },
    {
      title: '常见问题解答',
      content: '用户在使用过程中遇到的常见问题及其解决方案。包括登录问题、数据同步问题、权限设置问题等。',
      source: 'FAQ.pdf',
      type: 'FAQ'
    },
    {
      title: '安全策略规范',
      content: '系统的安全策略和最佳实践，包括密码策略、访问控制、数据加密和备份策略。这些策略确保了系统的安全性和可靠性。',
      source: '安全手册.pdf',
      type: 'SECURITY'
    },
    {
      title: '数据库配置',
      content: '详细的数据库配置说明，包括连接参数、索引优化、性能调优等内容。这些配置对系统性能有重要影响。',
      source: '数据库文档.md',
      type: 'TECHNICAL'
    },
    {
      title: 'API接口文档',
      content: 'RESTful API接口的详细说明，包括请求格式、响应结构、错误码定义等。开发者可以根据此文档进行集成开发。',
      source: 'API文档.json',
      type: 'TECHNICAL'
    },
    {
      title: '部署指南',
      content: '系统部署的完整流程，包括环境准备、依赖安装、配置文件设置、服务启动等步骤。',
      source: '部署手册.md',
      type: 'GUIDE'
    }
  ]

  // 生成25个模拟数据项以测试分页
  const mockData = []
  for (let i = 0; i < 25; i++) {
    const baseItem = baseData[i % baseData.length]
    mockData.push({
      id: String(i + 1),
      title: `${baseItem.title} #${i + 1}`,
      content: `${baseItem.content} (数据条目 ${i + 1})`,
      source: baseItem.source,
      type: baseItem.type,
      chunk_index: (i % 5) + 1,
      word_count: Math.floor(Math.random() * 200) + 50,
      score: Math.random() * 0.3 + 0.7, // 0.7-1.0之间的随机分数
      created_at: new Date(Date.now() - Math.random() * 86400000 * 30).toISOString() // 最近30天内的随机日期
    })
  }

  return mockData
}


const performSearch = async (page: number = 1) => {
  console.log('执行搜索:', {
    query: dataContentSearchQuery.value,
    hasKnowledgeBase: !!selectedKnowledgeBase.value,
    page: page
  })

  if (!selectedKnowledgeBase.value) {
    console.log('没有选择知识库')
    return
  }

  // 如果搜索词为空，清空搜索结果并恢复正常浏览
  if (!dataContentSearchQuery.value.trim()) {
    searchResults.value = []
    currentPage.value = 1
    await refreshDocuments(1)
    console.log('搜索词为空，恢复正常浏览模式')
    return
  }

  isLoadingDocuments.value = true

  try {
    // 计算偏移量
    const offset = (page - 1) * pageSize.value

    // 使用 getKnowledgeBaseData 方法进行搜索，直接支持分页
    console.log('调用搜索API:', `KnowledgeAPI.getKnowledgeBaseData(${selectedKnowledgeBase.value.id}, ${pageSize.value}, ${offset}, "${dataContentSearchQuery.value}")`)
    const response = await KnowledgeAPI.getKnowledgeBaseData(
        selectedKnowledgeBase.value.id,
        pageSize.value,
        offset,
        dataContentSearchQuery.value
    )

    if (response.success && response.data && response.data.chunks) {
      // 搜索模式下，直接使用API返回的分页数据
      knowledgeData.value = response.data.chunks
      totalItems.value = response.data.total || response.data.chunks.length
      currentPage.value = page

      // 清空搜索结果数组，因为现在直接使用knowledgeData
      searchResults.value = []

      console.log('✓ 搜索API成功:', {
        query: dataContentSearchQuery.value,
        resultCount: knowledgeData.value.length,
        total: totalItems.value,
        currentPage: currentPage.value
      })
    } else {
      console.warn('搜索API响应格式不正确，使用模拟数据', response)
      // 使用模拟数据进行搜索
      const allMockData = generateMockData()
      const filteredData = allMockData.filter(item => {
        const searchLower = dataContentSearchQuery.value.toLowerCase()
        const content = item.content.toLowerCase()
        const title = item.title.toLowerCase()
        const source = item.source.toLowerCase()

        return content.includes(searchLower) ||
            title.includes(searchLower) ||
            source.includes(searchLower)
      })

      // 分页处理
      const startIndex = (page - 1) * pageSize.value
      const endIndex = startIndex + pageSize.value
      knowledgeData.value = filteredData.slice(startIndex, endIndex)
      totalItems.value = filteredData.length
      currentPage.value = page
      searchResults.value = []
    }

    console.log('搜索完成:', {
      query: dataContentSearchQuery.value,
      resultCount: knowledgeData.value.length,
      total: totalItems.value
    })
  } catch (error) {
    console.error('搜索失败，使用模拟数据:', error)
    // 备用模拟数据搜索
    const allMockData = generateMockData()
    const filteredData = allMockData.filter(item => {
      const searchLower = dataContentSearchQuery.value.toLowerCase()
      const content = item.content.toLowerCase()
      const title = item.title.toLowerCase()
      const source = item.source.toLowerCase()

      return content.includes(searchLower) ||
          title.includes(searchLower) ||
          source.includes(searchLower)
    })

    // 分页处理
    const startIndex = (page - 1) * pageSize.value
    const endIndex = startIndex + pageSize.value
    knowledgeData.value = filteredData.slice(startIndex, endIndex)
    totalItems.value = filteredData.length
    currentPage.value = page
    searchResults.value = []
  } finally {
    isLoadingDocuments.value = false
  }
}

const viewDataDetail = (item: any) => {
  // 显示数据详情模态框
  console.log('查看数据详情:', item)
  // 这里可以实现详情查看功能
  showAlert(`标题: ${item.title}\n来源: ${item.source}\n内容: ${item.content}`, '数据详情')
}

const removeDataItem = async (item: any) => {
  showConfirm(
    '确定要删除这个数据片段吗？',
    '确认删除',
    async () => {
      try {
        // 调用API删除数据片段
        // await KnowledgeAPI.removeDataChunk(selectedKnowledgeBase.value.id, item.id)

        // 从本地数组中移除
        const index = knowledgeData.value.findIndex(data => data.id === item.id)
        if (index > -1) {
          knowledgeData.value.splice(index, 1)
        }

        showAlert('数据片段删除成功', '成功', 'success')
        console.log('数据片段已删除')
      } catch (error) {
        console.error('删除数据片段失败:', error)
        showAlert('删除数据片段失败: ' + (error as Error).message, '错误', 'error')
      }
    }
  )
}


// 工具方法
const getStatusText = (status: string) => {
  const statusMap = {
    'active': '活跃',
    'inactive': '非活跃',
    'building': '构建中'
  }
  return statusMap[status as keyof typeof statusMap] || status
}

// 获取知识库类型信息
const getKnowledgeBaseTypeInfo = (kbId: string) => {
  const indexType = knowledgeBaseTypes.value.get(kbId) || 'vector'
  
  const typeConfig = {
    'vector': {
      name: '向量索引',
      icon: 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
      color: 'blue',
      bgClass: 'bg-blue-50',
      textClass: 'text-blue-700',
      borderClass: 'border-blue-200'
    },
    'knowledge_graph': {
      name: '知识图谱',
      icon: 'M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9',
      color: 'purple',
      bgClass: 'bg-purple-50',
      textClass: 'text-purple-700',
      borderClass: 'border-purple-200'
    },
    'long_document': {
      name: '长文档',
      icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
      color: 'green',
      bgClass: 'bg-green-50',
      textClass: 'text-green-700',
      borderClass: 'border-green-200'
    }
  }
  
  return typeConfig[indexType as keyof typeof typeConfig] || typeConfig.vector
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

// 文件相关工具函数
const getFileType = (fileName: string) => {
  const ext = fileName.split('.').pop()?.toLowerCase()
  if (['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'].includes(ext || '')) return 'image'
  if (ext === 'pdf') return 'pdf'
  if (['txt', 'md', 'json', 'csv', 'xml'].includes(ext || '')) return 'text'
  return 'other'
}

// 生命周期
onMounted(() => {
  refreshKnowledgeBases()
})
</script>

<style scoped>
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

/* 自定义滚动条样式 */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
  transition: background-color 0.2s ease;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background-color: rgba(107, 114, 128, 0.8);
}

/* 分页控件样式优化 */
.pagination-container {
  background: rgba(249, 250, 251, 0.8);
  backdrop-filter: blur(4px);
}

/* 页码按钮悬停效果 */
.page-button {
  transition: all 0.2s ease;
}

.page-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.page-button:active:not(:disabled) {
  transform: translateY(0);
}

/* 当前页码按钮特殊样式 */
.page-button.active {
  background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
  box-shadow: 0 2px 8px rgba(31, 41, 55, 0.3);
}

/* 分页信息文字样式 */
.pagination-info {
  font-variant-numeric: tabular-nums;
}

/* 每页数量选择器样式 */
.page-size-selector {
  background: white;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.page-size-selector:focus {
  border-color: #1f2937;
  box-shadow: 0 0 0 3px rgba(31, 41, 55, 0.1);
}

/* 跳转输入框样式 */
.jump-input {
  background: white;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
}

.jump-input:focus {
  border-color: #1f2937;
  box-shadow: 0 0 0 3px rgba(31, 41, 55, 0.1);
}

/* 抽屉动画效果 */
.drawer-enter-active,
.drawer-leave-active {
  transition: all 0.3s ease;
}

.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
}

.drawer-enter-from .bg-white,
.drawer-leave-to .bg-white {
  transform: translateX(100%);
}

.drawer-enter-active .bg-white,
.drawer-leave-active .bg-white {
  transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* 背景遮罩动画 */
.drawer-enter-from .bg-black,
.drawer-leave-to .bg-black {
  opacity: 0;
}

.drawer-enter-active .bg-black,
.drawer-leave-active .bg-black {
  transition: opacity 0.3s ease;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .pagination-container {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .pagination-controls {
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem;
  }

  .pagination-info {
    text-align: center;
  }
}
</style> 