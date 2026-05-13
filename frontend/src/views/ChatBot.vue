<template>
  <div class="h-screen bg-gray-50 flex overflow-hidden">
    <!-- 左侧会话管理面板 -->
    <div class="w-80 bg-white border-r border-gray-200 flex flex-col">
      <!-- 会话面板头部 -->
      <div class="p-6 border-b border-gray-100">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 bg-gray-900 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
              </svg>
            </div>
            <div>
              <h2 class="text-lg font-medium text-gray-900">会话历史</h2>
              <p class="text-sm text-gray-500">管理对话记录</p>
            </div>
          </div>
          <button
              @click="createNewSession"
              class="text-gray-600 hover:text-gray-900 p-2 rounded-lg hover:bg-gray-100 transition-colors"
              title="新建会话"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
          </button>
        </div>

        <!-- 搜索框 -->
        <div class="relative">
          <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索会话..."
              class="w-full px-3 py-2 pl-9 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-transparent outline-none bg-gray-50"
          />
          <svg class="w-4 h-4 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" fill="none"
               stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
        </div>
      </div>

      <!-- 会话列表 -->
      <div class="flex-1 overflow-y-auto min-h-0">
        <div v-if="isLoadingSessions" class="p-6 text-center text-gray-500">
          <div class="animate-spin w-5 h-5 border-2 border-gray-400 border-t-transparent rounded-full mx-auto mb-2"></div>
          <span class="text-sm">加载中...</span>
        </div>

        <div v-else-if="filteredSessions.length === 0" class="p-6 text-center text-gray-500">
          <div class="w-12 h-12 mx-auto mb-4 bg-gray-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
            </svg>
          </div>
          <p class="text-sm">{{ searchQuery ? '未找到匹配的会话' : '暂无会话历史' }}</p>
        </div>

        <div v-else class="p-4">
          <div
              v-for="session in filteredSessions"
              :key="session.id"
              @click="switchSession(session.id)"
              class="group relative p-4 mb-3 rounded-lg cursor-pointer transition-all duration-200 border"
              :class="{
              'bg-gray-900 text-white border-gray-900': session.id === currentSessionId,
              'bg-white hover:bg-gray-50 border-gray-200': session.id !== currentSessionId
            }"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1 min-w-0">
                <!-- 会话标题 -->
                <div class="flex items-center space-x-2 mb-2">
                  <div
                      class="w-2 h-2 rounded-full flex-shrink-0"
                      :class="session.id === currentSessionId ? 'bg-green-400' : 'bg-gray-400'"
                  ></div>
                  <h3 class="text-sm font-medium line-clamp-1"
                      :class="session.id === currentSessionId ? 'text-white' : 'text-gray-900'">
                    {{ getSessionTitle(session) }}
                  </h3>
                </div>

                <!-- 最后消息预览 -->
                <p class="text-xs line-clamp-2 mb-2" v-if="session.last_message"
                   :class="session.id === currentSessionId ? 'text-gray-300' : 'text-gray-500'">
                  {{ session.last_message }}
                </p>

                <!-- 会话信息 -->
                <div class="flex items-center justify-between text-xs"
                     :class="session.id === currentSessionId ? 'text-gray-400' : 'text-gray-400'">
                  <div class="flex items-center space-x-2">
                    <span>{{ session.message_count }} 条消息</span>
                    <span>•</span>
                    <span>{{ formatRelativeTime(session.last_activity) }}</span>
                    <!-- 知识库指示器 -->
                    <span v-if="session.knowledge_base_ids && session.knowledge_base_ids.length > 0"
                          class="flex items-center space-x-1">
                      <span>•</span>
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M19 11H5m14-4h-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5H17m-2.5 7h-2.5m5 4h-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5H17m-2.5 7h-2.5"></path>
                      </svg>
                      <span>{{ session.knowledge_base_ids.length }}个库</span>
                    </span>
                  </div>
                </div>
              </div>

              <!-- 删除按钮 -->
              <button
                  @click="deleteSession(session.id, $event)"
                  class="opacity-0 group-hover:opacity-100 p-1.5 rounded-lg transition-all duration-200"
                  :class="session.id === currentSessionId ? 'text-gray-400 hover:text-red-400 hover:bg-red-900/20' : 'text-gray-400 hover:text-red-600 hover:bg-red-50'"
                  title="删除会话"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 面板底部操作 -->
      <div class="p-6 border-t border-gray-100">
        <div class="flex items-center justify-between text-xs text-gray-500">
          <span>{{ filteredSessions.length }} 个会话</span>
          <button
              @click="loadSessions"
              class="text-gray-600 hover:text-gray-900 transition-colors"
              title="刷新会话列表"
          >
            刷新
          </button>
        </div>
      </div>
    </div>

    <!-- 中间主要内容区域 -->
    <div class="flex-1 flex flex-col relative overflow-hidden">
      <!-- 页面头部 -->
      <div class="bg-white border-b border-gray-200 flex-shrink-0">
        <div class="px-8 py-6">
          <div class="flex items-center justify-between">
            <!-- 左侧标题 -->
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-gray-900 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                </svg>
              </div>
              <div>
                <h1 class="text-3xl font-light text-gray-900">
                  {{ currentSession ? getSessionTitle(currentSession) : 'AI 智能对话' }}
                </h1>
                <p class="text-gray-500">
                  {{ currentSession ? `${currentSession.message_count} 条消息` : '与AI助手进行智能对话，获取文档相关答案' }}
                </p>
              </div>
            </div>

            <!-- 右侧统计信息 -->
            <div class="flex items-center space-x-8">
              <div class="flex items-center space-x-6 text-sm">
                <div class="text-center">
                  <div class="text-2xl font-light text-gray-900">{{ messages.length }}</div>
                  <div class="text-gray-400 uppercase tracking-wide text-xs">当前对话</div>
                </div>
                <div class="text-center">
                  <div class="text-2xl font-light" :class="isLoading ? 'text-orange-500' : 'text-green-500'">
                    {{ isLoading ? '思考中' : '在线' }}
                  </div>
                  <div class="text-gray-400 uppercase tracking-wide text-xs">AI状态</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 聊天内容区域 -->
      <div class="flex-1 px-8 py-8 bg-gray-50 overflow-hidden">
        <div class="max-w-6xl mx-auto bg-white rounded-xl border border-gray-200 shadow-sm h-full flex flex-col">
          <!-- 消息列表容器 -->
          <div class="flex-1 overflow-y-auto p-8 pb-6 min-h-0 scroll-smooth" ref="messagesContainer">
            <!-- 欢迎消息 -->
            <div v-if="messages.length === 0" class="text-center py-16">
              <div class="w-16 h-16 mx-auto mb-6 bg-gray-100 rounded-xl flex items-center justify-center">
                <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
                </svg>
              </div>
              <h3 class="text-xl font-medium text-gray-900 mb-3">
                {{ currentSession ? '继续您的对话' : '欢迎使用AI智能助手' }}
              </h3>
              <p class="text-gray-500 mb-6">您可以询问关于已上传文档的任何问题，我会基于文档内容为您提供准确答案。</p>

              <!-- 知识库状态提示 -->
              <div class="mb-6">
                <div v-if="selectedKnowledgeBases.length > 0"
                     class="inline-flex items-center space-x-2 px-4 py-2 bg-blue-50 text-blue-700 rounded-lg">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span class="text-sm font-medium">
                    已选择 {{ selectedKnowledgeBases.length }} 个知识库，AI将基于这些内容回答问题
                  </span>
                </div>

                <div v-else class="inline-flex items-center space-x-2 px-4 py-2 bg-orange-50 text-orange-700 rounded-lg">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span class="text-sm font-medium">
                    未选择特定知识库，只能使用模型自身知识进行问答
                  </span>
                </div>
              </div>

              <div class="flex flex-wrap justify-center gap-2">
                <span
                    class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-700">文档问答</span>
                <span
                    class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-700">智能分析</span>
                <span
                    class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-700">内容总结</span>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-700">知识库检索</span>
              </div>
            </div>

            <!-- 聊天消息 -->
            <div class="space-y-4">
              <div
                  v-for="message in messages"
                  :key="message.id"
                  class="flex"
                  :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
              >
                <div
                    class="max-w-4xl px-4 py-3 rounded-lg shadow-sm transition-all duration-200"
                    :class="message.role === 'user'
                    ? 'bg-gray-900 text-white ml-16' 
                    : 'bg-gray-50 text-gray-900 border border-gray-200 mr-16'"
                >
                  <div class="flex items-start space-x-3">
                    <!-- AI头像 -->
                    <div
                        v-if="message.role === 'assistant'"
                        class="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center flex-shrink-0 mt-1"
                    >
                      <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                      </svg>
                    </div>

                    <div class="flex-1">
                      <div class="prose prose-sm max-w-none">
                        <!-- 对于用户消息，使用简单的文本显示 -->
                        <p v-if="message.role === 'user'" class="mb-0 leading-relaxed whitespace-pre-wrap">{{
                            message.content
                          }}</p>
                        <!-- 对于AI回复，使用Markdown渲染 -->
                        <MarkdownRenderer v-else :content="message.content"/>
                      </div>
                      <p
                          class="text-xs mt-2 opacity-70"
                          :class="message.role === 'user' ? 'text-gray-300' : 'text-gray-500'"
                      >
                        {{ formatTime(new Date(message.timestamp)) }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 加载中提示 -->
              <div v-if="isLoading" class="flex justify-start">
                <div class="bg-gray-50 border border-gray-200 text-gray-900 max-w-4xl px-4 py-3 rounded-lg shadow-sm mr-16">
                  <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center">
                      <svg class="w-4 h-4 text-white animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                      </svg>
                    </div>
                    <div class="flex items-center space-x-2">
                      <span class="text-sm text-gray-600">AI正在思考</span>
                      <div class="flex space-x-1">
                        <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                        <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 输入区域 -->
          <div class="flex-shrink-0 bg-gray-50 rounded-lg border border-gray-200 p-6 m-8 mt-0">
            <form @submit.prevent="sendMessage" class="flex space-x-3">
              <div class="flex-1 relative">
                <input
                    v-model="currentMessage"
                    type="text"
                    placeholder="输入您的问题..."
                    class="w-full px-4 py-3 pr-16 border border-gray-200 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-transparent outline-none bg-white transition-all duration-200"
                    :disabled="isLoading"
                />
                <!-- 清除按钮 -->
                <button
                    v-if="currentMessage"
                    type="button"
                    @click="currentMessage = ''"
                    class="absolute right-12 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 p-1 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
                <!-- 发送按钮（在输入框内） -->
                <button
                    type="submit"
                    :disabled="!currentMessage.trim() || isLoading"
                    class="absolute right-2 top-1/2 transform -translate-y-1/2 bg-gray-900 hover:bg-gray-800 disabled:bg-gray-400 text-white p-2 rounded-lg transition-all duration-200"
                >
                  <svg
                      v-if="isLoading"
                      class="w-4 h-4 animate-spin"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                  </svg>
                  <svg
                      v-else
                      class="w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                          d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                  </svg>
                </button>
              </div>
            </form>

            <!-- 快速提示 -->
            <div class="mt-4 space-y-3">
              <!-- 知识库使用提示 -->
              <div v-if="selectedKnowledgeBases.length > 0" class="flex items-center space-x-2 text-xs text-gray-600">
                <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                <span>
                  将从 {{ selectedKnowledgeBases.length }} 个知识库中检索相关信息：
                  <strong>{{ selectedKnowledgeBases.map(id => getKnowledgeBaseName(id)).join('、') }}</strong>
                </span>
              </div>

              <div v-else class="flex items-center space-x-2 text-xs text-orange-600">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L3.314 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                </svg>
                <span>未选择知识库，只能使用模型自身知识进行问答</span>
              </div>

              <!-- 快速提示按钮 -->
              <div class="flex flex-wrap gap-2">
                <button
                    v-for="suggestion in quickSuggestions"
                    :key="suggestion"
                    @click="currentMessage = suggestion"
                    class="text-sm px-3 py-1 bg-white border border-gray-200 rounded-full hover:bg-gray-100 hover:border-gray-300 transition-all duration-200"
                >
                  {{ suggestion }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 右侧知识库管理面板 -->
    <div class="w-96 bg-white border-l border-gray-200 flex flex-col">
      <!-- 知识库面板头部 -->
      <div class="p-6 border-b border-gray-100">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 bg-gray-900 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M19 11H5m14-4h-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5H17m-2.5 7h-2.5m5 4h-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5H17m-2.5 7h-2.5"></path>
              </svg>
            </div>
            <div>
              <h2 class="text-lg font-medium text-gray-900">知识库管理</h2>
              <p class="text-sm text-gray-500">为当前会话选择知识库</p>
            </div>
          </div>
          <button
              @click="loadKnowledgeBases"
              class="text-gray-600 hover:text-gray-900 p-2 rounded-lg hover:bg-gray-100 transition-colors"
              title="刷新知识库列表"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
          </button>
        </div>

        <!-- 选择状态概览 -->
        <div class="relative">
          <input
              v-model="knowledgeBaseSearch"
              type="text"
              placeholder="搜索知识库..."
              class="w-full px-3 py-2 pl-9 text-sm border border-gray-200 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-transparent outline-none bg-gray-50"
          />
          <svg class="w-4 h-4 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" fill="none"
               stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
        </div>
      </div>

      <!-- 知识库列表 -->
      <div class="flex-1 overflow-y-auto min-h-0">
        <div v-if="isLoadingKnowledgeBases" class="p-6 text-center text-gray-500">
          <div class="animate-spin w-5 h-5 border-2 border-gray-400 border-t-transparent rounded-full mx-auto mb-2"></div>
          <span class="text-sm">加载中...</span>
        </div>

        <div v-else-if="filteredKnowledgeBases.length === 0" class="p-6 text-center text-gray-500">
          <div class="w-12 h-12 mx-auto mb-4 bg-gray-100 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M19 11H5m14-4h-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5H17m-2.5 7h-2.5m5 4h-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5H17m-2.5 7h-2.5"></path>
            </svg>
          </div>
          <p class="text-sm">{{ knowledgeBaseSearch ? '未找到匹配的知识库' : '暂无可用知识库' }}</p>
        </div>

        <div v-else class="p-4">
          <!-- 全选控制 -->
          <div class="mb-3 p-4 rounded-lg cursor-pointer transition-all duration-200 border"
               :class="selectedKnowledgeBases.length === filteredKnowledgeBases.length ? 'bg-gray-900 text-white border-gray-900' : 'bg-white hover:bg-gray-50 border-gray-200'"
               @click="toggleAllKnowledgeBases">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div
                    class="w-2 h-2 rounded-full flex-shrink-0"
                    :class="selectedKnowledgeBases.length === filteredKnowledgeBases.length ? 'bg-green-400' : 'bg-gray-400'"
                ></div>
                <div class="flex-1 min-w-0">
                  <h3 class="text-sm font-medium line-clamp-1"
                      :class="selectedKnowledgeBases.length === filteredKnowledgeBases.length ? 'text-white' : 'text-gray-900'">
                    全部知识库
                  </h3>
                  <p class="text-xs line-clamp-1"
                     :class="selectedKnowledgeBases.length === filteredKnowledgeBases.length ? 'text-gray-300' : 'text-gray-500'">
                    {{ selectedKnowledgeBases.length === filteredKnowledgeBases.length ? '已全选' : '点击全选所有知识库' }}
                  </p>
                </div>
              </div>
              <div class="flex items-center space-x-2 text-xs"
                   :class="selectedKnowledgeBases.length === filteredKnowledgeBases.length ? 'text-gray-400' : 'text-gray-400'">
                <span>{{ selectedKnowledgeBases.length }}/{{ filteredKnowledgeBases.length }}</span>
              </div>
            </div>
          </div>

          <!-- 知识库项目 -->
          <div
              v-for="kb in filteredKnowledgeBases"
              :key="kb.id"
              @click="toggleKnowledgeBase(kb.id)"
              class="group relative p-4 mb-3 rounded-lg cursor-pointer transition-all duration-200 border"
              :class="{
              'bg-gray-900 text-white border-gray-900': selectedKnowledgeBases.includes(kb.id),
              'bg-white hover:bg-gray-50 border-gray-200': !selectedKnowledgeBases.includes(kb.id)
            }"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1 min-w-0">
                <!-- 知识库标题 -->
                <div class="flex items-center space-x-2 mb-2">
                  <div
                      class="w-2 h-2 rounded-full flex-shrink-0"
                      :class="selectedKnowledgeBases.includes(kb.id) ? 'bg-green-400' : (kb.status === 'active' ? 'bg-green-500' : 'bg-gray-400')"
                  ></div>
                  <h3 class="text-sm font-medium line-clamp-1"
                      :class="selectedKnowledgeBases.includes(kb.id) ? 'text-white' : 'text-gray-900'">
                    {{ kb.name }}
                  </h3>
                  <span
                      class="inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium flex-shrink-0"
                      :class="selectedKnowledgeBases.includes(kb.id)
                      ? (kb.status === 'active' ? 'bg-green-900/30 text-green-300' : 'bg-gray-700 text-gray-300')
                      : (kb.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600')"
                  >
                    {{ kb.status === 'active' ? '可用' : '不可用' }}
                  </span>
                </div>

                <!-- 知识库描述 -->
                <p class="text-xs line-clamp-2 mb-2" v-if="kb.description"
                   :class="selectedKnowledgeBases.includes(kb.id) ? 'text-gray-300' : 'text-gray-500'">
                  {{ kb.description }}
                </p>

                <!-- 知识库统计 -->
                <div class="flex items-center justify-between text-xs"
                     :class="selectedKnowledgeBases.includes(kb.id) ? 'text-gray-400' : 'text-gray-400'">
                  <div class="flex items-center space-x-2">
                    <div class="flex items-center space-x-1">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                      </svg>
                      <span>{{ kb.document_count }} 文档</span>
                    </div>
                    <span>•</span>
                    <div class="flex items-center space-x-1">
                      <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                              d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                      </svg>
                      <span>{{ formatFileSize(kb.size) }}</span>
                    </div>
                    <span>•</span>
                    <span>{{ formatRelativeTime(kb.updated_at || kb.created_at) }}</span>
                  </div>
                </div>
              </div>

              <!-- 选择指示器 -->
              <div class="ml-3 flex-shrink-0">
                <div
                    class="w-5 h-5 rounded-full border-2 flex items-center justify-center transition-all duration-200"
                    :class="selectedKnowledgeBases.includes(kb.id)
                    ? 'border-green-400 bg-green-400' 
                    : 'border-gray-300 group-hover:border-gray-400'"
                >
                  <svg
                      v-if="selectedKnowledgeBases.includes(kb.id)"
                      class="w-3 h-3 text-white"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                  >
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {computed, nextTick, onMounted, ref, watch} from 'vue'
import {ChatAPI, type ChatMessage, type ChatSession} from '@/api/chat'
import {getKnowledgeBases, type KnowledgeBase} from '@/api/knowledge'
import MarkdownRenderer from '@/components/MarkdownRenderer.vue'

// 使用ChatMessage类型
type Message = ChatMessage

// 响应式数据
const messages = ref<Message[]>([])
const currentMessage = ref('')
const isLoading = ref(false)
const messagesContainer = ref<HTMLElement>()
const currentSessionId = ref<string | null>(null)
const sessions = ref<ChatSession[]>([])
const isLoadingSessions = ref(false)
const searchQuery = ref('')
const knowledgeBases = ref<KnowledgeBase[]>([])
const selectedKnowledgeBases = ref<string[]>([])
const isLoadingKnowledgeBases = ref(false)
const knowledgeBaseSearch = ref('')

// 计算属性
const currentSession = computed(() => {
  return sessions.value.find(s => s.id === currentSessionId.value)
})

// 过滤会话列表
const filteredSessions = computed(() => {
  if (!searchQuery.value.trim()) {
    return sessions.value
  }

  const query = searchQuery.value.toLowerCase()
  return sessions.value.filter(session =>
      (session.last_message && session.last_message.toLowerCase().includes(query)) ||
      getSessionTitle(session).toLowerCase().includes(query)
  )
})

// 快速提示建议
const quickSuggestions = ref([
  '总结一下文档内容',
  '这个文档的主要观点是什么？',
  '有什么关键信息需要注意？',
  '请用列表格式列出要点',
  '请详细分析并用标题分段说明'
])

// 生成唯一ID
const generateId = () => Math.random().toString(36).substr(2, 9)

// 获取会话标题
const getSessionTitle = (session: ChatSession): string => {
  if (session.last_message) {
    // 取最后一条消息的前30个字符作为标题
    const title = session.last_message.replace(/\n/g, ' ').trim()
    return title.length > 30 ? title.substring(0, 30) + '...' : title
  }

  // 如果没有消息，使用创建时间生成标题
  const date = new Date(session.created_at)
  return `新对话 ${date.toLocaleDateString('zh-CN', {month: 'short', day: 'numeric'})}`
}

// 格式化时间
const formatTime = (date: Date) => {
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 格式化相对时间
const formatRelativeTime = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`

  return date.toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric'
  })
}

// 滚动到底部
const scrollToBottom = async (smooth: boolean = true) => {
  // 等待DOM更新完成
  await nextTick()
  
  // 延迟一小段时间确保所有内容都已渲染
  await new Promise(resolve => setTimeout(resolve, 50))
  
  if (messagesContainer.value) {
    const container = messagesContainer.value
    const scrollHeight = container.scrollHeight
    const clientHeight = container.clientHeight
    
    // 只有当内容超出容器高度时才需要滚动
    if (scrollHeight > clientHeight) {
      if (smooth) {
        // 使用平滑滚动
        container.scrollTo({
          top: scrollHeight,
          behavior: 'smooth'
        })
      } else {
        // 立即滚动
        container.scrollTop = scrollHeight
      }
    }
  }
}

// 强制滚动到底部（不使用平滑滚动）
const forceScrollToBottom = async () => {
  await scrollToBottom(false)
}

// 加载会话列表
const loadSessions = async () => {
  try {
    isLoadingSessions.value = true
    sessions.value = await ChatAPI.getSessions()
  } catch (error) {
    console.error('加载会话列表失败:', error)
  } finally {
    isLoadingSessions.value = false
  }
}

// 切换会话
const switchSession = async (sessionId: string) => {
  if (sessionId === currentSessionId.value) return // 避免重复切换

  try {
    currentSessionId.value = sessionId
    ChatAPI.setCurrentSession(sessionId)

    // 加载会话历史 - 使用数据库持久化的历史记录
    messages.value = await ChatAPI.getChatHistory(sessionId)

    // 加载会话的知识库配置
    await loadSessionKnowledgeBases(sessionId)

    await forceScrollToBottom()
  } catch (error) {
    console.error('切换会话失败:', error)
  }
}

// 创建新会话
const createNewSession = async () => {
  try {
    // 使用当前选中的知识库创建新会话
    currentSessionId.value = await ChatAPI.createNewSession(selectedKnowledgeBases.value)
    messages.value = []

    // 重新加载会话列表
    await loadSessions()
  } catch (error) {
    console.error('创建新会话失败:', error)
  }
}

// 删除会话
const deleteSession = async (sessionId: string, event: Event) => {
  event.stopPropagation() // 阻止触发切换会话

  if (!confirm('确定要删除这个会话吗？')) {
    return
  }

  try {
    await ChatAPI.deleteSession(sessionId)

    // 如果删除的是当前会话，创建新会话
    if (sessionId === currentSessionId.value) {
      await createNewSession()
    }

    // 重新加载会话列表
    await loadSessions()
  } catch (error) {
    console.error('删除会话失败:', error)
  }
}

// 发送消息
const sendMessage = async () => {
  if (!currentMessage.value.trim() || isLoading.value) return

  // 如果没有当前会话，创建新会话
  if (!currentSessionId.value) {
    await createNewSession()
  }

  const question = currentMessage.value.trim()
  currentMessage.value = ''

  // 显示用户消息
  const userMessage: Message = {
    id: generateId(),
    role: 'user',
    content: question,
    timestamp: new Date().toISOString(),
    session_id: currentSessionId.value!
  }
  messages.value.push(userMessage)

  await forceScrollToBottom()

  // 开始加载
  isLoading.value = true

  try {
    // 发送消息到AI并获取回复
    const aiResponse = await ChatAPI.sendMessage(question, currentSessionId.value!, selectedKnowledgeBases.value)

    // 添加AI回复消息
    const aiMessage: Message = {
      id: generateId(),
      role: 'assistant',
      content: aiResponse,
      timestamp: new Date().toISOString(),
      session_id: currentSessionId.value!
    }
    messages.value.push(aiMessage)

    await scrollToBottom()

    // 重新加载会话列表以更新最新活动时间
    await loadSessions()
  } catch (error) {
    console.error('发送消息失败:', error)

    // 如果API失败，显示错误消息
    const errorMessage: Message = {
      id: generateId(),
      role: 'assistant',
      content: '抱歉，我暂时无法回答您的问题。请稍后再试。',
      timestamp: new Date().toISOString(),
      session_id: currentSessionId.value!
    }
    messages.value.push(errorMessage)
    await forceScrollToBottom()
  } finally {
    isLoading.value = false
  }
}

// 监听会话列表变化，自动选择最新会话
watch(sessions, (newSessions) => {
  if (newSessions.length > 0 && !currentSessionId.value) {
    switchSession(newSessions[0].id)
  }
}, {immediate: true})

// 加载知识库列表
const loadKnowledgeBases = async () => {
  try {
    isLoadingKnowledgeBases.value = true
    const response = await getKnowledgeBases()
    knowledgeBases.value = response.data || []
  } catch (error) {
    console.error('加载知识库列表失败:', error)
  } finally {
    isLoadingKnowledgeBases.value = false
  }
}

// 加载会话的知识库配置
const loadSessionKnowledgeBases = async (sessionId: string) => {
  try {
    const knowledgeBaseIds = await ChatAPI.getSessionKnowledgeBases(sessionId)
    selectedKnowledgeBases.value = knowledgeBaseIds
  } catch (error) {
    console.error('加载会话知识库配置失败:', error)
    selectedKnowledgeBases.value = []
  }
}

// 保存当前会话的知识库配置
const saveSessionKnowledgeBases = async () => {
  if (!currentSessionId.value) return

  try {
    await ChatAPI.updateSessionKnowledgeBases(currentSessionId.value, selectedKnowledgeBases.value)
  } catch (error) {
    console.error('保存会话知识库配置失败:', error)
  }
}

// 切换所有知识库
const toggleAllKnowledgeBases = async () => {
  if (selectedKnowledgeBases.value.length < knowledgeBases.value.length) {
    selectedKnowledgeBases.value = knowledgeBases.value.map(kb => kb.id)
  } else {
    selectedKnowledgeBases.value = []
  }

  // 保存到当前会话
  await saveSessionKnowledgeBases()
}

// 监听知识库选择变化，自动保存到会话
watch(selectedKnowledgeBases, async (newValue, oldValue) => {
  // 只有在组件已经初始化完成且有当前会话时才保存
  if (currentSessionId.value && JSON.stringify(newValue) !== JSON.stringify(oldValue)) {
    await saveSessionKnowledgeBases()
  }
}, {deep: true})

// 获取知识库名称
const getKnowledgeBaseName = (id: string) => {
  const kb = knowledgeBases.value.find(kb => kb.id === id)
  return kb ? kb.name : '未知知识库'
}

// 格式化文件大小
const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 过滤知识库列表
const filteredKnowledgeBases = computed(() => {
  if (!knowledgeBaseSearch.value.trim()) {
    return knowledgeBases.value
  }

  const query = knowledgeBaseSearch.value.toLowerCase()
  return knowledgeBases.value.filter(kb =>
      kb.name.toLowerCase().includes(query) ||
      kb.description?.toLowerCase().includes(query)
  )
})

// 切换知识库
const toggleKnowledgeBase = async (id: string) => {
  if (selectedKnowledgeBases.value.includes(id)) {
    selectedKnowledgeBases.value = selectedKnowledgeBases.value.filter(i => i !== id)
  } else {
    selectedKnowledgeBases.value.push(id)
  }

  // 保存到当前会话
  await saveSessionKnowledgeBases()
}

// 组件挂载时的初始化
onMounted(async () => {
  // 加载知识库列表
  await loadKnowledgeBases()

  // 加载会话列表
  await loadSessions()

  // 如果有会话，切换到最近的会话
  if (sessions.value.length > 0) {
    await switchSession(sessions.value[0].id)
  } else {
    // 如果没有会话，创建新会话
    await createNewSession()
  }

  await forceScrollToBottom()
})

// 监听消息列表变化，自动滚动到底部
watch(messages, async (newMessages, oldMessages) => {
  // 只有当消息数量增加时才自动滚动
  if (newMessages.length > oldMessages.length) {
    await scrollToBottom()
  }
}, { deep: true })

// 监听加载状态变化，AI开始和结束思考时都滚动到底部
watch(isLoading, async (newLoading, oldLoading) => {
  // 当开始加载时（显示"AI正在思考"），立即滚动到底部
  if (!oldLoading && newLoading) {
    await scrollToBottom()
  }
  // 当结束加载时（AI回复完成），确保滚动到底部
  else if (oldLoading && !newLoading) {
    await scrollToBottom()
  }
})
</script>

<style scoped>
/* 自定义滚动条样式 */
.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(243, 244, 246, 0.5);
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(156, 163, 175, 0.5);
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(156, 163, 175, 0.7);
}

/* 确保滚动容器正确工作 */
.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) rgba(243, 244, 246, 0.5);
}

/* 平滑滚动支持 */
.scroll-smooth {
  scroll-behavior: smooth;
}

/* 确保滚动区域有正确的高度 */
.min-h-0 {
  min-height: 0;
}

/* 文本截断 */
.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 渐变文本 */
.bg-clip-text {
  -webkit-background-clip: text;
  background-clip: text;
}

/* 散文样式 */
.prose p {
  line-height: 1.6;
}

/* 动画过渡 */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style> 
