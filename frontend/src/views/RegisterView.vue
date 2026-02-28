<template>
  <div class="register-page d-flex align-items-center justify-content-center">
    <div class="card shadow-lg border-0 register-card">
      <div class="card-body p-5">
        <h2 class="text-center mb-4 fw-bold text-success">
          Create Account
        </h2>

        <form @submit.prevent="register">
          <!-- Full Name -->
          <div class="mb-3">
            <label class="form-label fw-semibold">Full Name</label>
            <input
              type="text"
              class="form-control form-control-lg"
              placeholder="Enter your full name"
              v-model="full_name"
              required
            />
          </div>

          <!-- Email -->
          <div class="mb-3">
            <label class="form-label fw-semibold">Email address</label>
            <input
              type="email"
              class="form-control form-control-lg"
              placeholder="Enter your email"
              v-model="email"
              required
            />
          </div>

          <!-- Qualification (optional) -->
          <div class="mb-3">
            <label class="form-label fw-semibold">Qualification</label>
            <input
              type="text"
              class="form-control form-control-lg"
              placeholder="Your qualification (optional)"
              v-model="qualification"
            />
          </div>

          <!-- Date of Birth (optional) -->
          <div class="mb-3">
            <label class="form-label fw-semibold">
              Date of Birth (DD-MM-YYYY)
            </label>
            <input
              type="text"
              class="form-control form-control-lg"
              placeholder="DD-MM-YYYY"
              v-model="dob"
            />
          </div>

          <!-- Password -->
          <div class="mb-3">
            <label class="form-label fw-semibold">Password</label>
            <input
              type="password"
              class="form-control form-control-lg"
              placeholder="Create a password"
              v-model="password"
              required
            />
          </div>

          <!-- Confirm Password -->
          <div class="mb-4">
            <label class="form-label fw-semibold">Confirm Password</label>
            <input
              type="password"
              class="form-control form-control-lg"
              placeholder="Re-enter password"
              v-model="confirm_password"
              required
            />
          </div>

          <!-- Error Message -->
          <div v-if="error" class="alert alert-danger text-center">
            {{ error }}
          </div>

          <!-- Success Message -->
          <div v-if="success" class="alert alert-success text-center">
            {{ success }}
          </div>

          <!-- Register Button -->
          <div class="d-grid mb-3">
            <button type="submit" class="btn btn-success btn-lg">
              Register
            </button>
          </div>

          <!-- Login Redirect -->
          <div class="text-center">
            <span class="text-muted">Already have an account?</span>
            <router-link
              to="/login"
              class="fw-semibold text-decoration-none ms-1"
            >
              Login
            </router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "RegisterView",

  data() {
    return {
      full_name: "",
      email: "",
      qualification: "",
      dob: "",
      password: "",
      confirm_password: "",
      error: null,
      success: null,
    }
  },

  methods: {
    async register() {
      this.error = null
      this.success = null

      if (this.password !== this.confirm_password) {
        this.error = "Passwords do not match"
        return
      }

      try {
        const response = await fetch("/api/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            full_name: this.full_name,
            email: this.email,
            password: this.password,
            qualification: this.qualification || null,
            dob: this.dob || null,
          }),
        })

        const data = await response.json()

        if (!response.ok) {
          this.error = data.message || "Registration failed"
          return
        }

        this.success = "Registration successful! Redirecting to login..."

        setTimeout(() => {
          this.$router.push("/login")
        }, 1500)

      } catch (err) {
        this.error = "Server unavailable. Please try again later."
      }
    },
  },
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #ecfdf5, #f0fdf4);
}

.register-card {
  width: 100%;
  max-width: 460px;
  border-radius: 1rem;
}

input:focus {
  box-shadow: none;
  border-color: #198754;
}
</style>
