<template>
  <slot-sub>
    <template #hello>
      <div>这个是name为hello的插槽</div>
    </template>
    <template slot-scope="scoped">
      <div>默认插槽 --- {{scoped}}---{{scoped.msg}}</div>
    </template>
    <template v-slot:world="worldScoped">
      <div>这个是name为world的插槽---{{worldScoped}}</div>
    </template>
  </slot-sub>
</template>

<script>
import SlotSub from './slotsub'
export default {
  components: {
    SlotSub
  }
}
</script>
