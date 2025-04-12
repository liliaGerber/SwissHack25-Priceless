<template>
  <v-card
      flat
      class="bg-background text-white rounded-xl w-full min-w-[300px]"
  >
    <!-- Title Row -->
    <div class="flex items-center gap-2 mb-2">
      <h2 class="text-lg font-semibold px-6 pt-0 pb-0">Upload Documents</h2>
    </div>

    <!-- Upload Section -->
    <div class="bg-secondary-background ml-4 p-5 rounded-xl space-y-4">
      <!-- Upload Input -->
      <v-file-input
          v-model="uploadedFiles"
          label="Select files"
          multiple
          show-size
          prepend-icon="mdi-upload"
          class="text-white"
          hide-details
          variant="outlined"
          @update:model-value="handleUpload"
      />

      <!-- Uploaded File List -->
      <div v-if="fileList.length" class="space-y-3">
        <h3 class="text-sm font-semibold text-gray-400">Uploaded Files</h3>
        <div
            v-for="(file, index) in fileList"
            :key="index"
            class="flex items-center justify-between bg-[#2A2C3B] px-4 py-2 rounded-md text-sm"
        >
          <div>
            <p class="text-white font-medium">{{ file.name }}</p>
            <p class="text-gray-400 text-xs">{{ (file.size / 1024).toFixed(1) }} KB</p>
          </div>
          <v-btn
              icon
              size="small"
              class="text-red-400"
              @click="removeFile(index)"
              variant="text"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </div>
      </div>
    </div>
  </v-card>
</template>

<script lang="ts" setup>
import {ref} from 'vue'
import {Customer} from "@/types/Customer.ts";

const uploadedFiles = ref<File[] | null>(null)
const fileList = ref<File[]>([])

const props = defineProps<{
  customer: Customer
}>()

function handleUpload(files: File[] | File) {
  const fileArray = Array.isArray(files) ? files : [files];

  const existingNames = new Set(fileList.value.map(f => f.name));
  const newFiles = fileArray.filter(file => !existingNames.has(file.name));
  fileList.value.push(...newFiles);

  uploadedFiles.value = null;
}

function removeFile(index: number) {
  fileList.value.splice(index, 1)
}
</script>
