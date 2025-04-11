<script lang="ts" setup>
import { TeamMember } from '../types/TeamMember';
import { PropType } from "vue";

const props = defineProps({
  teamMember: { type: Object as PropType<TeamMember>, required: true }
});

const member = props.teamMember as TeamMember;
</script>

<template>
  <v-card class="bg-primary card-style hover-effect d-flex flex-column">
    <div class="profile-image-wrapper">
      <v-img :src="member.profilePic" class="profile-image" cover></v-img>
    </div>

    <v-card-title class="text-center text-xl font-bold">{{ member.name }}</v-card-title>
    <v-card-subtitle class="text-center text-lg text-gray-400">{{ member.role }}</v-card-subtitle>

    <v-card-text class="description flex-grow">
      {{ member.description }}
    </v-card-text>

    <v-spacer></v-spacer>

    <v-card-actions class="buttons-container">
      <v-btn :href="member.linkedin" target="_blank" class="social-btn">
        <v-icon icon="mdi-linkedin" size="35" />
      </v-btn>
      <v-btn :href="`mailto:${member.email}`" class="social-btn">
        <v-icon icon="mdi-email" size="35" />
      </v-btn>
      <v-btn :href="`tel:${member.phone}`" class="social-btn">
        <v-icon icon="mdi-phone" size="35" />
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<style scoped>
.card-style {
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100%;
}
.hover-effect:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.profile-image-wrapper {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px auto;
  border: 3px solid white;
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

@media (min-width: 1024px) {
  .profile-image-wrapper {
    width: 170px;
    height: 170px;
  }
}

.description {
  flex-grow: 1;
  text-align: center;
  font-size: 16px;
  color: #fff;
  min-height: 80px;
  overflow: scroll;
}

.buttons-container {
  display: flex;
  justify-content: center;
  gap: 10px;
  padding-bottom: 10px;
}

.social-btn {
  min-width: 50px;
  min-height: 50px;
  border-radius: 50%;
}
</style>
