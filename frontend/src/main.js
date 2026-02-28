import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // This looks for src/router/index.js

// Ensure there are no double .use(router) calls
const app = createApp(App)
app.use(router)
app.mount('#app')