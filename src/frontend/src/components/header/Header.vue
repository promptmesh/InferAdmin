<script setup lang="ts">
import LogoArea from "./LogoArea.vue";
import CommandSection from "./CommandSection.vue";
import SettingsButton from "./SettingsButton.vue";
import SettingsDrawer from "../drawers/SettingsDrawer.vue"; // Adjust path if needed

import { ref } from 'vue';

const showSettingsDrawer = ref(false);
</script>

<template>
  <header class="w-full px-6 py-4 flex items-center border-b gap-4">
    <LogoArea />
    <div class="flex-1 flex items-center">
      <CommandSection />
    </div>
    <SettingsButton :onClick="() => showSettingsDrawer = true" />
  </header>

  <SettingsDrawer
    :open="showSettingsDrawer"
    :onClose="() => showSettingsDrawer = false"
  />
</template>
