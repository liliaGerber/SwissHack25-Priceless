<template>
  <v-card class="p-4">
    <h3 class="font-semibold text-xl mb-4">Upload Documents</h3>
    <v-file-input
      multiple
      label="Select files"
      variant="outlined"
      accept=".pdf,.doc,.zip,.png,.jpg"
      @change="handleUpload"
    />
    <div class="mt-2 text-sm text-gray-600">Supported: PDF, DOCX, ZIP, Images</div>
  </v-card>
</template>

<script setup lang="ts">
const handleUpload = (files: File[]) => {
  console.log('Uploaded files:', files)
  // handle upload logic here (emit or call API)
}
</script>
