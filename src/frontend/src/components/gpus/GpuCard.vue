<template>
  <div
    class="min-w-[240px] max-w-xs rounded-lg p-4 flex flex-col gap-2 relative transition-all"
    :class="[
      gpuState === 'selected' ? 'border-2 border-blue-500 ring-2 ring-blue-100 hover:shadow-lg cursor-pointer' : '',
      gpuState === 'unavailable' ? 'bg-gray-100 border border-gray-400 shadow-inner opacity-70' : '',
      gpuState === 'active' || gpuState === 'inactive' ? 'border border-gray-300 bg-white' : '',
      gpuState === 'unselected' ? 'border border-gray-300 bg-white hover:shadow-md cursor-pointer' : ''
    ]"
  >

    <div class="font-bold text-base text-gray-800 mb-1 truncate">{{ gpu.name }}</div>
    <div class="flex items-center justify-between">
      <span class="font-semibold text-sm">UUID:</span>
      <span class="text-xs text-gray-600">{{ gpu.uuid }}</span>
    </div>
    <div class="flex items-center justify-between">
      <span class="font-semibold text-sm">Assignment:</span>
      <span :class="[
        'text-xs',
        gpuState === 'unavailable' ? 'font-bold text-gray-800' : 'text-gray-600'
      ]">{{ gpu.assignment || 'N/A' }}</span>
    </div>
    <div class="flex flex-col gap-1 mt-2">
      <div class="flex items-center justify-between text-xs">
        <span>VRAM</span>
        <span>{{ gpu.vramUsage ?? 0 }}% / {{ gpu.vram ?? '?' }}GB</span>
      </div>
      <div class="w-full bg-gray-200 rounded h-2">
        <div class="bg-blue-500 h-2 rounded" :style="{ width: (gpu.vramUsage || 0) + '%' }"></div>
      </div>
      <div class="flex items-center justify-between text-xs">
        <span>Util</span>
        <span>{{ gpu.utilization ?? 0 }}%</span>
      </div>
      <div class="w-full bg-gray-200 rounded h-2">
        <div class="bg-green-500 h-2 rounded" :style="{ width: (gpu.utilization || 0) + '%' }"></div>
      </div>
      <div class="flex items-center justify-between text-xs">
        <span>Power</span>
        <span>{{ gpu.powerUsage ?? 0 }}% / {{ gpu.power ?? '?' }}W</span>
      </div>
      <div class="w-full bg-gray-200 rounded h-2">
        <div class="bg-yellow-500 h-2 rounded" :style="{ width: (gpu.powerUsage || 0) + '%' }"></div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { defineProps, computed } from 'vue'

const props = defineProps<{ gpu: Record<string, any>; state?: 'active' | 'inactive' | 'selected' | 'unselected' | 'unavailable' }>()

const gpuState = computed(() => {
  if (props.state) return props.state
  if (props.gpu.active === true) return 'active'
  if (props.gpu.active === false) return 'inactive'
  return 'unselected'
})


</script>

<style scoped>
/* Add any additional custom styles if needed */
</style>
