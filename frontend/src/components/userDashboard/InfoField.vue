<template>
  <div class="flex items-start gap-3">
    <v-icon :icon="icon" size="20" class="text-blue-500 mt-1" />
    <div>
      <p class="text-sm font-medium text-gray-600">{{ label }}</p>
      <p class="text-sm text-gray-800">{{ value }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  value: string
  icon: string
}>()
</script>
