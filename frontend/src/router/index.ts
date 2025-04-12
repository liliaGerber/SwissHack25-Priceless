
import {createRouter, createWebHistory} from 'vue-router'
import { RouteRecordRaw } from 'vue-router'
import TeamMemberCardGrid from "../components/TeamMemberCardGrid.vue";
import ContactForm from "../components/ContactForm.vue";
import SplitHomepage from "../components/SplitHomepage.vue";
import LoginForm from "../components/LoginForm.vue";
import UserDashboardMain from "@/components/userDashboard/UserDashboardMain.vue";

const routes: Array<RouteRecordRaw> = [
    {
        path: '/',
        name: 'Home',
        component: UserDashboardMain,
    },
    {
        path: '/team',
        name: 'Team',
        component: TeamMemberCardGrid,
    },
    {
        path: '/contact',
        name: 'Contact',
        component: ContactForm,
    },
    {
        path: '/login',
        name: 'Login',
        component: LoginForm,
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router