<script lang="ts" setup>
import {useMainInformationStore} from "../stores/MainInformationStore";
import {useBasicApiDataStore} from "../stores/BasicAPIData";
import {onMounted} from "vue";

const mainInfo = useMainInformationStore();
const basicInfo = useBasicApiDataStore();

onMounted(() => {
  basicInfo.fetchData();
});
</script>

<template>
  <v-row class="row-layout">
    <v-col cols="6">
      <div class="titles">
      <h1 class="text-9xl text-primary-text">{{ mainInfo.companyNameGetter }}</h1>
      <h2 class="text-2xl text-secondary-text">{{ mainInfo.companySloganGetter }}</h2>
      <h2 class="text-2xl text-secondary-text">{{ basicInfo.data }}</h2>
      </div>
    </v-col>
    <v-col class="mr-0 " cols="6">
      <img src="../assets/WomenScreenSitting.gif" alt="GIF">
    </v-col>
  </v-row>
</template>

<style scoped>
.row-layout {
  width: 100vw;
  height: 100vh;
  z-index: -1;
  margin-right: 0;
  margin-top: 6rem;
}
.titles{
  margin-top: 25%;
  margin-left: 30%;
}
</style>