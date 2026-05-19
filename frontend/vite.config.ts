import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  css: {
    postcss: {
      plugins: [
        tailwindcss
      ]
    }
  },
  server: {
    host: '0.0.0.0',  // 关键：监听所有网络接口
    port: 5173,
    cors: true,
    allowedHosts: 'all',
    proxy: {
      '/api': {
        target: 'http://192.168.1.1:8000',
      }
    }
  }
})
