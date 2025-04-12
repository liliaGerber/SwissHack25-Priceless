<template>
  <div class="flex gap-6">
    <!-- Sidebar -->
    <CustomerSidebar
        :customers="customers"
        @select="selectedCustomer = $event"
    />

    <!-- Dashboard View -->
    <UserDashboardUser
        v-if="selectedCustomer"
        :customer="selectedCustomer"
        class="flex-1"
    />
    <div v-else class="text-white text-center text-lg mt-10">
      Please select a customer from the sidebar.
    </div>
  </div>
</template>

<script lang="ts" setup>
import {ref} from 'vue'
import CustomerSidebar from '@/components/SidebarComponent.vue'
import UserDashboardUser from '@/components/userDashboard/UserDashboardMain.vue'
import {customers} from '@/data/customers.ts'


const selectedCustomer = ref()
</script>
