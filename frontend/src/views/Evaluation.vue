<template>
  <div class="flex flex-col h-full">
    <header class="bg-white border-b border-gray-200 flex-shrink-0">
      <div class="max-w-full mx-auto px-8 py-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-light text-gray-900 mb-2">RAG 评估</h1>
            <p class="text-gray-500">使用 RAGAS 框架评估知识库的检索增强生成效果</p>
          </div>
        </div>
      </div>
    </header>

    <main class="flex-1 min-h-0 overflow-y-auto px-8 py-6">
      <div class="max-w-5xl mx-auto space-y-6">
        <!-- 配置区域 -->
        <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
          <h2 class="text-lg font-medium text-gray-900 mb-5">评估配置</h2>

          <div class="grid grid-cols-2 gap-6">
            <!-- 知识库选择 -->
            <div class="col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-2">选择知识库</label>
              <a-select
                v-model:value="selectedKbIds"
                mode="multiple"
                placeholder="请选择要评估的知识库"
                class="w-full"
                :loading="loadingKbs"
                option-label-prop="label"
              >
                <a-select-option
                  v-for="kb in knowledgeBases"
                  :key="kb.id"
                  :value="kb.id"
                  :label="kb.name"
                >
                  <div class="flex items-center justify-between">
                    <span>{{ kb.name }}</span>
                    <span class="text-xs text-gray-400">{{ kb.status === 'active' ? '运行中' : kb.status }}</span>
                  </div>
                </a-select-option>
              </a-select>
            </div>

            <!-- 索引类型 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">索引类型</label>
              <a-radio-group v-model:value="indexType">
                <a-radio-button value="vector">向量索引</a-radio-button>
                <a-radio-button value="hybrid">混合索引</a-radio-button>
              </a-radio-group>
            </div>

            <!-- 测试集大小 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                测试集大小
                <span class="text-xs text-gray-400 ml-1">自动生成的问题数量</span>
              </label>
              <a-input-number v-model:value="testsetSize" :min="1" :max="20" class="w-full" />
            </div>

            <!-- 检索数量 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                检索返回数量 (Top K)
              </label>
              <a-input-number v-model:value="similarityTopK" :min="1" :max="20" class="w-full" />
            </div>

            <!-- 评估指标 -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">评估指标</label>
              <a-checkbox-group v-model:value="selectedMetrics" class="space-y-2">
                <div class="flex items-center space-x-4">
                  <a-checkbox value="faithfulness">
                    <span class="text-sm">忠实度</span>
                    <span class="text-xs text-gray-400 ml-1">Faithfulness</span>
                  </a-checkbox>
                  <a-checkbox value="answer_relevancy">
                    <span class="text-sm">答案相关性</span>
                    <span class="text-xs text-gray-400 ml-1">Answer Relevancy</span>
                  </a-checkbox>
                </div>
                <div class="flex items-center space-x-4">
                  <a-checkbox value="context_precision">
                    <span class="text-sm">上下文精确度</span>
                    <span class="text-xs text-gray-400 ml-1">Context Precision</span>
                  </a-checkbox>
                  <a-checkbox value="context_recall">
                    <span class="text-sm">上下文召回率</span>
                    <span class="text-xs text-gray-400 ml-1">Context Recall</span>
                  </a-checkbox>
                </div>
              </a-checkbox-group>
            </div>
          </div>

          <!-- 评估流程说明 -->
          <div class="mt-5 p-4 bg-gray-50 rounded-lg border border-gray-100">
            <h3 class="text-sm font-medium text-gray-700 mb-2">评估流程</h3>
            <div class="flex items-center space-x-2 text-xs text-gray-500">
              <span class="inline-flex items-center px-2 py-1 bg-white rounded border border-gray-200">1. 从向量库获取文档</span>
              <svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
              <span class="inline-flex items-center px-2 py-1 bg-white rounded border border-gray-200">2. 自动生成测试集</span>
              <svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
              <span class="inline-flex items-center px-2 py-1 bg-white rounded border border-gray-200">3. RAG 查询获取答案</span>
              <svg class="w-4 h-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
              <span class="inline-flex items-center px-2 py-1 bg-white rounded border border-gray-200">4. RAGAS 评分计算</span>
            </div>
          </div>

          <!-- 开始评估按钮 -->
          <div class="mt-5 flex items-center space-x-4">
            <button
              @click="startEvaluation"
              :disabled="isEvaluating || selectedKbIds.length === 0"
              class="bg-gray-900 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              <svg v-if="isEvaluating" class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
              <span>{{ isEvaluating ? '评估中...' : '开始评估' }}</span>
            </button>
            <span v-if="isEvaluating" class="text-sm text-gray-500">评估过程可能需要几分钟，请耐心等待</span>
          </div>
        </div>

        <!-- 评估结果 -->
        <div v-if="evalResult" class="space-y-6">
          <!-- 总体得分 -->
          <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
            <h2 class="text-lg font-medium text-gray-900 mb-5">总体得分</h2>
            <div class="grid grid-cols-4 gap-4">
              <div
                v-for="(score, key) in evalResult.aggregate_scores"
                :key="key"
                class="text-center p-4 rounded-lg border border-gray-100"
                :class="getScoreBgClass(score)"
              >
                <div class="text-3xl font-light mb-1" :class="getScoreTextClass(score)">
                  {{ (score * 100).toFixed(1) }}%
                </div>
                <div class="text-xs text-gray-500">{{ metricLabelMap[key] || key }}</div>
              </div>
              <div
                v-if="Object.keys(evalResult.aggregate_scores).length === 0"
                class="col-span-4 text-center py-8 text-gray-400"
              >
                暂无评分数据
              </div>
            </div>
          </div>

          <!-- 样本详情 -->
          <div class="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
            <div class="flex items-center justify-between mb-5">
              <h2 class="text-lg font-medium text-gray-900">样本详情</h2>
              <span class="text-sm text-gray-500">共 {{ evalResult.sample_count }} 个样本</span>
            </div>

            <div class="space-y-4">
              <div
                v-for="(sample, index) in evalResult.samples"
                :key="index"
                class="border border-gray-100 rounded-lg overflow-hidden"
              >
                <div
                  class="flex items-center justify-between px-4 py-3 bg-gray-50 cursor-pointer hover:bg-gray-100 transition-colors"
                  @click="toggleSample(index)"
                >
                  <div class="flex items-center space-x-3">
                    <span class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-gray-900 text-white text-xs font-medium">
                      {{ index + 1 }}
                    </span>
                    <span class="text-sm text-gray-900 truncate max-w-md">{{ sample.question }}</span>
                  </div>
                  <div class="flex items-center space-x-2">
                    <span v-if="sample.error" class="text-xs text-red-500">查询失败</span>
                    <svg
                      class="w-4 h-4 text-gray-400 transition-transform"
                      :class="{ 'rotate-180': expandedSamples.has(index) }"
                      fill="none" stroke="currentColor" viewBox="0 0 24 24"
                    >
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
                    </svg>
                  </div>
                </div>

                <div v-if="expandedSamples.has(index)" class="p-4 space-y-3 border-t border-gray-100">
                  <div v-if="sample.error" class="p-3 bg-red-50 rounded-lg border border-red-100">
                    <p class="text-sm text-red-600">{{ sample.error }}</p>
                  </div>
                  <div>
                    <label class="block text-xs font-medium text-gray-500 mb-1">问题</label>
                    <p class="text-sm text-gray-900">{{ sample.question }}</p>
                  </div>
                  <div>
                    <label class="block text-xs font-medium text-gray-500 mb-1">参考答案</label>
                    <p class="text-sm text-gray-700">{{ sample.ground_truth || '无' }}</p>
                  </div>
                  <div>
                    <label class="block text-xs font-medium text-gray-500 mb-1">RAG 回答</label>
                    <p class="text-sm text-gray-900 whitespace-pre-wrap">{{ sample.answer || '无回答' }}</p>
                  </div>
                  <div>
                    <label class="block text-xs font-medium text-gray-500 mb-1">检索上下文</label>
                    <div v-if="sample.contexts && sample.contexts.length > 0" class="space-y-2">
                      <div
                        v-for="(ctx, ctxIdx) in sample.contexts"
                        :key="ctxIdx"
                        class="p-2 bg-gray-50 rounded text-xs text-gray-600 line-clamp-3"
                      >
                        {{ ctx }}
                      </div>
                    </div>
                    <p v-else class="text-sm text-gray-400">无检索上下文</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 错误提示 -->
        <div v-if="evalError" class="bg-white rounded-xl border border-red-200 shadow-sm p-6">
          <div class="flex items-start space-x-3">
            <svg class="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
            <div>
              <h3 class="text-sm font-medium text-red-800">评估失败</h3>
              <p class="text-sm text-red-600 mt-1">{{ evalError }}</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { getKnowledgeBases, type KnowledgeBase } from '@/api/knowledge'
import { evaluateRag, type EvaluationResultData } from '@/api/evaluation'

const knowledgeBases = ref<KnowledgeBase[]>([])
const loadingKbs = ref(false)
const selectedKbIds = ref<string[]>([])
const indexType = ref('vector')
const testsetSize = ref(5)
const similarityTopK = ref(5)
const selectedMetrics = ref<string[]>(['faithfulness', 'answer_relevancy', 'context_precision', 'context_recall'])

const isEvaluating = ref(false)
const evalResult = ref<EvaluationResultData | null>(null)
const evalError = ref<string | null>(null)
const expandedSamples = ref<Set<number>>(new Set())

const metricLabelMap: Record<string, string> = {
  faithfulness: '忠实度',
  answer_relevancy: '答案相关性',
  context_precision: '上下文精确度',
  context_recall: '上下文召回率',
}

const getScoreBgClass = (score: number) => {
  if (score >= 0.8) return 'bg-green-50'
  if (score >= 0.6) return 'bg-yellow-50'
  return 'bg-red-50'
}

const getScoreTextClass = (score: number) => {
  if (score >= 0.8) return 'text-green-600'
  if (score >= 0.6) return 'text-yellow-600'
  return 'text-red-600'
}

const toggleSample = (index: number) => {
  if (expandedSamples.value.has(index)) {
    expandedSamples.value.delete(index)
  } else {
    expandedSamples.value.add(index)
  }
}

const loadKnowledgeBases = async () => {
  loadingKbs.value = true
  try {
    const response = await getKnowledgeBases()
    if (response.success) {
      knowledgeBases.value = response.data
    }
  } catch (error) {
    console.error('获取知识库列表失败:', error)
  } finally {
    loadingKbs.value = false
  }
}

const startEvaluation = async () => {
  if (selectedKbIds.value.length === 0) {
    message.warning('请选择至少一个知识库')
    return
  }

  isEvaluating.value = true
  evalResult.value = null
  evalError.value = null
  expandedSamples.value.clear()

  try {
    const response = await evaluateRag({
      knowledge_base_ids: selectedKbIds.value,
      index_type: indexType.value,
      testset_size: testsetSize.value,
      similarity_top_k: similarityTopK.value,
      metrics: selectedMetrics.value,
    })

    if (response.success && response.data) {
      evalResult.value = response.data
      message.success(response.message || '评估完成')
    } else {
      evalError.value = response.message || '评估失败'
    }
  } catch (error) {
    evalError.value = (error as Error).message || '评估请求失败'
    console.error('评估失败:', error)
  } finally {
    isEvaluating.value = false
  }
}

onMounted(() => {
  loadKnowledgeBases()
})
</script>

<style scoped>
.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
