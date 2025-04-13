<script setup lang="ts">
import NavbarWithLogin from "./components/NavbarWithLogin.vue";
import {useBasicApiDataStore} from "@/stores/BasicAPIData.ts";
import {onMounted} from "vue";


const customerStore = useBasicApiDataStore()

onMounted(async () => {
  await customerStore.getAllCustomers()
})

</script>
<template>
  <v-app>
    <NavbarWithLogin />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
