import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Vant from 'vant'
import 'vant/lib/index.css'
import '@/styles/index.less'
import 'amfe-flexible/index.js'
import zhCN from 'vee-validate/dist/locale/zh_CN'
import VeeValidate, { Validator } from 'vee-validate'

// 测试自定义插件
import MyModelPlugin from './views/test/mymodal'

Vue.use(VeeValidate, {
  // 配置改变的时候去触发校验，默认是 input
  // https://baianat.github.io/vee-validate/guide/events.html#changing-default-events
  // events:'change'
  events: ''
})

Validator.localize('zh_CN', zhCN)

Vue.config.productionTip = false

Vue.use(Vant)

Vue.prototype.$sleep = time => {
  return new Promise((resolve, reject) => {
    window.setTimeout(() => {
      resolve()
    }, time)
  })
}
Vue.use(MyModelPlugin)

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
