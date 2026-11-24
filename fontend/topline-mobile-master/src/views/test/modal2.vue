<template>
  <div>
    <button @click="handleShowModal">Show Modal</button>
  </div>
</template>

<script>
export default {
  methods: {
    handleShowModal () {
      this.$myModal('Hello World')
    }
  }
}
</script>
