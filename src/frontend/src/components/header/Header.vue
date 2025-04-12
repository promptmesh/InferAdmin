<script setup lang="ts">
import LogoArea from "./LogoArea.vue";
import CommandSection from "./CommandSection.vue";
</script>

<template>
  <header class="w-full px-6 py-4 flex items-center border-b">
    <LogoArea />
    <div class="flex-1 flex justify-between items-center">
      <div class="w-full max-w-4xl mx-auto">
        <CommandSection />
      </div>
    </div>
  </header>
</template>
