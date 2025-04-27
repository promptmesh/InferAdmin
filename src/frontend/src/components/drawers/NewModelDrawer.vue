<script setup lang="ts">
import { ref } from 'vue'
import { Drawer, DrawerContent } from '../ui/drawer'
import { Button } from '../ui/button'
import VolumeProgressBar from '../infra/VolumeProgressBar.vue'

const props = defineProps<{
  open: boolean
  onClose: () => void
  volumeUsed: number // Used space in GB
  volumeTotal: number // Total space in GB
  volumeLabel?: string
}>()

const emits = defineEmits(['submit'])

const hfId = ref('')

function submit() {
  emits('submit', { hfId: hfId.value })
  props.onClose()
}
</script>

<template>
  <Drawer v-model:open="props.open">
    <DrawerContent side="bottom" class="w-full max-w-lg mx-auto p-8 bg-white text-gray-900">
      <div class="flex flex-col gap-6">
        <h2 class="text-lg font-semibold mb-2">Add New Model</h2>
        <VolumeProgressBar :used="props.volumeUsed" :total="props.volumeTotal" :label="props.volumeLabel" />
        <label class="flex flex-col text-xs">
          <span class="mb-1 font-semibold">HuggingFace Model ID</span>
          <input v-model="hfId" placeholder="e.g. meta-llama/Llama-2-7b-hf" class="bg-gray-100 border px-2 py-1 rounded text-gray-900" />
        </label>
        <div class="flex gap-2 justify-end mt-4">
          <Button variant="secondary" @click="props.onClose">Cancel</Button>
          <Button variant="default" @click="submit" :disabled="!hfId.trim()">Add Model</Button>
        </div>
      </div>
    </DrawerContent>
  </Drawer>
</template>

<style scoped>
</style>
