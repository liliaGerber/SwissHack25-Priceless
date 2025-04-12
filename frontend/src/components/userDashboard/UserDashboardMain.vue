<template>
  <v-container fluid class="py-8 px-6 bg-gray-900 bg-background">
    <v-row dense>
      <!-- Left Column -->
      <v-col cols="12" md="4">
        <UserInfo />
        <DocumentUploader class="mt-6" />
      </v-col>

      <!-- Right Column -->
      <v-col cols="12" md="8">
        <FinancialStats />
        <BehaviorOverview class="mt-6" />

        <v-row class="mt-6" dense>
          <v-col cols="12" md="6">
            <v-card class="p-6 bg-white rounded-xl shadow-sm">
              <h2 class="text-xl font-semibold text-gray-800 mb-2">Customer Summary</h2>
              <p class="text-gray-600 text-sm">
                Layla has maintained a strong savings record with consistent engagement through our mobile app. No recent account issues detected.
              </p>
            </v-card>
          </v-col>

          <v-col cols="12" md="6">
            <v-card class="p-6 bg-white rounded-xl shadow-sm">
              <h2 class="text-xl font-semibold text-gray-800 mb-2">Chatbot Assistant</h2>
              <div class="text-gray-500 text-sm">
                Chatbot functionality coming soon...
              </div>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import UserInfo from './UserInfo.vue'
import FinancialStats from './FinancialStats.vue'
import BehaviorOverview from './BehaviorOverview.vue'
import DocumentUploader from './DocumentUploader.vue'
</script>
