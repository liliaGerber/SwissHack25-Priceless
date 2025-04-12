<template>
  <v-card
      flat
      class="bg-background text-white px-4 py-5  w-full max-w-[280px] h-full"
  >
    <h2 class="text-lg font-semibold px-2 mb-4">Customers</h2>

    <div class="flex flex-col gap-2 overflow-y-auto h-[calc(100vh-100px)]">
      <v-btn
          v-for="customer in customers"
          :key="customer.id"
          class="bg-secondary-background text-left text-white justify-start px-4 py-2 rounded-lg hover:bg-gray-700 transition"
          variant="flat"
          @click="selectCustomer(customer)"
      >
        {{ customer.name }}
      </v-btn>
    </div>
  </v-card>
</template>

<script lang="ts" setup>
import type { Customer } from '@/types/Customer'
import { defineEmits, onMounted, ref } from 'vue'
import { useBasicApiDataStore } from '@/stores/BasicAPIData.ts'

const customerStore = useBasicApiDataStore()
const customers = ref<Customer[]>([])

const emit = defineEmits<{
  (e: 'select', customer: Customer): void
}>()

function selectCustomer(customer: Customer) {
  emit('select', customer)
}

onMounted(async () => {
  await customerStore.getAllCustomers()
  customers.value = customerStore.customers
})
</script>
