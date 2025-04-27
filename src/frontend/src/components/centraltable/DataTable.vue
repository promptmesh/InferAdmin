<template>
  <div class="w-full overflow-x-auto">
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead v-for="col in columns" :key="col.id || col.accessorKey">
            {{ col.header }}
          </TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <TableRow v-for="row in table.getRowModel().rows" :key="row.id">
          <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id">
            <slot :name="cell.column.id" :cell="cell">
              {{ cell.getValue() }}
            </slot>
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { createTable, useVueTable, getCoreRowModel } from '@tanstack/vue-table'
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell } from '../ui/table'

const props = defineProps<{
  columns: any[],
  data: any[],
}>()

const table = useVueTable({
  data: props.data,
  columns: props.columns,
  getCoreRowModel: getCoreRowModel(),
})

</script>

<style scoped>
/* Add any table-specific styling here */
</style>
