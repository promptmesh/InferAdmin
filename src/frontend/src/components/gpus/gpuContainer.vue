<template>
  <div class="gpus-container">
    <h2 class="text-2xl font-bold text-center mb-6 text-gray-800 tracking-tight">Compute Resources</h2>
    <div :class="[
      'w-full pb-2',
      gpus.length <= 3
        ? 'flex justify-center gap-4 flex-wrap'
        : 'flex flex-row gap-4 overflow-x-auto'
    ]">
      <GpuCard v-for="(gpu, index) in gpus" :key="index" :gpu="gpu"
        :state="
          index === 0 ? 'active' :
          index === 1 ? 'selected' :
          index === 2 ? 'unavailable' :
          'unselected'"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import GpuCard from './GpuCard.vue'

// Keep the same GPU mock data as before
const gpus = [
  {
    name: "Nvidia RTX 3090",
    vram: 24,
    vramUsage: 80,
    utilization: 60,
    power: 350,
    powerUsage: 90,
    uuid: "8165",
    assignment: "vLLM Instance 1",
    active: true,
  },
  {
    name: "Nvidia RTX 3090",
    vram: 24,
    vramUsage: 70,
    utilization: 50,
    power: 350,
    powerUsage: 80,
    uuid: "8165",
    assignment: "vLLM Instance 1",
    active: true,
  },
  {
    name: "Nvidia RTX 3090",
    vram: 24,
    vramUsage: 0,
    utilization: 0,
    power: 350,
    powerUsage: 0,
    uuid: "8165",
    assignment: "None",
    active: false,
  },
  {
    name: "Nvidia RTX 3090",
    vram: 24,
    vramUsage: 0,
    utilization: 0,
    power: 350,
    powerUsage: 0,
    uuid: "8165",
    assignment: "None",
    active: false,
  },
]
</script>
