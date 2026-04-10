<template>
  <div class="container-fluid vh-100 d-flex flex-column home-bg">

    <!-- NAVBAR (UNCHANGED AS YOU SAID) -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-transparent px-4">
      <span class="navbar-brand fw-bold fs-4 text-white">
        Quiz Master V2
      </span>

      <div class="ms-auto d-flex align-items-center">
          <button class="btn btn-outline-light me-2" @click="goLogin">
            Login
          </button>

          <button class="btn btn-warning" @click="goRegister">
            Sign Up
          </button>
        </div>

    </nav>

    <!-- MAIN CONTENT -->
    <div class="flex-grow-1 d-flex align-items-center justify-content-center">

      <div class="content-wrapper text-center text-white px-4">

        <!-- TITLE -->
        <h1 class="display-4 fw-bold mb-3">
          Master Your Learning Journey
        </h1>

        <!-- SUBTITLE -->
        <p class="lead mb-4">
          Practice. Analyze. Improve. All in one intelligent quiz platform.
        </p>

        <!-- DESCRIPTION -->
        <p class="description-text mb-4">
          Quiz Master V2 is designed to help students enhance their knowledge through
          structured quizzes, real-time feedback, and detailed performance analytics.
          Track your progress across subjects and chapters, and identify areas that need improvement.
        </p>

        <!-- FEATURE LIST -->
        <div class="row justify-content-center mt-4">

          <div class="col-md-3 col-6 mb-3">
            <div class="feature-box">📚 Structured Learning</div>
          </div>

          <div class="col-md-3 col-6 mb-3">
            <div class="feature-box">📝 Timed Quizzes</div>
          </div>

          <div class="col-md-3 col-6 mb-3">
            <div class="feature-box">📊 Analytics Dashboard</div>
          </div>

          <div class="col-md-3 col-6 mb-3">
            <div class="feature-box">⚡ Instant Results</div>
          </div>

        </div>

        <!-- EXTRA TEXT -->
        <div class="mt-4 small text-light opacity-75">
          Built for students, educators, and exam preparation success.
        </div>

      </div>

    </div>

  </div>
</template>

<script>
export default {
  name: "HomeView",

  data() {
    return {

      /* KEEP ORIGINAL LOGIN LOGIC */
      isLoggedIn: !!localStorage.getItem("access_token"),

      /* EXTRA STATE (ADDED, NOT REMOVED) */
      debugMode: false

    }
  },

  methods: {

    goLogin() {
      console.log("Login button clicked");
      this.$router.push("/login").catch(err => console.log("Nav Error:", err));
    },

    goRegister() {
      this.$router.push("/register").catch(err => console.log("Nav Error:", err));
    },

    goDashboard() {
      const role = localStorage.getItem("role");
      this.$router.push(role === "admin" ? "/admin/dashboard" : "/dashboard");
    },

    /* EXTRA METHOD */
    logState(){
      if(this.debugMode){
        console.log("Home Loaded")
      }
    }

  },

  mounted(){
    this.logState()
  }

}
</script>

<style scoped>

/* 🔥 BACKGROUND IMAGE */
.home-bg {
  background-image: url("https://images.unsplash.com/photo-1523240795612-9a054b0db644");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;

  position: relative;
  z-index: 1;
}

/* 🔥 DARK OVERLAY */
.home-bg::before {
  content: "";
  position: absolute;
  inset: 0;
  background: rgba(15, 23, 42, 0.8);
  z-index: -1;
}

/* NAVBAR FIX */
.navbar {
  position: relative;
  z-index: 10;
}

/* 🔥 CONTENT ALIGNMENT */
.content-wrapper {
  max-width: 900px;
}

/* 🔥 DESCRIPTION TEXT */
.description-text {
  font-size: 1rem;
  line-height: 1.6;
  opacity: 0.9;
}

/* 🔥 FEATURE BOX */
.feature-box {
  background: rgba(255, 255, 255, 0.1);
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.95rem;
  backdrop-filter: blur(5px);
  transition: 0.3s;
}

.feature-box:hover {
  background: rgba(255, 255, 255, 0.2);
}

</style>