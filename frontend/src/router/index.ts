import {createRouter, createWebHistory} from 'vue-router'
import FileManager from '@/views/FileManager.vue'
import ChatBot from '@/views/ChatBot.vue'
import KnowledgeBase from '@/views/KnowledgeBase.vue'
import Evaluation from '@/views/Evaluation.vue'
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      title: '登录',
      hideLayout: true // 标记此页面不显示导航栏
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      title: '注册',
      hideLayout: true // 标记此页面不显示导航栏
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

  // 简单的认证检查 (实际项目中应该检查真实的认证状态)
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true'
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router 