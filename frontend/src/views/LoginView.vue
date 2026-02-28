<template>
  <div class="login-page d-flex align-items-center justify-content-center">
    <div class="card shadow-lg border-0 login-card">
      <div class="card-body p-5">
        <h2 class="text-center mb-4 fw-bold text-primary">
          Quiz Master Login
        </h2>

        <form @submit.prevent="login">
          <div class="mb-3">
            <label class="form-label fw-semibold">Email address</label>
            <input
              type="email"
              class="form-control form-control-lg"
              placeholder="Enter your email"
              v-model="email"
              :disabled="loading"
              required
            />
          </div>

          <div class="mb-4">
            <label class="form-label fw-semibold">Password</label>
            <input
              type="password"
              class="form-control form-control-lg"
              placeholder="Enter your password"
              v-model="password"
              :disabled="loading"
              required
            />
          </div>

          <div v-if="error" class="alert alert-danger text-center">
            {{ error }}
          </div>

          <div class="d-grid mb-3">
            <button type="submit" class="btn btn-primary btn-lg" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              {{ loading ? 'Logging in...' : 'Login' }}
            </button>
          </div>

          <div class="text-center">
            <span class="text-muted">Don’t have an account?</span>
            <router-link
              to="/register"
              class="fw-semibold text-decoration-none ms-1"
            >
              Sign up
            </router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { jwtDecode } from "jwt-decode"; 

export default {
  name: "LoginView",

  data() {
    return {
      email: "",
      password: "",
      error: null,
      loading: false,
    };
  },

  methods: {
    async login() {
      this.error = null;
      this.loading = true;

      try {
        // Changed to localhost to avoid some 127.0.0.1 browser restrictions
        const response = await fetch("http://localhost:5000/api/login", {
          method: "POST",
          headers: { 
            "Content-Type": "application/json",
            "Accept": "application/json"
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
          }),
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(data.message || "Invalid credentials");
        }

        const data = await response.json();

        // 1. Save Token
        localStorage.setItem("access_token", data.access_token);

        // 2. Decode JWT
        const decoded = jwtDecode(data.access_token);
        
        // Match the role structure from your Backend (sub is common in Flask-JWT-Extended)
        const role = decoded.role || (decoded.sub && decoded.sub.role) || decoded.sub;

        // 3. Save Role & Username (useful for the dashboard display)
        localStorage.setItem("role", role);
        if (decoded.sub && decoded.sub.username) {
            localStorage.setItem("username", decoded.sub.username);
        }

        // 4. Role-Based Redirect
        if (role === "admin") {
          this.$router.push("/admin/dashboard");
        } else {
          this.$router.push("/dashboard");
        }

      } catch (err) {
        console.error("Fetch encountered an error:", err);
        // Better error message for "Failed to Fetch" (Network error)
        this.error = err.message === 'Failed to fetch' 
            ? "Cannot connect to server. Ensure Flask is running on port 5000." 
            : err.message;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
/* Styles remain exactly as you provided */
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #eef2ff, #f8fafc);
}
.login-card {
  width: 100%;
  max-width: 420px;
  border-radius: 1rem;
}
input:focus {
  box-shadow: none;
  border-color: #4f46e5;
}
</style>