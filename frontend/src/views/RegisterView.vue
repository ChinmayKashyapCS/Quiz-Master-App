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

          <!-- Qualification -->
          <div class="mb-3">
            <label class="form-label fw-semibold">Qualification</label>
            <input
              type="text"
              class="form-control form-control-lg"
              placeholder="Your qualification (optional)"
              v-model="qualification"
            />
          </div>

          <!-- 🔥 UPDATED DOB FIELD (CALENDAR) -->
          <div class="mb-3">
            <label class="form-label fw-semibold">
              Date of Birth
            </label>

            <input
              type="date"
              class="form-control form-control-lg"
              v-model="dob_raw"
              :max="maxDate"
            />

            <!-- 🔥 EXTRA DISPLAY FORMAT -->
            <small class="text-muted">
              Selected: {{ formattedDOB || "Not selected" }}
            </small>
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

          <!-- Error -->
          <div v-if="error" class="alert alert-danger text-center">
            {{ error }}
          </div>

          <!-- Success -->
          <div v-if="success" class="alert alert-success text-center">
            {{ success }}
          </div>

          <!-- Register Button -->
          <div class="d-grid mb-3">
            <button type="submit" class="btn btn-success btn-lg">
              Register
            </button>
          </div>

          <!-- Login -->
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

      /* 🔥 NEW DOB STATES */
      dob_raw: "",      // yyyy-mm-dd from input
      dob: "",          // formatted DD-MM-YYYY

      password: "",
      confirm_password: "",
      error: null,
      success: null,

      /* 🔥 EXTRA STATE */
      debugMode: false
    }
  },

  computed: {

    /* 🔥 MAX DATE (NO FUTURE DOB) */
    maxDate(){
      return new Date().toISOString().split("T")[0]
    },

    /* 🔥 FORMATTED DOB */
    formattedDOB(){
      if(!this.dob_raw) return ""

      const [year, month, day] = this.dob_raw.split("-")

      return `${day}-${month}-${year}`
    }

  },

  methods: {

    /* 🔥 CONVERT DATE BEFORE SEND */
    prepareDOB(){

      if(!this.dob_raw){
        this.dob = null
        return
      }

      const [year, month, day] = this.dob_raw.split("-")

      this.dob = `${day}-${month}-${year}`
    },

    async register() {

      this.error = null
      this.success = null

      if (this.password !== this.confirm_password) {
        this.error = "Passwords do not match"
        return
      }

      /* 🔥 PREPARE DOB */
      this.prepareDOB()

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

    /* 🔥 DEBUG FUNCTION */
    logDOB(){
      if(this.debugMode){
        console.log("Raw:", this.dob_raw)
        console.log("Formatted:", this.dob)
      }
    }

  },

  watch:{
    dob_raw(){
      this.logDOB()
    }
  }

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

/* 🔥 EXTRA STYLE */
small{
  font-size: 0.75rem;
}

</style>