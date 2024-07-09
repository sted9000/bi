// src/router.js
import { createRouter, createWebHistory } from 'vue-router';
import Login from './components/Login.vue';
import Dashboard from './components/Dashboard.vue';
import Preshift from "@/components/Preshift";
import { supabase } from './supabase';
import TrendsComponent from "@/components/TrendsComponent";

const routes = [
    {
        path: '/',
        name: 'CHC Daily Report',
        component: Dashboard,
        meta: { requiresAuth: true },
    },
    {
        path: '/login',
        name: 'LoginComponent',
        component: Login,
    },
    {
        path: '/trends',
        name: 'CHC Trends',
        component: TrendsComponent,
        meta: { requiresAuth: true },
    },
    {
        path: '/preshift',
        name: 'PreshiftComponent',
        component: Preshift,
        meta: { requiresAuth: true },
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach(async (to, from, next) => {
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
    const user = (await supabase.auth.getSession()).data?.session?.user;

    if (requiresAuth && !user) {
        next('/login');
    } else {
        next();
    }
});

export default router;
