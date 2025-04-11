<template>
  <v-container height="90%">
    <v-row class="h-100 ml-10 mr-10" justify="center" align="center">
      <v-col cols="12" md="6">
        <div class="justify-center align-center mt-auto">
          <h1 class="text-primary-text text-6xl pr-10">Any questions?</h1>
        </div>
      </v-col>
      <v-col cols="12" md="6">
        <v-form ref="formRef" v-model="isValid" @submit.prevent="handleSubmit">
          <v-row>
            <v-col cols="12">
              <h1 class="text-primary-text text-4xl">Contact us</h1>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="form.name" label="Name" outlined required :rules="[rules.required]" />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="form.email" label="Email" outlined required :rules="[rules.required, rules.email]" />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="form.phone" label="Telephone Number" outlined />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="form.subject" label="Subject" outlined required :rules="[rules.required]" />
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="form.message" label="Message" outlined required :rules="[rules.required]" rows="5" />
            </v-col>
            <v-col cols="12">
              <v-btn color="primary" class="w-full" type="submit" :disabled="!isValid">
                <div v-if="!isLoading && !statusMessage">Submit</div>
                <v-progress-circular v-if="isLoading" color="secondary" indeterminate></v-progress-circular>
                <p v-if="statusMessage" class="text-green-500 mt-2">{{ statusMessage }}</p>
              </v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, reactive, ref } from "vue";
import emailjs from "emailjs-com";

export default defineComponent({
  name: "ContactForm",
  setup() {
    const form = reactive({
      name: "",
      email: "",
      phone: "",
      subject: "",
      message: "",
    });

    const isValid = ref(false);
    const formRef = ref();
    const statusMessage = ref("");
    const isLoading = ref(false);

    const rules = {
      required: (value: string) => !!value || "This field is required.",
      email: (value: string) => {
        const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return pattern.test(value) || "Invalid email address.";
      },
    };

    const handleSubmit = async () => {
      isLoading.value = true
      if (formRef.value?.validate()) {
        await sendEmail();
      }
      isLoading.value = false
    };

    const sendEmail = async () => {
      try {
        await emailjs.send(
            import.meta.env.VITE_EMAILJS_SERVICE_ID,
            import.meta.env.VITE_EMAILJS_TEMPLATE_ID,
            {
              from_name: form.name,
              from_email: form.email,
              from_phone: form.phone,
              subject: form.subject,
              message: form.message,
            },
            import.meta.env.VITE_EMAILJS_PUBLIC_KEY
        );
        statusMessage.value = "Message sent successfully!";

        // Clear form after successful submission
        formRef.value.reset()

      } catch (error) {
        console.error("Email sending failed:", error);
        statusMessage.value = "Error sending email. Please try again later.";
      }
    };

    return {
      form,
      isValid,
      isLoading,
      formRef,
      rules,
      handleSubmit,
      statusMessage,
    };
  },
});
</script>

<style scoped>
v-text-field {
  min-height: 50px !important;
}
</style>
