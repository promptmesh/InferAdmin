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
import { ref, onMounted, onUnmounted } from "vue";

const isOpen = ref(false);
import type { Ref } from 'vue'
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
            <CommandItem value="launch-inference" @click="selectItem">
              <Gauge />
              <span>Launch Inference Engine</span>
            </CommandItem>
            <CommandItem value="launch-application" @click="selectItem">
              <Container />
              <span>Launch Application</span>
            </CommandItem>
            <CommandItem value="pull-hf-model" @click="selectItem">
              <FileBox />
              <span>Pull HuggingFace Model</span>
            </CommandItem>
            <CommandItem value="pull-docker-image" @click="selectItem">
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
