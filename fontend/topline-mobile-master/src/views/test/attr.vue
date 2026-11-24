<template>
  <div>
    <foo-com
      placeholder="请输入内容"
      type="password"
      @focus="handleFocus"
      @blur="handleBlur"/>
  </div>
</template>

<script>
import FooCom from './foo'
export default {
  components: {
    FooCom
  },
  methods: {
    handleFocus (e) {
      console.log('focus', e)
    },
    handleBlur () {
      console.log('blur')
    }
  }
}
</script>
