<script setup lang="ts">
import {useMainInformationStore} from "../stores/MainInformationStore";

const mainStore = useMainInformationStore()


</script>

<template>
  <v-app-bar scroll-behavior="collapse" scroll-threshold="289" class="bg-secondary text-primary-text">
    <v-toolbar-title>{{mainStore.companyNameGetter}}</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn to="/">Home</v-btn>
    <v-btn to="/team">Team</v-btn>
    <v-btn to="/contact">Contact</v-btn>
  </v-app-bar>
</template>

<style scoped>
</style>