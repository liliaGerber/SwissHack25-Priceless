<template>
  <v-card class="p-6 w-full bg-background rounded-xl text-white">
    <h2 class="text-xl font-semibold mb-4">Meeting Planner</h2>

    <v-textarea
        v-model="prompt"
        label="Enter prompt"
        auto-grow
        class="mb-4"
    />

    <v-btn :loading="loading" @click="fetchMeetingPlan" class="mb-4" color="primary">
      Generate Meeting Plan
    </v-btn>

    <v-alert v-if="error" type="error" class="mb-4">{{ error }}</v-alert>

    <v-alert
        v-if="meetingPlan"
        type="success"
        class="whitespace-pre-line"
    >
      {{ meetingPlan }}
    </v-alert>
  </v-card>
</template>

<script lang="ts" setup>
import {ref} from 'vue'
import {useRagStore} from '@/stores/ragStore'
import type {Customer} from '@/types/Customer'

const ragStore = useRagStore()
const prompt = ref('Plan a meeting with this customer including timing, topics, and roles.')
const meetingPlan = ref<string | null>(null)
const error = ref<string | null>(null)
const loading = ref(false)

const props = defineProps<{
  customer: Customer
}>()

async function fetchMeetingPlan() {
  loading.value = true
  error.value = null
  meetingPlan.value = null
  try {
    const result = await ragStore.queryPlan(prompt.value, props.customer.id)
    meetingPlan.value = typeof result === 'string' ? result : result?.answer || JSON.stringify(result)
  } catch (e: any) {
    error.value = e.message || 'Failed to generate meeting plan'
  } finally {
    loading.value = false
  }
}
</script>

