<script setup lang="ts">
import { Settings } from "lucide-vue-next"

defineProps<{ onClick?: () => void }>()
</script>

<template>
    <button
    class="flex items-center justify-center w-10 h-10 rounded-full bg-white shadow-sm z-10 hover:bg-blue-50 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
    type="button"
    @click="$props.onClick && $props.onClick()"
    aria-label="Open settings"
  >
    <!-- Try rendering both icons for debugging -->
    <Settings class="w-5 h-5 text-blue-600" />
    <!-- <Gauge class="w-5 h-5 text-red-600" /> -->
    <!-- <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg> -->
  </button>
</template>

<style scoped>
</style>
