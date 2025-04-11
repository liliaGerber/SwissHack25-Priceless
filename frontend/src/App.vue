<script setup lang="ts">
import NavbarWithLogin from "./components/NavbarWithLogin.vue";
</script>
<template>
  <v-app>
    <NavbarWithLogin />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
