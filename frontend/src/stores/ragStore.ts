import {defineStore} from 'pinia'
import axios from 'axios'
import api from "@/api/api.ts";

export const useRagStore = defineStore('rag', {
    state: () => ({
        loading: false,
        error: null as string | null,
        result: null as string | null,
    }),

    actions: {
        async queryAgent(endpoint: string, prompt: string, userId: string) {
            this.loading = true
            this.error = null
            try {
                const res = await api.get(`/rag/${endpoint}`, {
                    params: {prompt, user_id: userId},
                })
                this.result = res.data
                return res.data
            } catch (err: any) {
                this.error = err?.response?.data?.error || err.message
            } finally {
                this.loading = false
            }
        },

        queryInvestment(prompt: string, userId: string) {
            return this.queryAgent('investment', prompt, userId)
        },

        queryRetirement(prompt: string, userId: string) {
            return this.queryAgent('retirement', prompt, userId)
        },

        queryCredit(prompt: string, userId: string) {
            return this.queryAgent('credit', prompt, userId)
        },

        querySummary(prompt: string, userId: string) {
            return this.queryAgent('summary', prompt, userId)
        },

        queryInteraction(prompt: string, userId: string) {
            return this.queryAgent('interaction', prompt, userId)
        },

        queryVision(prompt: string, userId: string) {
            return this.queryAgent('vision', prompt, userId)
        },

        queryMeeting(prompt: string, userId: string) {
            return this.queryAgent('meeting', prompt, userId)
        },

        queryPlan(prompt: string, userId: string) {
            return this.queryAgent('plan', prompt, userId)
        },
    },
})
