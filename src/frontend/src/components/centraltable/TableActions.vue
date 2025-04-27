<script setup lang="ts">
import { Button } from '../ui/button'
import { defineProps, defineEmits } from 'vue'

// Define props for row data and action handlers
const props = defineProps<{
  row: any
  updateLabel?: string
  deleteLabel?: string
  onUpdate?: (row: any) => void
  onDelete?: (row: any) => void
  updateDisabled?: boolean
  deleteDisabled?: boolean
}>()

const emits = defineEmits(['update', 'delete'])

function handleUpdate() {
  emits('update', props.row)
  if (props.onUpdate) props.onUpdate(props.row)
}
function handleDelete() {
  emits('delete', props.row)
  if (props.onDelete) props.onDelete(props.row)
}
</script>

<template>
  <div class="flex gap-2">
    <Button
      size="sm"
      variant="secondary"
      class="font-semibold"
      :disabled="updateDisabled"
      @click="handleUpdate"
    >
      {{ updateLabel || 'Update' }}
    </Button>
    <Button
      size="sm"
      variant="destructive"
      class="font-semibold"
      :disabled="deleteDisabled"
      @click="handleDelete"
    >
      {{ deleteLabel || 'Delete' }}
    </Button>
  </div>
</template>
