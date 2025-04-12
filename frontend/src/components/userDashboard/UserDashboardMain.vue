<template>
  <v-container class="py-8 px-6 bg-gray-900 bg-background" fluid>
    <v-row dense>
      <!-- Left Column -->
      <v-col cols="12" md="4">
        <UserInfo/>
        <DocumentUploader class="mt-6"/>
      </v-col>

      <!-- Right Column -->
      <v-col cols="12" md="4">
        <BankAccountsCard/>
        <CreditScoreCard/>
        <BehaviorOverview class="mt-6"/>
        <CustomerSummary/>
        <gpt-chat-component/>
    </v-col>
      <v-col cols="12" md="4">
        <gpt-chat-component/>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import UserInfo from './UserInfo.vue'
import BankAccountsCard from './BankAccountsCard.vue'
import BehaviorOverview from './BehaviorOverview.vue'
import DocumentUploader from './DocumentUploader.vue'
import CreditScoreCard from './CreditScoreCard.vue'
import CustomerSummary from "./CustomerSummary.vue";
import GptChatComponent from "@/components/userDashboard/GptChatComponent.vue";
</script>
