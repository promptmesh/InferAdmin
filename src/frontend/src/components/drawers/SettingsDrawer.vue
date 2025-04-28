<script setup lang="ts">
import {
  Drawer,
  DrawerContent,
  DrawerHeader,
  DrawerTitle,
  DrawerDescription,
  DrawerFooter,
  DrawerClose
} from '@/components/ui/drawer'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { ref } from 'vue'

defineProps<{ open: boolean; onClose: () => void }>()

// Dummy data for API keys
const apiKeys = ref([
  { id: 'key_1', key: 'sk-abc...xyz', created: '2024-01-01', lastUsed: '2024-04-27' },
  { id: 'key_2', key: 'sk-123...789', created: '2024-02-15', lastUsed: '2024-04-28' }
])
const serverName = ref('My InferAdmin Server')

function generateNewKey() {
  // Placeholder for API call
  console.log('Generating new API key...')
  apiKeys.value.push({ id: `key_${apiKeys.value.length + 1}`, key: `sk-new...${Math.random().toString(36).substring(2, 6)}`, created: new Date().toISOString().split('T')[0], lastUsed: 'Never' })
}

function resetPassword() {
  // Placeholder for API call
  console.log('Initiating password reset...')
}

function saveServerName() {
  // Placeholder for API call to save the name
  console.log('Saving server name:', serverName.value)
  // You might want to add visual feedback here (e.g., toast notification)
}
</script>

<template>
  <Drawer :open="open" @update:open="(isOpen) => !isOpen && onClose()">
    <DrawerContent>
      <div class="mx-auto w-full max-w-md p-4">
        <DrawerHeader>
          <DrawerTitle>Settings</DrawerTitle>
          <DrawerDescription>Manage your account, server, and API access.</DrawerDescription>
        </DrawerHeader>

        <div class="space-y-6 py-4">
          <!-- Server Name Section -->
          <div class="space-y-2">
            <Label for="server-name">Server Name</Label>
            <div class="flex items-center gap-2">
              <Input id="server-name" v-model="serverName" placeholder="Enter server name" />
              <Button variant="outline" size="sm" @click="saveServerName">Save</Button>
            </div>
          </div>

          <!-- Reset Password Section -->
          <div class="space-y-2">
            <h4 class="font-medium">Account Security</h4>
            <Button variant="outline" @click="resetPassword">Reset Password</Button>
            <p class="text-sm text-muted-foreground">Initiate a password reset process via email.</p>
          </div>

          <!-- API Keys Section -->
          <div class="space-y-2">
            <h4 class="font-medium">API Keys</h4>
            <ul class="space-y-2 rounded-md border p-3">
              <li v-if="apiKeys.length === 0" class="text-sm text-muted-foreground">No API keys found.</li>
              <li v-for="apiKey in apiKeys" :key="apiKey.id" class="flex items-center justify-between text-sm">
                <span class="font-mono truncate" :title="apiKey.key">{{ apiKey.key }}</span>
                <span class="text-xs text-muted-foreground">Created: {{ apiKey.created }}</span>
                <!-- Add delete button here if needed -->
              </li>
            </ul>
            <Button @click="generateNewKey">Generate New API Key</Button>
          </div>
        </div>

        <DrawerFooter>
          <DrawerClose as-child>
            <Button variant="outline" @click="onClose">Close</Button>
          </DrawerClose>
        </DrawerFooter>
      </div>
    </DrawerContent>
  </Drawer>
</template>
