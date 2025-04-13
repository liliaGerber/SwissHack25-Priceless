<template>
  <v-container class="py-8 px-6 bg-background min-h-screen" fluid>
    <v-row dense>
      <!-- Sidebar with User Info and Tabs -->
      <v-col cols="12" md="4" class="flex flex-col gap-6">
        <!-- Always-visible User Info -->
        <UserInfo :customer="customer"/>
        <BankAccountsCard :customer="customer"/>
        <CreditScoreCard :customer="customer" class="mt-5"/>
      </v-col>
      <v-col cols="12" md="2" class="flex flex-col gap-6">
        <!-- Vertical Tabs -->
        <v-card flat class="bg-secondary-background text-white rounded-xl h-full max-h-[375px] items-center">
          <v-tabs
              v-model="tab"
              direction="vertical"
              class="bg-secondary-background text-white"
              slider-color="white"
          >
            <v-tab
                v-for="(section, i) in sections"
                :key="i"
                class="justify-start text-left"
            >
              {{ section.label }}
            </v-tab>
          </v-tabs>
        </v-card>
      </v-col>

      <!-- Dynamic Tab Content -->
      <v-col cols="12" md="6">
        <v-window v-model="tab">
          <v-window-item :value="0">
            <CustomerSummary :customer="customer"/>
            <TopicsCard :customer="customer"/>

          </v-window-item>
          <v-window-item :value="1">
            <PlanMyMeeting :customer="customer"/>
          </v-window-item>
          <v-window-item :value="2">
            <div class="w-full h-full gap-2 ml-2">
              <BankAccountsCard :customer="customer"/>
              <CreditScoreCard :customer="customer" class="mt-5"/>
            </div>
          </v-window-item>
          <v-window-item :value="3">
            <BehaviorOverview :customer="customer"/>
          </v-window-item>
          <v-window-item :value="4">
            <MeetingHistoryByUser :customer="customer"/>
          </v-window-item>
          <v-window-item :value="5">
            <DocumentUploader :customer="customer"/>
          </v-window-item>
          <v-window-item :value="6">
            <GptChatComponent :customer="customer"/>
          </v-window-item>
        </v-window>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import {ref} from 'vue'
import type {Customer} from '@/types/Customer'

import UserInfo from './UserInfo.vue'
import DocumentUploader from './DocumentUploader.vue'
import CustomerSummary from './CustomerSummary.vue'
import TopicsCard from './TopicsCard.vue'
import BankAccountsCard from './BankAccountsCard.vue'
import CreditScoreCard from './CreditScoreCard.vue'
import BehaviorOverview from './BehaviorOverview.vue'
import GptChatComponent from '@/components/userDashboard/GptChatComponent.vue'
import PlanMyMeeting from "@/components/userDashboard/PlanMyMeeting.vue";
import MeetingHistoryByUser from "@/components/userDashboard/MeetingHistoryByUser.vue";

const props = defineProps<{ customer: Customer }>()

const tab = ref(0)

const sections = [
  {label: 'Summary'},
  {label: 'Plan my meeting'},
  {label: 'Wealth'},
  {label: 'Behavior'},
  {label: 'Meeting history'},
  {label: 'Documents'},
  {label: 'Chat'}
]
</script>
