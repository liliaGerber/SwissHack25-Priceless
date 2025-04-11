import './style.css'
import { createApp } from 'vue'

import { vuetify } from "./plugins/vuetify";
import App from './App.vue'
import router from "./router";
import {createPinia} from "pinia";
const pinia = createPinia()

createApp(App).use(vuetify).use(router).use(pinia).mount('#app')
