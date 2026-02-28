<template>
  <div class="container-fluid vh-100 d-flex flex-column home-bg">
    <nav class="navbar navbar-expand-lg navbar-dark bg-transparent px-4">
      <span class="navbar-brand fw-bold fs-4 text-white">
        Quiz Master V2
      </span>

      <div class="ms-auto d-flex align-items-center">
        <div v-if="!isLoggedIn">
          <button class="btn btn-outline-light me-2" @click="goLogin">
            Login
          </button>

          <button class="btn btn-warning" @click="goRegister">
            Sign Up
          </button>
        </div>

        <button v-else class="btn btn-success" @click="goDashboard">
          Go to Dashboard
        </button>
      </div>
    </nav>

    <div class="flex-grow-1 d-flex align-items-center justify-content-center">
      <HomeDescription />
    </div>
  </div>
</template>

<script>
import HomeDescription from "@/components/HomeDescription.vue"

export default {
  name: "HomeView",
  components: { HomeDescription },
  data() {
    return {
      // Logic to check login status immediately
      isLoggedIn: !!localStorage.getItem("access_token"),
    }
  },
  methods: {
    goLogin() {
      console.log("Login button clicked"); // Check your browser console!
      this.$router.push("/login").catch(err => console.log("Nav Error:", err));
    },
    goRegister() {
      this.$router.push("/register").catch(err => console.log("Nav Error:", err));
    },
    goDashboard() {
      const role = localStorage.getItem("role");
      this.$router.push(role === "admin" ? "/admin/dashboard" : "/dashboard");
    },
  },
}
</script>

<style scoped>
.home-bg {
  background: linear-gradient(135deg, #0f172a, #1e293b);
  /* Ensure the background doesn't block clicks */
  position: relative;
  z-index: 1;
}
.navbar {
  /* Ensure navbar is on top of any background elements */
  position: relative;
  z-index: 10;
}
</style>