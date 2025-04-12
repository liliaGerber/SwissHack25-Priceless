<template>
  <v-card
      flat
      class="bg-background text-white px-6 py-5 rounded-xl w-full max-w-fit"
  >
    <!-- Title Row -->
    <div class="flex items-center gap-2 mb-2">
      <h2 class="text-lg font-semibold px-6 pt-0 pb-0">Customer Summary</h2>
    </div>

    <!-- Content Row -->
    <div
        class="bg-secondary-background ml-4 p-5 rounded-xl text-sm text-gray-300 leading-relaxed
             max-w-[600px] min-h-[120px] max-h-[400px] overflow-scroll whitespace-pre-line"
    >
      <p class="text-wrap">
        {{ customer.summary }}
      </p>
    </div>
  </v-card>
</template>

<script lang="ts" setup>
import { customer } from '@/data/customer.ts'
</script>
