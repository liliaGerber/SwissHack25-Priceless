<template>
  <v-container class=" bg-background text-white px-6 py-8 rounded-xl mx-auto space-y-8">

    <!-- Accounts -->
    <v-card flat class="bg-background p-0 rounded-xl overflow-hidden">
      <h2 class="text-lg font-semibold px-6 pt-6 pb-4">Bank Accounts</h2>
      <v-row
          dense
          class="no-gutters justify-start gap-0 max-w-fit"
      >
        <v-col
            v-for="(account, index) in financialData.accounts"
            :key="account.iban"
            cols="12"
            md="6"
            class="p-0 flex justify-start mx-0"
        >
          <v-card
              class="bg-secondary-background text-white px-6 py-5 rounded-none h-full w-full max-w-[300px]
               md:first:rounded-l-xl md:last:rounded-r-xl"
              flat
          >
            <div class="mb-3 text-lg font-semibold capitalize flex items-center">
              <v-icon size="20" class="mr-2 text-blue-400">mdi-bank</v-icon>
              {{ account.type }} Account
            </div>
            <div class="text-sm text-gray-300 space-y-1">
              <p><strong>IBAN:</strong> {{ account.iban }}</p>
              <p><strong>Balance:</strong> €{{ account.balance.toLocaleString() }}</p>
              <p><strong>Last Updated:</strong> {{ account.last_updated }}</p>

              <template v-if="account.monthly_inflow">
                <p><strong>Inflow:</strong> €{{ account.monthly_inflow }}</p>
                <p><strong>Outflow:</strong> €{{ account.monthly_outflow }}</p>
              </template>

              <template v-if="account.interest_rate">
                <p><strong>Interest Rate:</strong> {{ account.interest_rate }}%</p>
                <p><strong>Goal:</strong> {{ account.goal }}</p>
              </template>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-card>

  </v-container>
</template>

<script lang="ts" setup>
import {customer} from '@/data/customer.ts';

const financialData = customer.financial_data;
</script>
