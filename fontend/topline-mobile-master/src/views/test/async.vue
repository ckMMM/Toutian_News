<template>
  <div>
    <h1>动态组件 & 异步组件</h1>
    <button @click="component = 'login-com'">登录</button>
    <button @click="component = 'register-com'">注册</button>
    <keep-alive>
      <component :is="component" />
    </keep-alive>
  </div>
</template>

<script>
export default {
  components: {
    LoginCom: () => import('./login'),
    RegisterCom: () => import('./register')
  },
  data () {
    return {
      component: 'login-com'
    }
  }
}
</script>
