<template>
  <!-- 从外部提供的数据，默认作用于根元素上面 -->
  <div>
    <!-- <input v-bind="$attrs" type="text"> -->
    <!-- <input @focus="$emit('focus',$event)" v-bind="$attrs"> -->
    <!-- 继承原生事件 -->
    <input v-on="$listeners" v-bind="$attrs">
  </div>
</template>

<script>
export default {
  inheritAttrs: false, // 禁用根元素的属性继承
  created () {
    console.log(this.$attrs)
  }
}
</script>
