<script setup lang="ts">
import {
  Command,
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
  CommandShortcut,
} from '@/components/ui/command'

import {
  Gauge,
  FileBox,
  Container,
  Box,
  Settings
} from 'lucide-vue-next'
</script>

<template>
    <Command>
      <CommandInput placeholder="Type a command or search..." />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>
        <CommandGroup heading="Suggestions">
          <CommandItem value="launch-inference">
            <Gauge />
            <span>Launch Inference Engine </span>
          </CommandItem>
          <CommandItem value="launch-application">
            <Container />
            <span>Launch Application </span>
          </CommandItem>
          <CommandItem value="pull-hf-model">
            <FileBox />
            <span>Pull HuggingFace Model </span>
          </CommandItem>
          <CommandItem value="pull-docker-image">
            <Box />
            <span>Pull Docker Images </span>
          </CommandItem>
        </CommandGroup>
        <CommandSeparator />
        <CommandGroup heading="Settings">
          <CommandItem value="config">
            <Settings />
            <span>Configuration </span>
          </CommandItem>
        </CommandGroup>
      </CommandList>
    </Command>
  </template>