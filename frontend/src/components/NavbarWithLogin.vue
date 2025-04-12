<script lang="ts" setup>

// Navbar with login button, collapsible
import {useMonitorSize} from "../composables/monitor-size";
import {ref} from "vue";
import {useMainInformationStore} from "../stores/MainInformationStore";

const screenSizes = useMonitorSize();
const drawer = ref(false);

const links = [
  {name: "Home", path: "/"},
  {name: "My Customers", path: "/team"},
  {name: "History", path: "/contact"},
];
const mainStore = useMainInformationStore();
</script>

<template>
  <!--  Desktop View-->
  <v-app-bar v-if="!screenSizes.isMobile.value" class="justify-evenly bg-secondary-background" elevation="0">
    <v-app-bar-title class="max-w-fit">{{ mainStore.companyNameGetter }}</v-app-bar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items >
      <template v-for="link in links">
        <router-link :to=link.path class="pa-5 align-center mt-auto">{{ link.name }}</router-link>
      </template>
    </v-toolbar-items>
    <v-spacer></v-spacer>
    <v-btn to="/login">Login</v-btn>
  </v-app-bar>

  <!--  Mobile View-->
  <v-app-bar v-if="screenSizes.isMobile.value" class="justify-between">
    <v-app-bar-title>{{ mainStore.companyNameGetter }}</v-app-bar-title>
    <v-toolbar-items>
      <v-btn @click="drawer = !drawer">
        <v-icon icon="mdi-menu" size="30"/>
      </v-btn>
    </v-toolbar-items>
  </v-app-bar>

  <v-navigation-drawer
      v-model="drawer"
      :width="screenSizes.browserWidth.value"
      class="h-100"
      temporary
  >
    <v-list density="compact" nav>
      <template v-for="link in links" class="flex-row ">
        <v-list-item :to=link.path class="pa-5 align-center mt-auto">{{ link.name }}</v-list-item>
      </template>
    </v-list>
  </v-navigation-drawer>
</template>

