<template>
  <button @click="onClick()" :style="{ background: backgroundColor }">
    {{ text }}
  </button>
</template>

<script>
export default {
  name: 'EditUserButton',
  props: {
    text: String,
    backgroundColor: String,
  },
  methods: {
    onClick() {
      this.$emit('btn-click')
    },
  },
}
</script>