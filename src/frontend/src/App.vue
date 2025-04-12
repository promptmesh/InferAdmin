<script setup lang="ts">
import Header from "./components/header/Header.vue";
import GpuContainer from "./components/gpus/gpuContainer.vue";
</script>

<template>
  <div class="app-container">
    <Header />
    <logo-area />
    <command_section />
    <main class="content-container">
      <div class="content">
        <GpuContainer />
      </div>
    </main>
  </div>
</template>

<style scoped>
.app-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.content-container {
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.content {
  width: 100%;
  padding: 0 1rem;
  height: 100%;
  flex: 1;
}
</style>
