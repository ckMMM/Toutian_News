/**
 * this.$myModal({xxx})
 * 该 JavaScript 的作用：将 index.vue 干到 Vue.prototype 上，以方法的方式来调用 index.vue
 */
import MyModal from './index.vue'

export default {
  install(Vue, options) {
    // 这句话很重要
    const MyModalInstance = Vue.extend(MyModal)

    Vue.prototype.$myModal = message => {
      // 创建组件实例
      const instance = new MyModalInstance()

      // 设置组件相关数据
      // instance.show = true
      instance.message = message

      // 获取到 $mount 之后的模板内容
      const instanceEl = instance.$mount().$el

      console.log(instanceEl)

      // 插入到body中
      document.body.append(instanceEl)

      // 调用方法显示
      instance
        .showBox()
        .then()
        /*eslint handle-callback-err: ["error", "error"]*/
        .catch(err => {
          console.log('关闭了...')

          instance.$destroy()
        })
    }
  }
}
