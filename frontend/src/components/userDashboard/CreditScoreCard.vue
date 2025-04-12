<template>
  <v-card
      flat
      class="bg-background text-white px-6 py-5 rounded-xl w-full max-w-fit"
  >
    <!-- Title Row -->
    <div class="flex items-center gap-2 mb-2">
<!--      <v-icon class="text-green-400" size="24">mdi-shield-check</v-icon>-->
      <h2 class="text-lg font-semibold px-6 pt-0 pb-0">Credit Score</h2>
    </div>

    <!-- Info Row -->
    <div class="flex bg-secondary-background ml-4 p-5 rounded-xl flex-wrap md:flex-nowrap items-center gap-x-6 text-sm text-gray-300">
      <div class="flex gap-1">
        <p class="text-gray-400 font-bold">Score:</p>
        <p class="font-medium text-white">{{ creditData.score }}</p>
      </div>
      <div class="flex gap-1">
        <p class="text-gray-400 font-bold">Rating:</p>
        <p class="capitalize">{{ creditData.rating }}</p>
      </div>
      <div class="flex gap-1">
        <p class="text-gray-400 font-bold">Last Checked:</p>
        <p>{{ creditData.last_checked }}</p>
      </div>
    </div>
  </v-card>
</template>

<script lang="ts" setup>
import {customer} from '@/data/customer.ts';

const creditData = customer.financial_data.credit_score
</script>
