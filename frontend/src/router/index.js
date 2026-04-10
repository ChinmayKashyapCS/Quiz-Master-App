import { createRouter, createWebHistory } from "vue-router"
import HomeView from "../views/HomeView.vue"
import ChapterView from "../views/ChapterView.vue"

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
  },
  {
    path: "/admin/subjects",
    component: () => import("../views/SubjectView.vue"),
    meta: { requiresAuth: true, role: "admin" }
  },
  {
    path: "/admin/chapters",
    name: "chapters",
    component: ChapterView,
    meta: { requiresAuth: true, role: "admin" }
  },
  {
    path: "/admin/quizzes",
    component: () => import("../views/QuizView.vue")
  },
  {
    path: "/scores",
    name: "scores",
    component: () => import("../views/ScoreUser.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: "/exam/:quiz_id",
    name: "exam",
    component: () => import("../views/QuizExam.vue"),
    meta: { requiresAuth: true, role: "user" }
  },
  {
    path: "/user/stats",
    name: "user-stats",
    component: () => import("../views/UserStats.vue"),
    meta: { requiresAuth: true }
  },
  {
    path: "/admin/stats",
    name: "admin-stats",
    component: () => import("../views/AdminStats.vue"),
    meta: { requiresAuth: true, role: "admin" }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})



router.beforeEach((to, from, next) => {

  const token = localStorage.getItem("access_token")
  const role = localStorage.getItem("role")

  if (to.meta.requiresAuth && !token) {
    next("/login")
  }
  else if (to.meta.role && role !== to.meta.role) {
    next("/")
  }
  else {
    next()
  }

})

export default router