<template>
  <div>
    <div class="text-center">
      <div class="w-10 h-10 mx-auto mb-2 bg-gradient-to-r from-purple-500 to-indigo-600 rounded-xl flex items-center justify-center">
        <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      </div>
      <h2 class="text-sm font-medium text-gray-900 mb-1">使用统计分析</h2>
      <p class="text-xs text-gray-500 mb-3">数据统计功能开发中</p>
      
      <!-- 功能预览卡片 -->
      <div class="grid grid-cols-1 gap-2 mb-3">
        <div class="bg-gray-50 rounded-lg p-2 border border-gray-100 flex items-center gap-2">
          <div class="w-6 h-6 bg-blue-100 rounded flex items-center justify-center flex-shrink-0">
            <svg class="w-3 h-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
            </svg>
          </div>
          <div class="text-left">
            <p class="text-xs font-medium text-gray-900">文件上传统计</p>
            <p class="text-xs text-gray-400">上传量、成功率</p>
          </div>
        </div>
        
        <div class="bg-gray-50 rounded-lg p-2 border border-gray-100 flex items-center gap-2">
          <div class="w-6 h-6 bg-green-100 rounded flex items-center justify-center flex-shrink-0">
            <svg class="w-3 h-3 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
            </svg>
          </div>
          <div class="text-left">
            <p class="text-xs font-medium text-gray-900">对话数据分析</p>
            <p class="text-xs text-gray-400">问答量、响应时间</p>
          </div>
        </div>
        
        <div class="bg-gray-50 rounded-lg p-2 border border-gray-100 flex items-center gap-2">
          <div class="w-6 h-6 bg-purple-100 rounded flex items-center justify-center flex-shrink-0">
            <svg class="w-3 h-3 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
            </svg>
          </div>
          <div class="text-left">
            <p class="text-xs font-medium text-gray-900">知识库使用情况</p>
            <p class="text-xs text-gray-400">检索频率、热门内容</p>
          </div>
        </div>
      </div>
      
      <div class="flex items-center justify-center gap-1.5 text-xs text-amber-600 bg-amber-50 px-2 py-1.5 rounded-lg border border-amber-200">
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <span>功能开发中</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script> 