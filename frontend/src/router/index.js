import { createRouter, createWebHistory } from "vue-router"
// Use relative paths (./ or ../) to be safe
import HomeView from "../views/HomeView.vue"

const routes = [
  { path: "/", name: "home", component: HomeView },
  { 
    path: "/login", 
    name: "login", 
    component: () => import("../views/LoginView.vue") 
  },
  { 
    path: "/register", 
    name: "register", 
    component: () => import("../views/RegisterView.vue") 
  },
  { 
    path: "/dashboard", 
    component: () => import("../views/UserDashboard.vue"),
    meta: { requiresAuth: true } 
  },
  { 
    path: "/admin/dashboard", 
    component: () => import("../views/AdminDashboard.vue"),
    meta: { requiresAuth: true, role: 'admin' } 
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router