<script setup lang="ts">
import { ref } from 'vue'
import { Drawer, DrawerContent } from '../ui/drawer'
import { Button } from '../ui/button'
import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from '../ui/select'
import GpuCard from '../gpus/GpuCard.vue'

// Props
const props = defineProps<{
  open: boolean
  onClose: () => void
  modelOptions: Array<{ repo_id: string; path: string; size_gb: number; last_updated?: string | null }>
  gpuList: string[]
  gpuDetails: Record<string, any>
}>()

// Emits
const emits = defineEmits(['submit'])

// Form State
const applicationType = ref('vLLM')
const name = ref('')
const port = ref('')
const selectedModel = ref('')
const selectedGpus = ref<string[]>([])
const args = ref<Array<{ key: string; value: string }>>([])
const flags = ref<string[]>([])

function addArg() {
  args.value.push({ key: '', value: '' })
}
function removeArg(idx: number) {
  args.value.splice(idx, 1)
}
function addFlag() {
  flags.value.push('')
}
function removeFlag(idx: number) {
  flags.value.splice(idx, 1)
}
function toggleGpu(uuid: string) {
  if (selectedGpus.value.includes(uuid)) {
    selectedGpus.value = selectedGpus.value.filter(g => g !== uuid)
  } else {
    selectedGpus.value.push(uuid)
  }
}
function submit() {
  emits('submit', {
    applicationType: applicationType.value,
    name: name.value,
    port: port.value,
    model: selectedModel.value,
    gpus: selectedGpus.value,
    args: args.value,
    flags: flags.value
  })
  props.onClose()
}
</script>

<template>
  <Drawer v-model:open="props.open">
    <DrawerContent side="bottom" class="w-screen max-w-none p-8 bg-white text-gray-900">
      <div class="grid grid-cols-3 gap-6">
        <!-- Left: App Info -->
        <div class="flex flex-col gap-4">
          <label class="flex flex-col text-xs">
            <span class="mb-1 font-semibold">Application Type</span>
            <Select v-model="applicationType">
              <SelectTrigger>
                <SelectValue placeholder="Select type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="vLLM">vLLM</SelectItem>
                <SelectItem value="OpenWebUI">OpenWebUI</SelectItem>
              </SelectContent>
            </Select>
          </label>
          <label class="flex flex-col text-xs">
            <span class="mb-1 font-semibold">Name</span>
            <input v-model="name" class="bg-gray-100 border px-2 py-1 rounded text-gray-900" />
          </label>
          <label class="flex flex-col text-xs">
            <span class="mb-1 font-semibold">Port</span>
            <input v-model="port" class="bg-gray-100 border px-2 py-1 rounded text-gray-900" />
          </label>
          <label v-if="applicationType !== 'OpenWebUI'" class="flex flex-col text-xs">
            <span class="mb-1 font-semibold">Model</span>
            <Select v-model="selectedModel">
              <SelectTrigger>
                <SelectValue placeholder="Select model" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem v-for="model in props.modelOptions" :key="model.repo_id" :value="model.repo_id">
                  {{ model.repo_id }}
                  <span class="text-xs text-gray-400 ml-2">({{ model.path }})</span>
                  <span class="text-xs text-gray-400 ml-2">- {{ model.size_gb }}GB</span>
                </SelectItem>
              </SelectContent>
            </Select>
          </label>
        </div>
        <!-- Middle: Arguments -->
        <Tabs default-value="arguments" class="w-full">
  <TabsList class="mb-4">
    <TabsTrigger value="arguments">Arguments</TabsTrigger>
    <TabsTrigger value="flags">Flags</TabsTrigger>
  </TabsList>
  <TabsContent value="arguments">
    <div class="space-y-3">
      <div v-for="(arg, idx) in args" :key="idx" class="flex items-center gap-2 border p-2 rounded-md bg-gray-50">
        <input v-model="arg.key" placeholder="Key" class="bg-white border px-2 py-1 rounded text-gray-900 w-1/3" />
        <input v-model="arg.value" placeholder="Value" class="bg-white border px-2 py-1 rounded text-gray-900 w-1/2" />
        <Button size="icon" variant="ghost" @click="removeArg(idx)"><span class="sr-only">Remove</span><svg class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg></Button>
      </div>
      <Button variant="outline" class="mt-2" @click="addArg">Add Argument</Button>
    </div>
  </TabsContent>
  <TabsContent value="flags">
    <div class="space-y-3">
      <div v-for="(flag, idx) in flags" :key="idx" class="flex items-center gap-2 border p-2 rounded-md bg-gray-50">
        <input v-model="flags[idx]" placeholder="Flag (e.g., --no-cache)" class="bg-white border px-2 py-1 rounded text-gray-900 w-full" />
        <Button size="icon" variant="ghost" @click="removeFlag(idx)"><span class="sr-only">Remove</span><svg class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg></Button>
      </div>
      <Button variant="outline" class="mt-2" @click="addFlag">Add Flag</Button>
    </div>
  </TabsContent>
</Tabs>
        <!-- Right: GPU Selection -->
        <div class="flex flex-col gap-4">
          <label class="font-semibold text-xs mb-2">Select GPUs</label>
          <div class="flex flex-row gap-4 overflow-x-auto pb-2">
            <div v-for="gpuUuid in props.gpuList" :key="gpuUuid" @click="toggleGpu(gpuUuid)">
              <GpuCard :gpu="props.gpuDetails[gpuUuid] || { uuid: gpuUuid }" :selected="selectedGpus.includes(gpuUuid)" class="cursor-pointer border-2" :class="selectedGpus.includes(gpuUuid) ? 'border-blue-600' : 'border-gray-200'" />
            </div>
          </div>
        </div>
      </div>
      <div class="flex gap-2 justify-end mt-8">
        <Button variant="secondary" class="font-semibold" @click="props.onClose">Cancel</Button>
        <Button variant="default" class="font-semibold" @click="submit">Create Application</Button>
      </div>
    </DrawerContent>
  </Drawer>
</template>
