import Vue from 'vue'
import Vuex from 'vuex'

import * as auth from '@/utils/auth'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    // 初始化的时候，从本地存储获取数据，防止刷新丢失 token
    user: auth.getUser()
  },
  mutations: {
    /**
     * 登录成功，调用 mutations 更新容器中的 user 的状态
     */
    setUser (state, user) {
      state.user = user

      // 将数据存储到本地
      auth.saveUser(user)
    }
  },
  actions: {}
})
