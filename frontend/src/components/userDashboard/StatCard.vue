<template>
  <v-card class="flex items-center justify-between p-3" :color="color + '-100'" variant="tonal">
    <span class="text-sm font-medium text-gray-700">{{ label }}</span>
    <span class="text-lg font-semibold text-gray-900">{{ value }}</span>
  </v-card>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  value: string
  color: string
}>()
</script>
