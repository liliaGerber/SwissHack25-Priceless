<script lang="ts" setup>
import TeamMemberCard from "./TeamMemberCard.vue";
import { TeamMember } from "../types/TeamMember";
import teamMembersJson from "../settings/teamMembers.json"

const teamMembers = teamMembersJson as TeamMember[];
</script>

<template>
  <v-container fluid class="container-position mt-lg-16">
    <v-row class="w-100 justify-center">
      <v-col
          v-for="member in teamMembers"
          :key="member.name"
          class="d-flex justify-center"
          cols="12" xs="12" sm="6" md="4" lg="3"
      >
        <TeamMemberCard class="card-props" :team-member="member" />
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.container-position {
  width: 90%;
  margin: auto;
}

.card-props {
  height: auto;
  width: 100%;
  max-width: 400px;
  max-height: 600px;
}

@media (min-width: 1024px) {
  .card-props {
    max-width: 350px;
  }
}

@media (min-width: 1440px) {
  .card-props {
    max-width: 400px;
  }
}
</style>
