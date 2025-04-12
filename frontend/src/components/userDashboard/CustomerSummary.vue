<template>
  <v-card
      class="bg-background text-white mt-0 rounded-xl w-full"
  >
    <!-- Title Row -->
    <div class="flex items-center mb-2">
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
import {Customer} from "@/types/Customer.ts";

const props = defineProps<{
  customer: Customer
}>()
</script>
