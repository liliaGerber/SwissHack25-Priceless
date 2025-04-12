<template>
  <v-card
      flat
      class="bg-background text-white px-6 py-5 rounded-xl w-full"
  >
    <h2 class="text-lg font-semibold mb-6">Topic Overview</h2>

    <!-- Section Template -->
    <div v-for="section in topicSections" :key="section.title" class="mb-6">
      <h3 class="text-md font-semibold text-white mb-3 px-1">
        {{ section.title }}
      </h3>

      <div class="bg-background rounded-xl">
        <ul class=" divide-gray-700">
          <li
              v-for="(item, index) in section.items"
              :key="section.key + '-' + index"
              class="hover:bg-gray-300 px-4 py-3 mb-3 cursor-pointer rounded-xl bg-secondary-background transition "
              @click="handleClick(section.title, item)"
          >
            <span class="text-sm text-gray-300">{{ item }}</span>
          </li>
          <li
              v-if="!section.items.length"
              class="text-sm text-gray-500 italic px-4 py-3"
          >
            No {{ section.title.toLowerCase() }}.
          </li>
        </ul>
      </div>
    </div>
  </v-card>
</template>

<script lang="ts" setup>
import type { Customer } from '@/types/Customer'
import { computed } from 'vue'

const props = defineProps<{
  customer: Customer
}>()

const handleClick = (sectionTitle: string, item: string) => {
  console.log(`Clicked on "${item}" in "${sectionTitle}"`)
  // You can emit here or trigger dialog/etc.
}

const topicSections = computed(() => [
  {
    title: 'Current Topics',
    key: 'current',
    items: props.customer.suggestions || []
  },
  {
    title: 'Upcoming Topics',
    key: 'upcoming',
    items: props.customer.upcomingTopics || []
  },
  {
    title: 'Discussed Topics',
    key: 'discussed',
    items: props.customer.interactions?.map((i) => i.note) || []
  }
])
</script>
