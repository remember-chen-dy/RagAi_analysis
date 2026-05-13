<template>
  <div class="markdown-renderer prose prose-sm max-w-none" v-html="renderedMarkdown"></div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'

// 导入highlight.js的CSS样式
import 'highlight.js/styles/github.css'

interface Props {
  content: string
}

const props = defineProps<Props>()

// 配置marked
onMounted(() => {
  // 配置marked选项
  marked.setOptions({
    breaks: true, // 支持换行符
    gfm: true, // 启用GitHub风格的markdown
  })
})

// 渲染markdown内容
const renderedMarkdown = computed(() => {
  try {
    let html = marked(props.content || '') as string
    
    // 后处理：为代码块添加语法高亮
    html = html.replace(/<pre><code class="language-(\w+)">([\s\S]*?)<\/code><\/pre>/g, (match, lang, code) => {
      const decodedCode = decodeHtml(code)
      let highlightedCode = decodedCode
      
      if (lang && hljs.getLanguage(lang)) {
        try {
          highlightedCode = hljs.highlight(decodedCode, { language: lang }).value
        } catch (err) {
          console.warn('Highlight.js error:', err)
        }
      } else {
        try {
          highlightedCode = hljs.highlightAuto(decodedCode).value
        } catch (err) {
          console.warn('Highlight.js auto error:', err)
        }
      }
      
      return `<pre class="bg-gray-100 rounded-lg p-4 my-4 overflow-x-auto border"><code class="language-${lang} text-sm font-mono">${highlightedCode}</code></pre>`
    })
    
    // 为无语言的代码块添加高亮
    html = html.replace(/<pre><code>([\s\S]*?)<\/code><\/pre>/g, (match, code) => {
      const decodedCode = decodeHtml(code)
      let highlightedCode = decodedCode
      
      try {
        highlightedCode = hljs.highlightAuto(decodedCode).value
      } catch (err) {
        console.warn('Highlight.js auto error:', err)
      }
      
      return `<pre class="bg-gray-100 rounded-lg p-4 my-4 overflow-x-auto border"><code class="text-sm font-mono">${highlightedCode}</code></pre>`
    })
    
    // 后处理：添加Tailwind CSS类
    html = html.replace(/<h1>/g, '<h1 class="text-2xl font-bold mt-6 mb-4 text-gray-800">')
    html = html.replace(/<h2>/g, '<h2 class="text-xl font-semibold mt-6 mb-4 text-gray-800">')
    html = html.replace(/<h3>/g, '<h3 class="text-lg font-semibold mt-6 mb-3 text-gray-800">')
    html = html.replace(/<h4>/g, '<h4 class="text-base font-semibold mt-4 mb-2 text-gray-800">')
    html = html.replace(/<h5>/g, '<h5 class="text-sm font-semibold mt-4 mb-2 text-gray-800">')
    html = html.replace(/<h6>/g, '<h6 class="text-xs font-semibold mt-4 mb-2 text-gray-800">')
    
    html = html.replace(/<p>/g, '<p class="mb-3 leading-relaxed text-gray-700">')
    html = html.replace(/<code>/g, '<code class="bg-gray-100 px-2 py-1 rounded text-sm font-mono text-gray-800">')
    html = html.replace(/<a /g, '<a class="text-blue-600 hover:text-blue-800 underline" target="_blank" rel="noopener" ')
    html = html.replace(/<ul>/g, '<ul class="my-3 ml-6 list-disc">')
    html = html.replace(/<ol>/g, '<ol class="my-3 ml-6 list-decimal">')
    html = html.replace(/<li>/g, '<li class="mb-1">')
    html = html.replace(/<blockquote>/g, '<blockquote class="border-l-4 border-blue-300 pl-4 py-2 my-3 bg-blue-50 text-gray-700 italic">')
    html = html.replace(/<table>/g, '<table class="w-full border-collapse border border-gray-300 my-4">')
    html = html.replace(/<th>/g, '<th class="border border-gray-300 px-3 py-2 bg-gray-50 font-semibold text-left">')
    html = html.replace(/<td>/g, '<td class="border border-gray-300 px-3 py-2">')
    html = html.replace(/<tr>/g, '<tr class="border-b border-gray-200">')
    html = html.replace(/<hr>/g, '<hr class="my-6 border-gray-300">')
    html = html.replace(/<strong>/g, '<strong class="font-semibold">')
    html = html.replace(/<em>/g, '<em class="italic">')
    html = html.replace(/<del>/g, '<del class="line-through">')
    
    return html
  } catch (error) {
    console.error('Markdown rendering error:', error)
    return `<p class="text-red-500">Markdown渲染错误: ${error}</p>`
  }
})

// 解码HTML实体
const decodeHtml = (html: string): string => {
  const txt = document.createElement('textarea')
  txt.innerHTML = html
  return txt.value
}
</script>

<style scoped>
.markdown-renderer {
  color: #111827;
  line-height: 1.6;
}

/* 确保代码块的样式正确 */
.markdown-renderer :deep(pre) {
  background-color: #f8f9fa !important;
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 1rem 0;
  overflow-x: auto;
  border: 1px solid #e5e7eb;
}

.markdown-renderer :deep(pre code) {
  background: none !important;
  padding: 0 !important;
  border-radius: 0 !important;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 0.875rem;
  line-height: 1.5;
}

.markdown-renderer :deep(code) {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
}

/* 表格样式 */
.markdown-renderer :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  background: white;
}

.markdown-renderer :deep(th) {
  background-color: #f3f4f6;
  font-weight: 600;
  text-align: left;
}

.markdown-renderer :deep(td), 
.markdown-renderer :deep(th) {
  border: 1px solid #d1d5db;
  padding: 0.75rem;
}

/* 列表样式 */
.markdown-renderer :deep(ul) {
  list-style-type: disc;
  margin-left: 1.5rem;
}

.markdown-renderer :deep(ol) {
  list-style-type: decimal;
  margin-left: 1.5rem;
}

.markdown-renderer :deep(li) {
  margin-bottom: 0.25rem;
}

/* 引用样式 */
.markdown-renderer :deep(blockquote) {
  border-left: 4px solid #93c5fd;
  padding-left: 1rem;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  margin: 0.75rem 0;
  background-color: #eff6ff;
  color: #374151;
  font-style: italic;
}

/* 链接样式 */
.markdown-renderer :deep(a) {
  color: #2563eb;
  text-decoration: underline;
  transition: color 0.2s ease;
}

.markdown-renderer :deep(a:hover) {
  color: #1d4ed8;
}

/* 分隔线样式 */
.markdown-renderer :deep(hr) {
  margin: 1.5rem 0;
  border: none;
  border-top: 1px solid #d1d5db;
}

/* 响应式图片 */
.markdown-renderer :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 0.375rem;
  margin: 1rem 0;
}
</style> 