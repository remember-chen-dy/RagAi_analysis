<script setup lang="ts">
import Layout from './components/Layout.vue'
import { useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()
const hideLayout = computed(() => route.meta?.hideLayout)
</script>

<template>
  <div v-if="hideLayout" class="h-screen overflow-hidden">
    <router-view />
  </div>
  <Layout v-else />
</template>

<style>
/* 全局样式 - 防止滚动条 */
html, body {
  height: 100%;
  overflow: hidden;
}

#app {
  height: 100vh;
  overflow: hidden;
}
</style>
