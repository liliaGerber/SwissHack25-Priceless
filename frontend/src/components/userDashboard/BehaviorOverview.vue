<template>
  <v-card
      class="bg-background text-white px-6 py-5 rounded-xl w-full max-w-fit"
      flat
  >
    <!-- Title Row -->
    <div class="flex items-center gap-2 mb-2">
      <h2 class="text-lg font-semibold px-6 pt-0 pb-0">Behavior Overview</h2>
    </div>

    <!-- Info Row -->
    <div
        class="flex flex-col bg-secondary-background ml-4 p-5 rounded-xl gap-4 text-sm text-gray-300"
    >
      <!-- Stats Row -->
      <div class="flex flex-wrap md:flex-nowrap gap-x-8 gap-y-4">
        <div class="flex gap-2 items-center">
          <p class="text-gray-400 font-bold">App Logins (30d):</p>
          <p class="text-white font-medium">{{ props.customer.behavior.appLogins }}</p>
        </div>
        <div class="flex gap-2 items-center">
          <p class="text-gray-400 font-bold">Transactions (30d):</p>
          <p class="text-white font-medium">{{ props.customer.behavior.transactions }}</p>
        </div>
      </div>

      <!-- Engagement Row -->
      <div>
        <v-progress-linear
            :model-value="props.customer.behavior.engagement"
            color="cyan"
            height="10"
            rounded
        />
        <p class="text-sm text-gray-400 mt-2">
          Engagement: <span class="text-white font-medium">{{ props.customer.behavior.engagement }}%</span>
        </p>
      </div>
    </div>
  </v-card>
</template>

<script lang="ts" setup>
import {Customer} from "@/types/Customer.ts";

const props = defineProps<{
  customer: Customer
}>()

</script>
