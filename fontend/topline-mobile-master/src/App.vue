<template>
  <div id="app">
    <!-- <van-button type="default">默认按钮</van-button>
    <van-button type="primary">主要按钮</van-button>
    <van-button type="info">信息按钮</van-button>
    <van-button type="warning">警告按钮</van-button>
    <van-button type="danger">危险按钮</van-button> -->
    <!-- <div class="test"></div> -->
    <!-- 缓存路由 -->
    <keep-alive>
      <router-view />
    </keep-alive>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style lang="less" scoped>
.test {
  width: 375px;
  height: 200px;
  background: red;
}
</style>
