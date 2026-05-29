<template>
  <div class="flex flex-col h-screen overflow-hidden">
    <!-- 页面头部 -->
    <header class="bg-white border-b border-gray-100 flex-shrink-0">
      <div class="h-full mx-auto px-6 py-3">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 bg-gray-900 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-medium text-gray-900">AI 智能对话</h1>
              <p class="text-sm text-gray-400">基于知识库的智能问答助手</p>
            </div>
          </div>
          <div class="flex items-center space-x-4 text-xs text-gray-500">
            <div class="flex items-center space-x-1.5">
              <div class="w-1.5 h-1.5 rounded-full" :class="isLoading ? 'bg-orange-400 animate-pulse' : 'bg-green-400'"></div>
              <span>{{ isLoading ? 'AI思考中' : '在线' }}</span>
            </div>
            <span class="text-gray-300">|</span>
            <span>{{ messages.length }} 条消息</span>
          </div>
        </div>
      </div>
    </header>
    <!-- 主要内容区域 - 包含左右面板和中间聊天 -->
    <main class="h-[calc(100vh-10px)] px-6 py-4 overflow-hidden flex ">
      <!-- 左侧：会话管理面板 -->
      <div class="w-72 flex-shrink-0 max-h-[calc(100vh-180px)] bg-white rounded-xl border border-gray-100 shadow-sm flex flex-col">
        <div class="px-4 py-3 border-b border-gray-100 flex-shrink-0">
          <button
            @click="createNewSession"
            class="w-full flex items-center justify-center gap-2 px-3 py-2 bg-gray-900 hover:bg-gray-800 text-white rounded-lg text-sm font-medium transition-colors"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
            </svg>
            <span>新建会话</span>
          </button>
        </div>
        <div class="px-4 py-2 flex-shrink-0">
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索会话..."
              class="w-full px-3 py-1.5 pl-8 text-xs border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-gray-400 bg-gray-50 placeholder-gray-400"
            />
            <svg class="w-3.5 h-3.5 text-gray-400 absolute left-2.5 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
        </div>
        <div class="flex-1 min-h-0 overflow-y-auto px-3 py-2">
          <div v-if="isLoadingSessions" class="flex items-center justify-center py-10">
            <div class="w-4 h-4 border-2 border-gray-300 border-t-gray-600 rounded-full animate-spin"></div>
          </div>
          <div v-else-if="filteredSessions.length === 0" class="text-center py-10">
            <p class="text-sm text-gray-400">{{ searchQuery ? '未找到匹配的会话' : '暂无会话历史' }}</p>
          </div>
          <div v-else class="space-y-1">
            <div
              v-for="session in filteredSessions"
              :key="session.id"
              @click="switchSession(session.id)"
              class="group p-3 rounded-lg cursor-pointer transition-colors"
              :class="session.id === currentSessionId ? 'bg-gray-100' : 'hover:bg-gray-50'"
            >
              <div class="flex items-start gap-2">
                <div class="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0" :class="session.id === currentSessionId ? 'bg-gray-600' : 'bg-gray-300'"></div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-900 truncate">{{ getSessionTitle(session) }}</p>
                  <p class="text-xs text-gray-400 truncate mt-0.5" v-if="session.last_message">{{ session.last_message }}</p>
                  <p class="text-xs text-gray-400 mt-1">{{ session.message_count }}条消息 · {{ formatRelativeTime(session.last_activity) }}</p>
                </div>
              </div>
              <button
                @click="deleteSession(session.id, $event)"
                class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 p-1 rounded text-gray-400 hover:text-red-500 hover:bg-red-50 transition-all"
              >
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
        <div class="px-4 py-2 border-t border-gray-100 flex items-center justify-between text-xs text-gray-400 flex-shrink-0">
          <span>{{ sessions.length }} 个会话</span>
          <button @click="loadSessions" class="hover:text-gray-600 transition-colors">刷新</button>
        </div>
      </div>

      <!-- 中间：聊天区域 - 无卡片包裹，极简风格 -->
      <div class="flex-1 flex flex-col max-h-[calc(100vh-180px)] px-6 py-4 mb-4 overflow-hidden">
        <div class="flex-1 min-h-0 overflow-y-auto px-4 py-3" ref="messagesContainer">
          <!-- 欢迎消息 -->
          <div v-if="messages.length === 0" class="flex items-center justify-center h-full">
            <div class="text-center max-w-md">
              <div class="w-14 h-14 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-5">
                <svg class="w-7 h-7 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
                </svg>
              </div>
              <h2 class="text-lg font-medium text-gray-800 mb-2">开始新的对话</h2>
              <p class="text-sm text-gray-400 mb-6">选择知识库后向AI提问，获取精准回答</p>
              <div class="flex flex-wrap justify-center gap-2 mb-6">
                <button
                  v-for="suggestion in quickSuggestions"
                  :key="suggestion"
                  @click="currentMessage = suggestion"
                  class="text-sm px-3 py-1.5 bg-white border border-gray-200 rounded-full text-gray-600 hover:bg-gray-50 transition-colors"
                >
                  {{ suggestion }}
                </button>
              </div>
              <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs"
                :class="selectedKnowledgeBases.length > 0 ? 'bg-blue-50 text-blue-600' : 'bg-amber-50 text-amber-600'">
                <span>{{ selectedKnowledgeBases.length > 0 ? `已选择 ${selectedKnowledgeBases.length} 个知识库` : '未选择知识库' }}</span>
              </div>
            </div>
          </div>

          <!-- 聊天消息 -->
          <div v-else class="space-y-4">
            <div
              v-for="message in messages"
              :key="message.id"
              class="flex" :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
            >
              <div
                class="max-w-[80%] px-4 py-3 text-sm leading-relaxed"
                :class="message.role === 'user'
                  ? 'bg-gray-900 text-white rounded-2xl rounded-br-sm'
                  : ''"
              >
                <div class="flex items-start gap-3" v-if="message.role === 'user' || true">
                  <div v-if="message.role === 'assistant'" class="w-7 h-7 bg-indigo-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                    <svg class="w-4 h-4 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
                    </svg>
                  </div>
                  <div class="min-w-0 flex-1">
                    <template v-if="message.role === 'user'">
                      <p>{{ message.content }}</p>
                    </template>
                    <template v-else>
                      <MarkdownRenderer :content="message.content"/>
                    </template>
                    <p class="text-xs mt-1 opacity-50">{{ formatTime(new Date(message.timestamp)) }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- 加载中 -->
            <div v-if="isLoading" class="flex justify-start">
              <div class="flex items-center gap-3 px-4 py-3">
                <div class="w-7 h-7 bg-indigo-100 rounded-full flex items-center justify-center">
                  <svg class="w-4 h-4 animate-spin text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                  </svg>
                </div>
                <div class="flex items-center gap-1">
                  <div class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"></div>
                  <div class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                  <div class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="flex-shrink-0 px-4 pb-3 pt-2">
          <form @submit.prevent="sendMessage" class="bg-white rounded-xl border border-gray-200 shadow-sm flex items-center gap-2 px-4 py-3">
            <input
              v-model="currentMessage"
              type="text"
              placeholder="输入您的问题，按回车发送..."
              class="flex-1 text-sm bg-transparent outline-none placeholder-gray-400"
              :disabled="isLoading"
            />
            <button
              type="submit"
              :disabled="!currentMessage.trim() || isLoading"
              class="w-8 h-8 flex items-center justify-center bg-gray-900 hover:bg-gray-800 disabled:bg-gray-300 text-white rounded-lg transition-colors flex-shrink-0"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"/>
              </svg>
            </button>
          </form>
        </div>
      </div>  

      <!-- 右侧：知识库面板 -->
      <div class="w-72 flex-shrink-0 max-h-[calc(100vh-180px)] bg-white rounded-xl border border-gray-100 shadow-sm flex flex-col">
        <div class="px-4 py-3 border-b border-gray-100 flex-shrink-0">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2">
              <div class="w-7 h-7 bg-indigo-100 rounded-lg flex items-center justify-center">
                <svg class="w-4 h-4 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
                </svg>
              </div>
              <h2 class="text-sm font-medium text-gray-900">知识库</h2>
            </div>
            <button @click="loadKnowledgeBases" class="text-gray-400 hover:text-gray-600 transition-colors p-1 rounded hover:bg-gray-100">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
            </button>
          </div>
          <div class="relative">
            <input
              v-model="knowledgeBaseSearch"
              type="text"
              placeholder="搜索知识库..."
              class="w-full px-3 py-1.5 pl-8 text-xs border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-gray-400 bg-gray-50 placeholder-gray-400"
            />
            <svg class="w-3.5 h-3.5 text-gray-400 absolute left-2.5 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </div>
        </div>
        <div class="flex-1 min-h-0 overflow-y-auto px-3 py-2">
          <div v-if="isLoadingKnowledgeBases" class="flex items-center justify-center py-10">
            <div class="w-4 h-4 border-2 border-gray-300 border-t-indigo-600 rounded-full animate-spin"></div>
          </div>
          <div v-else-if="filteredKnowledgeBases.length === 0" class="text-center py-10">
            <p class="text-sm text-gray-400">{{ knowledgeBaseSearch ? '未找到匹配的知识库' : '暂无可用知识库' }}</p>
          </div>
          <div v-else class="space-y-1">
            <!-- 全选 -->
            <div
              @click="toggleAllKnowledgeBases"
              class="flex items-center gap-2 p-2 rounded-lg cursor-pointer transition-colors hover:bg-gray-50"
            >
              <div
                class="w-4 h-4 rounded border flex items-center justify-center flex-shrink-0 transition-colors"
                :class="selectedKnowledgeBases.length === filteredKnowledgeBases.length && filteredKnowledgeBases.length > 0
                  ? 'bg-indigo-600 border-indigo-600' : 'border-gray-300'"
              >
                <svg v-if="selectedKnowledgeBases.length === filteredKnowledgeBases.length && filteredKnowledgeBases.length > 0" class="w-2.5 h-2.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
              <span class="text-xs text-gray-600">全部知识库</span>
              <span class="text-xs text-gray-400 ml-auto">{{ selectedKnowledgeBases.length }}/{{ filteredKnowledgeBases.length }}</span>
            </div>

            <!-- 知识库项 -->
            <div
              v-for="kb in filteredKnowledgeBases"
              :key="kb.id"
              @click="kb.status !== 'building' && toggleKnowledgeBase(kb.id)"
              class="flex items-start gap-2 p-2 rounded-lg transition-colors"
              :class="kb.status === 'building' ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:bg-gray-50'"
            >
              <div
                class="w-4 h-4 rounded border flex items-center justify-center flex-shrink-0 mt-0.5 transition-colors"
                :class="selectedKnowledgeBases.includes(kb.id) ? 'bg-indigo-600 border-indigo-600' : 'border-gray-300'"
              >
                <svg v-if="selectedKnowledgeBases.includes(kb.id)" class="w-2.5 h-2.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"/>
                </svg>
              </div>
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-1.5">
                  <p class="text-sm font-medium text-gray-900 truncate">{{ kb.name }}</p>
                  <span v-if="kb.status === 'building'" class="text-xs px-1.5 py-0.5 rounded bg-yellow-50 text-yellow-600">构建中</span>
                  <span v-else class="text-xs px-1.5 py-0.5 rounded" :class="kb.status === 'active' ? 'bg-green-50 text-green-600' : 'bg-gray-100 text-gray-400'">
                    {{ kb.status === 'active' ? '可用' : '不可用' }}
                  </span>
                </div>
                <p class="text-xs text-gray-400 truncate mt-0.5">{{ kb.document_count }} 文档 · {{ formatFileSize(kb.size) }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import {computed, nextTick, onMounted, ref, watch} from 'vue'
import {ChatAPI, type ChatMessage, type ChatSession} from '@/api/chat'
import {getKnowledgeBases, type KnowledgeBase} from '@/api/knowledge'
import MarkdownRenderer from '@/components/MarkdownRenderer.vue'

type Message = ChatMessage

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

const currentSession = computed(() => sessions.value.find(s => s.id === currentSessionId.value))

const filteredSessions = computed(() => {
  if (!searchQuery.value.trim()) return sessions.value
  const query = searchQuery.value.toLowerCase()
  return sessions.value.filter(session =>
    (session.last_message && session.last_message.toLowerCase().includes(query)) ||
    getSessionTitle(session).toLowerCase().includes(query)
  )
})

const quickSuggestions = ref([
  '总结一下文档内容', '这个文档的主要观点是什么？', '有什么关键信息需要注意？', '请用列表格式列出要点'
])

const generateId = () => Math.random().toString(36).substr(2, 9)

const getSessionTitle = (session: ChatSession): string => {
  if (session.last_message) {
    const title = session.last_message.replace(/\n/g, ' ').trim()
    return title.length > 30 ? title.substring(0, 30) + '...' : title
  }
  const date = new Date(session.created_at)
  return `新对话 ${date.toLocaleDateString('zh-CN', {month: 'short', day: 'numeric'})}`
}

const formatTime = (date: Date) => {
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

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
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

const scrollToBottom = async (smooth: boolean = true) => {
  await nextTick()
  await new Promise(resolve => setTimeout(resolve, 50))
  if (messagesContainer.value) {
    const container = messagesContainer.value
    if (container.scrollHeight > container.clientHeight) {
      if (smooth) {
        container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' })
      } else {
        container.scrollTop = container.scrollHeight
      }
    }
  }
}

const forceScrollToBottom = async () => { await scrollToBottom(false) }

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

const switchSession = async (sessionId: string) => {
  if (!sessionId) return
  if (sessionId === currentSessionId.value) return
  try {
    currentSessionId.value = sessionId
    ChatAPI.setCurrentSession(sessionId)
    const history = await ChatAPI.getChatHistory(sessionId)
    messages.value = history.filter(m => m.content)
    await loadSessionKnowledgeBases(sessionId)
    await forceScrollToBottom()
  } catch (error) {
    console.error('切换会话失败:', error)
    messages.value = []
  }
}

const createNewSession = async () => {
  try {
    currentSessionId.value = await ChatAPI.createNewSession(selectedKnowledgeBases.value)
    messages.value = []
    await loadSessions()
  } catch (error) {
    console.error('创建新会话失败:', error)
  }
}

const deleteSession = async (sessionId: string, event: Event) => {
  event.stopPropagation()
  if (!confirm('确定要删除这个会话吗？')) return
  try {
    await ChatAPI.deleteSession(sessionId)
    if (sessionId === currentSessionId.value) await createNewSession()
    await loadSessions()
  } catch (error) {
    console.error('删除会话失败:', error)
  }
}

const sendMessage = async () => {
  if (!currentMessage.value.trim() || isLoading.value) return
  if (!currentSessionId.value) await createNewSession()
  const question = currentMessage.value.trim()
  currentMessage.value = ''
  const userMessage: Message = {
    id: generateId(), role: 'user', content: question,
    timestamp: new Date().toISOString(), session_id: currentSessionId.value!
  }
  messages.value.push(userMessage)
  await forceScrollToBottom()
  isLoading.value = true

  const aiMessageId = generateId()
  const aiMessage: Message = {
    id: aiMessageId, role: 'assistant', content: '',
    timestamp: new Date().toISOString(), session_id: currentSessionId.value!
  }
  messages.value.push(aiMessage)

  try {
    await ChatAPI.sendMessageStream(
      question,
      (token: string) => {
        const msg = messages.value.find(m => m.id === aiMessageId)
        if (msg) {
          msg.content += token
        }
      },
      async (fullResponse: string, sources: any[]) => {
        const msg = messages.value.find(m => m.id === aiMessageId)
        if (msg) {
          msg.content = fullResponse
        }
        await loadSessions()
      },
      (error: string) => {
        console.error('发送消息失败:', error)
        const msg = messages.value.find(m => m.id === aiMessageId)
        if (msg && !msg.content) {
          msg.content = '抱歉，我暂时无法回答您的问题。请稍后再试。'
        }
      },
      currentSessionId.value!,
      selectedKnowledgeBases.value
    )
  } catch (error) {
    console.error('发送消息失败:', error)
    const msg = messages.value.find(m => m.id === aiMessageId)
    if (msg && !msg.content) {
      msg.content = '抱歉，我暂时无法回答您的问题。请稍后再试。'
    }
    await forceScrollToBottom()
  } finally {
    isLoading.value = false
  }
}

watch(sessions, (newSessions) => {
  if (newSessions.length > 0 && !currentSessionId.value) switchSession(newSessions[0].id)
})

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

const loadSessionKnowledgeBases = async (sessionId: string) => {
  try {
    const session = sessions.value.find(s => s.id === sessionId)
    if (session?.knowledge_base_ids) {
      selectedKnowledgeBases.value = [...session.knowledge_base_ids]
    } else {
      selectedKnowledgeBases.value = []
    }
  } catch (error) {
    console.error('加载会话知识库配置失败:', error)
    selectedKnowledgeBases.value = []
  }
}

const saveSessionKnowledgeBases = async () => {
  if (!currentSessionId.value) return
  try {
    const session = sessions.value.find(s => s.id === currentSessionId.value)
    if (session) {
      session.knowledge_base_ids = [...selectedKnowledgeBases.value]
    }
  } catch (error) {
    console.error('保存会话知识库配置失败:', error)
  }
}

const toggleAllKnowledgeBases = async () => {
  const availableKbs = knowledgeBases.value.filter(kb => kb.status !== 'building')
  if (selectedKnowledgeBases.value.length < availableKbs.length) {
    selectedKnowledgeBases.value = availableKbs.map(kb => kb.id)
  } else {
    selectedKnowledgeBases.value = []
  }
  await saveSessionKnowledgeBases()
}

watch(selectedKnowledgeBases, async (newValue, oldValue) => {
  if (currentSessionId.value && JSON.stringify(newValue) !== JSON.stringify(oldValue)) {
    await saveSessionKnowledgeBases()
  }
}, {deep: true})


const formatFileSize = (bytes: number | undefined) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
}

const filteredKnowledgeBases = computed(() => {
  if (!knowledgeBaseSearch.value.trim()) return knowledgeBases.value
  const query = knowledgeBaseSearch.value.toLowerCase()
  return knowledgeBases.value.filter(kb =>
    kb.name.toLowerCase().includes(query) || kb.description?.toLowerCase().includes(query)
  )
})

const toggleKnowledgeBase = async (id: string) => {
  if (selectedKnowledgeBases.value.includes(id)) {
    selectedKnowledgeBases.value = selectedKnowledgeBases.value.filter(i => i !== id)
  } else {
    selectedKnowledgeBases.value.push(id)
  }
  await saveSessionKnowledgeBases()
}

onMounted(async () => {
  await loadKnowledgeBases()
  await loadSessions()
  if (sessions.value.length > 0) {
    await switchSession(sessions.value[0].id)
  } else {
    await createNewSession()
  }
  await forceScrollToBottom()
})

watch(messages, async (newMessages, oldMessages) => {
  if (newMessages.length > oldMessages.length) await scrollToBottom()
}, { deep: true })

watch(isLoading, async (newLoading, oldLoading) => {
  if (!oldLoading && newLoading) await scrollToBottom()
  else if (oldLoading && !newLoading) await scrollToBottom()
})
</script>

<style scoped>
.overflow-y-auto::-webkit-scrollbar { width: 4px; }
.overflow-y-auto::-webkit-scrollbar-track { background: transparent; }
.overflow-y-auto::-webkit-scrollbar-thumb { background: rgba(156, 163, 175, 0.3); border-radius: 2px; }

.animate-bounce { animation: bounce 1s infinite; }
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-3px); }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.min-h-0 { min-height: 0; }
</style>
