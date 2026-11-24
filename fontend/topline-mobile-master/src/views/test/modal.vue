<template>
  <div>
    <button @click="isShow = true">Show Modal</button>
    <ModalSub1 v-model="isShow">
      <template #body>
        <button>
          <form>
            <label for>用户名:</label>
            <input type="text" />
            <br />
            <label for>密码:</label>
            <input type="password" />
            <br />
            <button>登录</button>
          </form>
        </button>
      </template>
    </ModalSub1>
  </div>
</template>

<script>
import ModalSub1 from './modalsub1'
export default {
  components: {
    ModalSub1
  },
  data () {
    return {
      isShow: false
    }
  }
}
</script>
