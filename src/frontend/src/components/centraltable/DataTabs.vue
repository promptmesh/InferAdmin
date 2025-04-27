<template>
  <Tabs v-model="currentTab" class="w-full">
    <TabsList class="w-full flex bg-white rounded-t-lg mb-2 px-2 py-1">
      <TabsTrigger
        v-for="tab in tabs"
        :key="tab.value"
        :value="tab.value"
        :class="[
          'px-6 py-2 mx-1 rounded-lg transition-colors duration-150 font-semibold',
          currentTab === tab.value
            ? 'text-blue-600 border-b-2 border-blue-600 bg-white shadow-sm'
            : 'text-gray-500 hover:text-blue-600 bg-gray-50 hover:bg-white'
        ]"
      >
        {{ tab.label }}
      </TabsTrigger>
    </TabsList>
    <TabsContent
      v-for="tab in tabs"
      :key="tab.value"
      :value="tab.value"
      class="pt-4"
    >
      <slot :name="tab.value" />
    </TabsContent>
  </Tabs>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../ui/tabs'

const props = defineProps<{
  tabs: Array<{ label: string; value: string }>,
  modelValue?: string
}>()
const emit = defineEmits(['update:modelValue', 'tab-change'])

const currentTab = ref(props.modelValue ?? props.tabs[0]?.value)

watch(() => props.modelValue, (val) => {
  if (val !== undefined) currentTab.value = val
})
watch(currentTab, (val) => {
  emit('update:modelValue', val)
  emit('tab-change', val)
})
</script>

<style scoped>
/* Additional styling can go here if needed */
</style>
