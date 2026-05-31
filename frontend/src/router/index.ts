import {createRouter, createWebHistory} from 'vue-router'
import FileManager from '@/views/FileManager.vue'
import ChatBot from '@/views/ChatBot.vue'
import KnowledgeBase from '@/views/KnowledgeBase.vue'
import Evaluation from '@/views/Evaluation.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import { getAuthToken } from '@/api/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      title: '登录',
      hideLayout: true
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      title: '注册',
      hideLayout: true
    }
  },
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/files',
    name: 'FileManager',
    component: FileManager,
    meta: {
      title: '文件管理',
      requiresAuth: true
    }
  },
  {
    path: '/chat',
    name: 'ChatBot',
    component: ChatBot,
    meta: {
      title: 'AI对话',
      requiresAuth: true
    }
  },
  {
    path: '/knowledge',
    name: 'KnowledgeBase',
    component: KnowledgeBase,
    meta: {
      title: '知识库管理',
      requiresAuth: true
    }
  },

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, _, next) => {
  if (to.meta.title) {
    document.title = `${to.meta.title} - AI平台`
  }

  const token = getAuthToken()

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && token) {
    next('/files')
  } else {
    next()
  }
})

export default router 