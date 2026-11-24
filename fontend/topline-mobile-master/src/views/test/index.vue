<template>
  <div>
    <!-- <input v-validate="'required|email'" name="email" type="text">
    <span>{{ errors.first('email') }}</span>-->
    <van-cell-group>
      <van-field v-validate="'required'" v-model="username" name="username" placeholder="请输入用户名" :error-message="errors.first('username')"/>
    </van-cell-group>
  </div>
</template>

<script>
export default {
  data () {
    return {
      username: ''
    }
  }
}
</script>

<style>
</style>
