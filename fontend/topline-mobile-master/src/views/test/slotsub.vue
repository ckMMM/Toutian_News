<template>
  <div>
    <slot name="hello" />
    <hr />
    <slot v-bind:msg="msg" />
    <hr />
    <slot name="world" v-bind:message="msg" v-bind:age="age" />
  </div>
</template>

<script>
export default {
  data () {
    return {
      msg: '你好呀',
      age: 30
    }
  }
}
</script>
