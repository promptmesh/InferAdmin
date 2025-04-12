<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue'
import { Button } from '@/components/ui/button'
</script>

<template>
  <div>
    <a href="https://inferadmin.com" target="_blank">
      <img src="/inferadmin_logo.svg" class="logo" alt="InferAdmin logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
    <div class="mt-">

    </div>
  </div>
  <HelloWorld msg="InferAdmin + Vue" />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
