<script setup lang="ts">
import command_section from './components/header/CommandSection.vue';
import LogoArea from './components/header/LogoArea.vue';
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
  <logo-area/>
  <command_section/>
  
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
