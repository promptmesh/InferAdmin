<template>
  <div>
    <DataTabs :tabs="tabs" v-model="activeTab" @tab-change="onTabChange">
      <template #applications>
        <DataTable :columns="applicationsColumns" :data="applicationsData">
          <template #actions="{ cell }">
            <Button size="sm" variant="secondary" class="font-semibold" @click="openDetails(cell.row.original)">Details</Button>
          </template>
        </DataTable>
        <Drawer v-model:open="detailsDialog">
          <DrawerContent side="bottom" class="w-screen max-w-none p-8 bg-white text-gray-900">
            <div class="grid grid-cols-3 gap-6">
              <!-- Left: Core Details -->
              <div class="flex flex-col gap-4">
                <label v-for="field in coreFields" :key="field.key" class="flex flex-col text-xs">
                  <span class="mb-1 font-semibold">{{ field.label }}</span>
                  <input :value="selectedApplication[field.key]" readonly class="bg-gray-100 border px-2 py-1 rounded text-gray-900" />
                </label>
              </div>
              <!-- Middle: Logs -->
              <div class="flex flex-col">
                <div class="flex items-center justify-between mb-1">
                  <label class="font-semibold text-xs">Logs</label>
                  <Button size="sm" variant="default" class="font-semibold" @click="refreshLogs">Refresh Logs</Button>
                </div>
                <textarea :value="selectedApplication.logs" readonly class="bg-black text-green-400 font-mono text-xs p-3 rounded h-64 resize-none max-h-96" />
              </div>
              <!-- Right: GPUs -->
              <div class="flex flex-col h-full">
                <div v-if="gpuList.length" class="flex flex-row gap-4 overflow-x-auto pb-2">
                  <GpuCard v-for="gpuUuid in gpuList" :key="gpuUuid" :gpu="assignedGpuDetails[gpuUuid] || { uuid: gpuUuid, name: gpuUuid, assignment: selectedApplication.name, vram: 24, vramUsage: 60, utilization: 50, power: 350, powerUsage: 80, active: true }" />
                </div>
                <div v-else class="text-gray-400 text-xs">No GPUs assigned</div>
              </div>
            </div>
            <div class="flex gap-2 justify-end mt-8">
              <Button variant="secondary" class="font-semibold" @click="closeDetails">Close</Button>
              <Button variant="secondary" class="font-semibold">Edit</Button>
              <Button variant="destructive" class="font-semibold">Delete</Button>
              <Button variant="secondary" class="font-semibold" @click="restartContainer">Restart Container</Button>
            </div>
          </DrawerContent>
        </Drawer>
      </template>
      <template #models>
        <DataTable :columns="modelsColumns" :data="modelsData">
          <template #actions="{ cell }">
            <TableActions
              :row="cell.row.original"
              @update="updateModel"
              @delete="deleteModel"
            />
          </template>
        </DataTable>
      </template>
      <template #images>
        <DataTable :columns="imagesColumns" :data="imagesData">
          <template #actions="{ cell }">
            <TableActions
              :row="cell.row.original"
              @update="updateImage"
              @delete="deleteImage"
            />
          </template>
        </DataTable>
      </template>
    </DataTabs>
  </div>
</template>

<script setup lang="ts">
import DataTabs from './DataTabs.vue'
import DataTable from './DataTable.vue'
import TableActions from './TableActions.vue'
import { Button } from '../ui/button'
import { Drawer, DrawerContent } from '../ui/drawer'
import { ref, reactive, computed } from 'vue'
import GpuCard from '../gpus/GpuCard.vue' // DRY, minimal GPU card

// Placeholder: refresh logs for the selected application
function refreshLogs() {
  // TODO: Implement log fetching
  window.alert('Logs refreshed!')
}

// Placeholder: restart the container for the selected application
function restartContainer() {
  // TODO: Implement restart logic
  window.alert('Container restarted!')
}

// Placeholder: update/delete handlers for models and images
function updateModel(row: any) {
  window.alert('Update Model: ' + JSON.stringify(row))
}
function deleteModel(row: any) {
  window.alert('Delete Model: ' + JSON.stringify(row))
}
function updateImage(row: any) {
  window.alert('Update Image: ' + JSON.stringify(row))
}
function deleteImage(row: any) {
  window.alert('Delete Image: ' + JSON.stringify(row))
}

// Example: Map GPU UUIDs to details (replace with real data as needed)
const assignedGpuDetails: Record<string, any> = {
  'uuid-1': {
    uuid: 'uuid-1',
    name: 'Nvidia RTX 3090',
    assignment: 'Inference Service',
    vram: 24,
    vramUsage: 80,
    utilization: 60,
    power: 350,
    powerUsage: 90,
    active: true,
  },
  'uuid-2': {
    uuid: 'uuid-2',
    name: 'Nvidia RTX 4090',
    assignment: 'Inference Service',
    vram: 24,
    vramUsage: 65,
    utilization: 55,
    power: 350,
    powerUsage: 85,
    active: true,
  },
}

const tabs = [
  { label: 'Applications', value: 'applications' },
  { label: 'Models', value: 'models' },
  { label: 'Images', value: 'images' }
]

const applicationsColumns = [
  { id: 'id', accessorKey: 'id', header: 'ID' },
  { id: 'name', accessorKey: 'name', header: 'Name' },
  { id: 'state', accessorKey: 'state', header: 'State' },
  { id: 'type', accessorKey: 'type', header: 'Type' },
  { id: 'deployed', accessorKey: 'deployed', header: 'Deployed' },
  { id: 'host_port', accessorKey: 'host_port', header: 'Host Port' },
  { id: 'gpu_uuids', accessorKey: 'gpu_uuids', header: 'GPU UUIDs' },
  { id: 'actions', header: 'Actions' },
]

const modelsColumns = [
  { id: 'repo_id', accessorKey: 'repo_id', header: 'Repo ID' },
  { id: 'path', accessorKey: 'path', header: 'Path' },
  { id: 'size_gb', accessorKey: 'size_gb', header: 'Size (GB)' },
  { id: 'last_updated', accessorKey: 'last_updated', header: 'Last Updated' },
  { id: 'actions', header: 'Actions' },
]

const imagesColumns = [
  { id: 'repo', accessorKey: 'repo', header: 'Repo' },
  { id: 'id', accessorKey: 'id', header: 'ID' },
  { id: 'path', accessorKey: 'path', header: 'Path' },
  { id: 'tag', accessorKey: 'tag', header: 'Tag' },
  { id: 'created', accessorKey: 'created', header: 'Created' },
  { id: 'size', accessorKey: 'size', header: 'Size (GB)' },
  { id: 'actions', header: 'Actions' },
]

const applicationsData = [
  {
    id: 'app1',
    name: 'Inference Service',
    state: 'running',
    type: 'gpu',
    deployed: '2025-04-27T19:00:00Z',
    host_port: 8080,
    gpu_uuids: ['uuid-1', 'uuid-2'].join(', '),
    logs: 'View Logs'
  },
  {
    id: 'app2',
    name: 'Training Service',
    state: 'stopped',
    type: 'cpu',
    deployed: '2025-04-25T10:00:00Z',
    host_port: 9000,
    gpu_uuids: '',
    logs: 'View Logs'
  }
]

const modelsData = [
  {
    repo_id: 'huggingface/bert',
    path: '/models/bert',
    size_gb: 2.1,
    last_updated: '2025-04-20T12:00:00Z'
  },
  {
    repo_id: 'openai/gpt',
    path: '/models/gpt',
    size_gb: 5.6,
    last_updated: '2025-04-18T16:00:00Z'
  }
]

const imagesData = [
  {
    repo: 'myorg/infer',
    id: 'sha256:abcd1234',
    path: '/images/infer',
    tag: 'latest',
    created: '2025-04-10T09:00:00Z',
    size: 1200.5
  },
  {
    repo: 'myorg/train',
    id: 'sha256:efgh5678',
    path: '/images/train',
    tag: 'v1.0',
    created: '2025-03-22T14:00:00Z',
    size: 950.2
  }
]

const activeTab = ref('applications')
const detailsDialog = ref(false)
// Use an explicit index signature to allow string-based property access
const selectedApplication = reactive<Record<string, any>>({})

const coreFields = [
  { key: 'name', label: 'Name' },
  { key: 'id', label: 'ID' },
  { key: 'state', label: 'State' },
  { key: 'type', label: 'Type' },
  { key: 'host_port', label: 'Host Port' },
  { key: 'deployed', label: 'Deployed' },
]

function openDetails(app: Record<string, any>) {
  Object.assign(selectedApplication, app)
  detailsDialog.value = true
} // Explicit type for app
function closeDetails() {
  detailsDialog.value = false
  Object.keys(selectedApplication).forEach((k: string) => delete selectedApplication[k])
}
function onTabChange(tabValue: string) {
  // Handle tab switch logic here
  activeTab.value = tabValue
}

const gpuList = computed(() => {
  if (!selectedApplication.gpu_uuids) return []
  return selectedApplication.gpu_uuids.split(',').map(x => x.trim()).filter(Boolean)
})
</script>

<style scoped>
/* Add any additional styling here if needed */
</style>
