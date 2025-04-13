// stores/maininformationstore.ts
import {defineStore} from 'pinia';
import api from '../api/api';
import {Customer} from "@/types/Customer.ts";

export const useBasicApiDataStore = defineStore('basicData', {
    state: () => ({
        data: null,
        loading: false,
        error: null,
        customers: [] as Customer[]
    }),
    actions: {
        async fetchData() {
            this.loading = true;
            this.error = null;
            try {
                const response = await api.get('/');
                this.data = response.data;
            } catch (error: any) {
                this.error = error?.message || 'An unknown error occurred';
            } finally {
                this.loading = false;
            }
        },
        async chatWithBot(prompt: string, user_id: string) {
            this.loading = true;
            this.error = null;
            try {
                const response = await api.get('/rag/interaction', {params: {prompt: prompt, user_id: user_id}});
                this.data = response.data;
                return response.data;
            } catch (error: any) {
                this.error = error?.message || 'An unknown error occurred';
            } finally {
                this.loading = false;
            }
        }, async getAllCustomers() {
            this.loading = true;
            this.error = null;
            try {
                const response = await api.get('/customers');
                this.customers = response.data as Customer[];
                return this.customers as Customer[];
            } catch (error: any) {
                this.error = error?.message || 'An unknown error occurred';
            } finally {
                this.loading = false;
            }
        },
    },
});