<template>
  <div>
    <van-nav-bar title="登录" />
    <van-cell-group>
      <van-field v-model="user.mobile" v-validate="'required'" name="mobile" :error-message="errors.first('mobile')" clearable label="手机号" placeholder="请输入手机号" />
      <van-field v-model="user.code" v-validate="'required'" name="code" :error-message="errors.first('code')"  type="number" label="验证码" placeholder="请输入验证码" required />
    </van-cell-group>
    <div class="login-btn">
      <van-button :loading="loading" @click="handleLogin" type="info">登录</van-button>
    </div>
  </div>
</template>

<script>
import { login } from '@/api/user'
export default {
  data () {
    return {
      user: {
        mobile: '18801185985',
        code: '246810'
      },
      loading: false
    }
  },
  created () {
    this.configCustomMessages()
  },
  methods: {
    // 自定义消息校验规则
    configCustomMessages () {
      const dict = {
        custom: {
          mobile: {
            required: '手机号不能为空'
          },
          code: {
            required: () => '验证码不能为空'
          }
        }
      }

      // or use the instance method
      this.$validator.localize('zh_CN', dict)
    },
    async handleLogin () {
      this.loading = true

      const valid = await this.$validator.validate()

      // 校验不通过
      if (!valid) {
        this.loading = false
        return
      }

      try {
        // 校验通过，发送登录请求
        const data = await login(this.user)

        // 通过提交 mutation 更新 Vuex 容器中的状态
        this.$store.commit('setUser', data)

        // 跳转到home
        this.$router.push('/home')
      } catch (error) {
        this.$toast.fail('登录失败')
      }

      this.loading = false
    }
  }
}
</script>

<style lang="less" scoped>
.login-btn {
  padding: 10px;

  button {
    width: 100%;
  }
}
</style>
