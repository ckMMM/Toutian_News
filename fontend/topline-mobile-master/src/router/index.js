import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/login', component: () => import('@/views/login') },
    {
      path: '/',
      component: () => import('@/views/tabbar-layout'),
      children: [{ path: 'home', component: () => import('@/views/home') }]
    },
    { path: '/test', component: () => import('@/views/test') },
    { path: '/test/attr', component: () => import('@/views/test/attr') },
    { path: '/test/slot', component: () => import('@/views/test/slot') },
    { path: '/test/async', component: () => import('@/views/test/async') },
    { path: '/test/modal', component: () => import('@/views/test/modal') },
    { path: '/test/modal2', component: () => import('@/views/test/modal2') },
    { path: '/chat', component: () => import('@/views/chat') }
  ]
})
