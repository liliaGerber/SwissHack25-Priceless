// stores/maininformationstore.ts
import { defineStore } from 'pinia';

export const useMainInformationStore = defineStore('main', {
    state: () => ({
        companyName: "Priceless",
        companySlogan: "Ich will nicht mehr, ich kann nicht mehr, ich halte das alles nicht mehr aus"
    }),
    getters: {
        companyNameGetter: (state) => state.companyName,
        companySloganGetter: state => state.companySlogan
    }
});