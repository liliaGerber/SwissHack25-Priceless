<script lang="ts" setup>
// Simple Home page just with text

import {useMainInformationStore} from "../stores/MainInformationStore";
import BubbleBackground from "./backgrounds/BubbleBackground.vue";
// import {ref} from "vue";

const mainStore = useMainInformationStore();
/*const sectionRefEl = ref<HTMLElement | null>()
function scrollTo() {
  sectionRefEl.value?.scrollIntoView({ behavior: 'smooth' })
}*/
</script>

<template>
    <v-col class="w-100 align-content-center mt-32 z-50">
    <v-row class="flex-column align-center mt-0" >
      <h1 class="text-9xl text-primary text-medium-emphasis">{{ mainStore.companyNameGetter }}</h1>
      <h2>Sub text that look aesthetic describing something</h2>
    </v-row>
      <div class="mt-12">
    <v-row justify="center" class="flex-row align-content-center align-center ">
<!--      <v-btn class="mr-5 bg-white" @click="scrollTo()"> Learn more</v-btn>-->
      <v-btn class="mr-5 bg-white"> Learn more</v-btn>
      <v-btn class="ml-5 bg-white">Learn more</v-btn>
    </v-row>
      </div>
    </v-col>
  <BubbleBackground></BubbleBackground>

  <div class="background overflow-auto" style="z-index: -1;">
<!--  <div class="background overflow-auto" ref="sectionRefEl" style="z-index: -1;">-->

    <div class="mt-52 ml-52">
   Add content here
    </div>
  </div>
</template>

<style scoped>
.background {
  background: theme('colors.primary');
  width: 100%;
  margin-top: -30px;
  min-height: 100vh;
  z-index: 10 !important;
}
</style>