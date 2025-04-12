<template>
  <div class="gpus-container">
    <h1>GPUs</h1>
    <div class="gpu-grid">
      <GpuView v-for="(gpu, index) in gpus" :key="index" :gpu="gpu" />
    </div>
  </div>
</template>

<script>
import GpuView from "./gpuView.vue";

export default {
  name: "GpuContainer",
  components: {
    GpuView,
  },
  data() {
    return {
      gpus: [
        {
          name: "Nvidia RTX 3090",
          vram: 24,
          vramUsage: 80, // Active
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
          vramUsage: 70, // Active
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
          vramUsage: 0, // Inactive
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
          vramUsage: 0, // Inactive
          utilization: 0,
          power: 350,
          powerUsage: 0,
          uuid: "8165",
          assignment: "None",
          active: false,
        },
      ],
    };
  },
};
</script>

<style scoped>
.gpus-container {
  padding: 20px;
  background-color: #f5f7f9;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.gpu-grid {
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  justify-content: center;
}
</style>
