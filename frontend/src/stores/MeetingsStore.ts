import { defineStore } from 'pinia'
import api from "@/api/api.ts";

export const useMeetingStore = defineStore('meetings', {
  state: () => ({
    meetings: [] as any[],
    loading: false,
    error: null as string | null
  }),

  actions: {
    async fetchAllMeetings() {
      this.loading = true
      this.error = null
      try {
        const res = await api.get('/meetings')
        this.meetings = res.data
      } catch (e: any) {
        this.error = e.message || 'Failed to load meetings'
      } finally {
        this.loading = false
      }
    },

    async fetchMeetingsByCustomer(customerId: string) {
      this.loading = true
      this.error = null
      try {
        const res = await api.get(`/meetings/customer/${customerId}`)
        this.meetings = res.data
      } catch (e: any) {
        this.error = e.message || 'Failed to load meetings'
      } finally {
        this.loading = false
      }
    },

    async fetchMeetingsByAdvisor(advisorId: string) {
      this.loading = true
      this.error = null
      try {
        const res = await api.get(`/meetings/advisor/${advisorId}`)
        this.meetings = res.data
      } catch (e: any) {
        this.error = e.message || 'Failed to load meetings'
      } finally {
        this.loading = false
      }
    },

    async clearMeetings() {
      this.loading = true
      this.error = null
      try {
        await api.delete('/meetings/clear')
        this.meetings = []
      } catch (e: any) {
        this.error = e.message || 'Failed to clear meetings'
      } finally {
        this.loading = false
      }
    }
  }
})
