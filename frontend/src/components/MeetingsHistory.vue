<template>
  <v-card class="p-12 mx-16 my-10 bg-background rounded-2xl text-white">
    <h2 class="text-2xl font-bold mb-8">All Meetings</h2>

    <v-progress-circular v-if="store.loading" indeterminate color="primary" class="mb-6 mx-auto" />
    <v-alert v-if="store.error" type="error" class="mb-4">{{ store.error }}</v-alert>

    <div v-for="meeting in store.meetings" :key="meeting._id" class="mb-10">
      <v-card class="p-10 bg-secondary-background rounded-xl shadow-lg space-y-6">
        <div class="p-6">
        <div class="flex justify-between items-start">
          <div class="flex flex-col gap-3">
            <h3 class="text-xl font-bold">{{ meeting.title }}</h3>
            <div class="flex gap-2 flex-wrap">
              <v-chip size="small" color="primary" variant="flat">Date: {{ meeting.date }}</v-chip>
              <v-chip size="small" color="primary" variant="flat">Duration: {{ meeting.durationMinutes }} min</v-chip>
              <v-chip size="small" color="primary" variant="flat">Customer: {{ meeting.customerId }}</v-chip>
            </div>
          </div>
        </div>

        <div>
          <h4 class="text-base font-semibold text-white mb-1 mt-4">Summary</h4>
          <p class="text-sm leading-relaxed text-gray-200">{{ meeting.summary }}</p>
        </div>

        <div v-if="meeting.nextSteps?.length">
          <h4 class="text-base font-semibold text-white mb-1 mt-4">Next Steps</h4>
          <v-timeline density="compact" align="start">
            <v-timeline-item
              v-for="(step, index) in meeting.nextSteps"
              :key="index"
              dot-color="primary"
              size="small"
              class="text-sm text-gray-100"
            >
              {{ step }}
            </v-timeline-item>
          </v-timeline>
        </div>
          </div>
      </v-card>
    </div>
  </v-card>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue'
import { useMeetingStore } from '@/stores/MeetingsStore.ts'

const store = useMeetingStore()

onMounted(() => {
  store.fetchAllMeetings()
})
</script>

<style scoped>
.v-card {
  background-color: #1e1e2f;
}
</style>
