<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  used: number,      // Used space in GB
  total: number      // Total space in GB
  label?: string     // Optional label (e.g., "Volume A")
}>()

const percent = computed(() => {
  if (!props.total) return 0
  return Math.min(100, Math.round((props.used / props.total) * 100))
})

const remaining = computed(() => Math.max(0, props.total - props.used))
</script>

<template>
  <div class="flex flex-col gap-1">
    <div class="flex justify-between items-center mb-1">
      <span v-if="props.label" class="text-xs font-medium text-gray-700">{{ props.label }}</span>
      <span class="text-xs text-gray-500">{{ used }}GB / {{ total }}GB</span>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-3 relative">
      <div :style="{ width: percent + '%' }"
           class="h-3 rounded-full bg-blue-500 transition-all duration-300"></div>
      <span class="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-gray-600">
        {{ remaining }}GB left
      </span>
    </div>
  </div>
</template>

<style scoped>
</style>
