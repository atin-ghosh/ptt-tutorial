<template>
  <div class="fullscreen">
    <Login />
  </div>
</template>

<script>
// @ is an alias to /src
import Login from '../components/Login.vue'

export default {
  name: 'Home',
  components: {
    Login
  }
}
</script>

<style>
.fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  overflow: auto;
  background: #333f6b; /* Just to visualize the extent */ 
}
</style>