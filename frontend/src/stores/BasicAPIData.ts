// stores/maininformationstore.ts
import { defineStore } from 'pinia';
import api from '../api/api';

export const useBasicApiDataStore = defineStore('basicData', {
    state: () => ({
        data: null,
        loading: false,
        error: null,
    }),
    actions: {
        async fetchData() {
            this.loading = true;
            this.error = null;
            try {
                const response = await api.get('/');
                this.data = response.data;
            } catch (error : any) {
                this.error = error?.message || 'An unknown error occurred';
            } finally {
                this.loading = false;
            }
        },
    },
});