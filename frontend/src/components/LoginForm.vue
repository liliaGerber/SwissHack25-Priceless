<template>
  <v-container class="flex h-75 items-center">
    <v-row justify="center" align="center" class="w-full mt-50">
      <v-col cols="12" sm="10" md="6" xl="4">
        <v-card class="pa-10 rounded-lg w-full max-w-xl mx-auto">
          <h1 class="text-primary-text text-4xl text-center mb-6 font-semibold">Login</h1>
          <v-form ref="formRef" v-model="isValid">
            <v-text-field
                v-model="form.email"
                label="Email"
                outlined
                required
                class="mb-4 text-lg"
                density="comfortable"
                :rules="[rules.required]"
            />
            <v-text-field
                v-model="form.password"
                label="Password"
                outlined
                required
                type="password"
                class="mb-6 text-lg"
                density="comfortable"
                :rules="[rules.required]"
            />
            <v-btn color="primary" class="w-full h-12 text-lg font-semibold" type="submit" :disabled="!isValid">
              <div v-if="!isLoading">Login</div>
              <v-progress-circular v-if="isLoading" color="secondary" indeterminate></v-progress-circular>
            </v-btn>
            <p class="text-center mt-4">
              <a href="#" class="text-primary-text hover:underline text-lg">Forgot Password?</a>
            </p>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from "vue";

export default defineComponent({
  name: "LoginForm",
  setup() {
    const form = reactive({
      email: "",
      password: "",
    });

    const isValid = ref(false);
    const formRef = ref();
    const isLoading = ref(false);

    const rules = {
      required: (value: string) => !!value || "This field is required.",
      email: (value: string) => {
        const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return pattern.test(value) || "Invalid email address.";
      },
    };

    return {
      form,
      isValid,
      isLoading,
      formRef,
      rules,
    };
  },
});
</script>

<style scoped>
v-card {
  max-width: 600px;
  width: 100%;
}

v-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;}
</style>
