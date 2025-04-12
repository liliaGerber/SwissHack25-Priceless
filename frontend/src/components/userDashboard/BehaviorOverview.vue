<template>
  <v-card class="p-4">
    <h3 class="font-semibold text-xl mb-4">Behavior Overview</h3>
    <v-row>
      <v-col cols="6">
        <StatCard label="App Logins (30d)" value="23" color="indigo" />
      </v-col>
      <v-col cols="6">
        <StatCard label="Transactions (30d)" value="58" color="purple" />
      </v-col>
    </v-row>
    <v-row class="mt-4">
      <v-col cols="12">
        <v-progress-linear :model-value="engagement" color="cyan" height="10" rounded />
        <p class="text-sm text-gray-600 mt-2">Engagement: {{ engagement }}%</p>
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup lang="ts">
import StatCard from './StatCard.vue'

const engagement = 67
</script>
