<template>
  <v-card
      flat
      class="bg-background text-white px-6 py-5 rounded-xl w-[600px] h-[800px] flex flex-col"
  >
    <!-- Title -->
    <div class="flex items-center gap-2 mb-2">
      <h2 class="text-lg font-semibold">Chat with GPT</h2>
    </div>
    <!-- Scrollable chat area grows above -->
    <div
        ref="chatContainer"
        class="bg-secondary-background p-4 rounded-xl text-sm overflow-y-auto flex-1 space-y-3"
    >
      <!-- Content flipped: input stays locked at bottom -->
      <div class="flex flex-col-reverse flex-1 overflow-hidden gap-4 h-[400px]">
        <!-- Input stays at bottom visually -->
        <div class="flex items-center gap-2 mt-4">
          <v-text-field
              v-model="message"
              placeholder="Type your message..."
              hide-details
              variant="outlined"
              density="comfortable"
              class="flex-1 bg-secondary-background text-white rounded-full"
              color="cyan"
              @keyup.enter="sendMessage"
          />
          <v-btn icon color="cyan" @click="sendMessage">
            <v-icon>mdi-send</v-icon>
          </v-btn>
        </div>

        <div
            ref="chatContainer"
            class="bg-secondary-background p-4 rounded-xl text-sm overflow-y-auto flex-1 flex flex-col-reverse gap-2"
        >
          <!-- Typing indicator -->
          <div v-if="isTyping" class="flex justify-start">
            <div class="bg-[#2A2C3B] text-gray-400 px-4 py-2 rounded-lg max-w-xs italic">
              GPT is typing...
            </div>
          </div>

          <!-- Render messages in reverse so new messages go above -->
          <div v-for="(entry, index) in [...chatLog].reverse()" :key="index">
            <div
                class="flex"
                :class="entry.sender === 'user' ? 'justify-end' : 'justify-start'"
            >
              <div
                  class="px-3 py-2 rounded-lg max-w-xs"
                  :class="entry.sender === 'user'
              ? 'bg-cyan-400 text-white'
              : 'bg-[#2A2C3B] text-gray-200'"
              >
                {{ entry.message }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </v-card>
</template>
<script lang="ts" setup>
import { ref, nextTick, onMounted } from 'vue'

const message = ref('')
const isTyping = ref(false)
const chatLog = ref<{ sender: 'user' | 'gpt'; message: string }[]>([])
const chatContainer = ref<HTMLElement | null>(null)

onMounted(() => {
  chatLog.value.push({
    sender: 'gpt',
    message: 'Hi! What would you like to know today?',
  })

  scrollToBottom()
})

function sendMessage() {
  if (!message.value.trim()) return

  const userMessage = message.value.trim()
  chatLog.value.push({ sender: 'user', message: userMessage })
  message.value = ''

  scrollToBottom()

  isTyping.value = true

  setTimeout(() => {
    isTyping.value = false
    chatLog.value.push({ sender: 'gpt', message: userMessage })
    scrollToBottom()
  }, 1000)
}

function scrollToBottom() {
  nextTick(() => {
    requestAnimationFrame(() => {
      if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight
      }
    })
  })
}
</script>