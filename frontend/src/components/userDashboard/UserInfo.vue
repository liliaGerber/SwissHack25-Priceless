<template>
  <v-card class="bg-secondary-background text-white rounded-xl px-3 py-6 max-w-fit">
    <div class="flex items-center gap-4 mb-2 px-3">
      <v-avatar size="90">
        <img :alt="customer.name" :src="customer.avatar"/>
      </v-avatar>
      <div>
        <h2 class="text-xl font-bold leading-tight">{{ customer.name }}</h2>
        <p class="text-gray-400 text-sm">{{ customer.id }}</p>
      </div>
    </div>

    <v-list class="bg-transparent text-white px-0 overflow-hidden">
      <v-list-item class="list-item" density="compact">
        <v-icon class="mr-3" size="20">mdi-email</v-icon>
        <span>{{ customer.email }}</span>
      </v-list-item>

      <v-list-item class="list-item" density="compact">
        <v-icon class="mr-3" size="20">mdi-phone</v-icon>
        <span>{{ customer.phone }}</span>
      </v-list-item>

      <v-list-item class="list-item" density="compact">
        <v-icon class="mr-3" size="20">mdi-map-marker</v-icon>
        <span>{{ customer.address }}</span>
      </v-list-item>

      <v-list-item class="list-item" density="compact">
        <v-icon class="mr-3" size="20">mdi-card-account-details</v-icon>
        <span>{{ customer.accountNumber }}</span>
      </v-list-item>

      <v-list-item class="list-item" density="compact">
        <v-icon class="mr-3" size="20">mdi-check-circle</v-icon>
        <span>{{ customer.status }}</span>
      </v-list-item>

      <v-list-item class="list-item" density="compact">
        <v-icon class="mr-3" size="20">mdi-calendar</v-icon>
        <span>{{ customer.birthdate }}</span>
      </v-list-item>

      <v-list-item class="list-item" density="compact">
        <v-icon class="mr-3" size="20">mdi-clock-time-four</v-icon>
        <span>Last Login &nbsp; {{ customer.lastLogin }}</span>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script lang="ts" setup>
import {customer} from "@/data/customer.ts";
</script>
<style scoped>

.list-item {
  padding: 0;
  margin-bottom: -10px;
}
</style>