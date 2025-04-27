<script setup lang="ts">
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator
} from "@/components/ui/command";

import { Gauge, FileBox, Container, Box, Settings } from "lucide-vue-next";
import NewApplicationDrawer from '../drawers/NewApplicationDrawer.vue' // Adjust path if needed
import NewImageDrawer from '../drawers/NewImageDrawer.vue'


// Dummy data for demonstration (replace with real data from store or props)
const dummyModels = [
  {
    repo_id: 'meta/llama-2-70b',
    path: 'models/llama-2-70b',
    size_gb: 40,
    last_updated: '2025-04-01T12:00:00Z',
  },
  {
    repo_id: 'openai/gpt-4',
    path: 'models/gpt-4',
    size_gb: 50,
    last_updated: '2025-03-15T08:00:00Z',
  }
]
const dummyGpuList = ['gpu-1', 'gpu-2', 'gpu-3']
const dummyGpuDetails = {
  'gpu-1': { uuid: 'gpu-1', name: 'NVIDIA A100', vram: 40 },
  'gpu-2': { uuid: 'gpu-2', name: 'NVIDIA H100', vram: 80 },
  'gpu-3': { uuid: 'gpu-3', name: 'NVIDIA RTX 4090', vram: 24 }
}

import { ref, onMounted, onUnmounted } from "vue";

const isOpen = ref(false);
const showNewAppDrawer = ref(false)
const showNewImageDrawer = ref(false)
const newAppType = ref<'inference' | 'application' | null>(null)


const inputRef = ref<HTMLInputElement | null>(null);
const commandContainer = ref(null);

const handleFocus = () => {
  isOpen.value = true;
};

// Close on escape key press
const handleKeydown = (event: KeyboardEvent) => {
  if (event.key === "Escape" && isOpen.value) {
    isOpen.value = false;
    inputRef.value?.blur();
  }

  // Open on Cmd+K or Ctrl+K
  if ((event.metaKey || event.ctrlKey) && event.key === "k") {
    event.preventDefault();
    isOpen.value = true;
    inputRef.value?.focus();
  }
};

const handleClickOutside = (event: MouseEvent) => {
  if (commandContainer.value && !commandContainer.value.contains(event.target as Node)) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener("keydown", handleKeydown);
  document.addEventListener("mousedown", handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener("keydown", handleKeydown);
  document.removeEventListener("mousedown", handleClickOutside);
});

function handleCommand(action: string) {
  if (action === 'launch-inference') {
    showNewAppDrawer.value = true
    newAppType.value = 'inference'
  } else if (action === 'launch-application') {
    showNewAppDrawer.value = true
    newAppType.value = 'application'
  } else if (action === 'pull-docker-image') {
    showNewImageDrawer.value = true
  }
  isOpen.value = false;
  inputRef.value?.blur();
}

const selectItem = () => {
  isOpen.value = false;
  inputRef.value?.blur();
};
</script>

<template>
  <div class="relative" ref="commandContainer">
    <Command>
      <CommandInput
        ref="inputRef"
        placeholder="Type a command or search..."
        @focus="handleFocus"
        @mousedown="isOpen = true"
      />

      <div
        v-if="isOpen"
        class="absolute top-full left-0 right-0 mt-2 bg-background rounded-md border shadow-lg z-50"
      >
        <CommandList>
          <CommandEmpty>No results found.</CommandEmpty>
          <CommandGroup heading="Suggestions">
            <CommandItem value="launch-inference" @click="() => handleCommand('launch-inference')">
              <Gauge />
              <span>Launch Inference Engine</span>
            </CommandItem>
            <CommandItem value="launch-application" @click="() => handleCommand('launch-application')">
              <Container />
              <span>Launch Application</span>
            </CommandItem>

            <CommandItem value="pull-hf-model" @click="selectItem">
              <FileBox />
              <span>Pull HuggingFace Model</span>
            </CommandItem>
            <CommandItem value="pull-docker-image" @click="() => handleCommand('pull-docker-image')">
              <Box />
              <span>Pull Docker Images</span>
            </CommandItem>
          </CommandGroup>
          <CommandSeparator />
          <CommandGroup heading="Settings">
            <CommandItem value="config" @click="selectItem">
              <Settings />
              <span>Configuration</span>
            </CommandItem>
          </CommandGroup>
        </CommandList>
      </div>
    </Command>
  </div>
    <NewApplicationDrawer
      v-if="showNewAppDrawer"
      :open="showNewAppDrawer"
      :onClose="() => { showNewAppDrawer = false }"
      :modelOptions="dummyModels"
      :gpuList="dummyGpuList"
      :gpuDetails="dummyGpuDetails"
      @submit="() => { showNewAppDrawer = false; /* handle submit here */ }"
      
    />
  <NewImageDrawer
    :open="showNewImageDrawer"
    :onClose="() => showNewImageDrawer = false"
    :volumeUsed="24"
    :volumeTotal="100"
    volumeLabel="Volume A"
    @submit="(payload) => { showNewImageDrawer = false; /* handle payload.repoStr here */ }"
  />
</template>


<style scoped>
.absolute {
  position: absolute;
}
.top-full {
  top: 100%;
}
.left-0 {
  left: 0;
}
.right-0 {
  right: 0;
}
.mt-2 {
  margin-top: 0.5rem;
}
.z-50 {
  z-index: 50;
}
</style>
