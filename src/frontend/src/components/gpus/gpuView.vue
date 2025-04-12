<template>
  <div class="gpu-container">
    <div class="gpu-card" :class="{ inactive: !gpu.active }">
      <h2>{{ gpu.name }}</h2>
      <div class="gpu-stats">
        <div class="stat">
          <p>{{ gpu.vram }} GB</p>
          <div class="progress-bar">
            <div
              class="progress"
              :style="{ height: gpu.vramUsage + '%' }"
            ></div>
          </div>
          <p>VRAM</p>
        </div>
        <div class="stat">
          <p>{{ gpu.utilization }}%</p>
          <div class="progress-bar">
            <div
              class="progress"
              :style="{ height: gpu.utilization + '%' }"
            ></div>
          </div>
          <p>UTIL</p>
        </div>
        <div class="stat">
          <p>{{ gpu.power }}W</p>
          <div class="progress-bar">
            <div
              class="progress"
              :style="{ height: gpu.powerUsage + '%' }"
            ></div>
          </div>
          <p>PWR</p>
        </div>
      </div>
      <div class="gpu-info">
        <p><strong>UUID</strong></p>
        <p>{{ gpu.uuid }}</p>
        <p><strong>Assignment</strong></p>
        <p>{{ gpu.assignment }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "GpuView",
  props: {
    gpu: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.gpu-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.gpu-card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 250px;
  text-align: center;
  font-family: Arial, sans-serif;
}

.inactive {
  color: #9aa6b8;
}

.inactive .progress {
  background: #e0e0e0;
}

h2 {
  font-size: 18px;
  margin-bottom: 10px;
  color: inherit;
}

.gpu-stats {
  display: flex;
  justify-content: space-between;
  margin: 20px 0;
}

.stat {
  text-align: center;
}

.stat p {
  margin: 5px 0;
  font-size: 14px;
  color: #555;
}

.progress-bar {
  width: 10px;
  height: 100px;
  background: #e6e6e6;
  border-radius: 5px;
  margin: 0 auto;
  position: relative;
  overflow: hidden;
}

.progress {
  width: 100%;
  background: #1a1a1a;
  position: absolute;
  bottom: 0;
  border-radius: 5px;
}

.gpu-info {
  margin-top: 10px;
  font-size: 14px;
  color: #555;
}

.gpu-info p {
  margin: 5px 0;
}

.gpu-info strong {
  color: #333;
}
</style>
