<template>
  <div class="dashboard-bg min-vh-100">
    <!-- NAVBAR -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary px-4">
      <span class="navbar-brand fw-bold">Quiz Master</span>

      <div class="ms-auto d-flex align-items-center gap-3">
        <input
          v-model="search"
          class="form-control form-control-sm"
          placeholder="Search quizzes..."
        />
        <span class="text-white">Welcome, User</span>
        <button class="btn btn-outline-light btn-sm" @click="logout">
          Logout
        </button>
      </div>
    </nav>

    <!-- CONTENT -->
    <div class="container mt-4">
      <!-- TOP NAV -->
      <div class="mb-3 d-flex gap-3">
        <router-link class="btn btn-outline-primary btn-sm" to="/dashboard">
          Home
        </router-link>
        <router-link class="btn btn-outline-primary btn-sm" to="/scores">
          Scores
        </router-link>
        <router-link class="btn btn-outline-primary btn-sm" to="/summary">
          Summary
        </router-link>
      </div>

      <!-- UPCOMING QUIZZES -->
      <div class="card shadow-sm">
        <div class="card-header bg-light fw-semibold">
          Upcoming Quizzes
        </div>

        <div class="card-body p-0">
          <table class="table table-hover mb-0 text-center">
            <thead class="table-secondary">
              <tr>
                <th>ID</th>
                <th>No. of Questions</th>
                <th>Date</th>
                <th>Duration</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="quiz in filteredQuizzes" :key="quiz.id">
                <td>{{ quiz.id }}</td>
                <td>{{ quiz.question_count }}</td>
                <td>{{ quiz.date_of_quiz }}</td>
                <td>{{ quiz.duration }}</td>
                <td>
                  <div class="d-flex justify-content-center gap-2">
                    <button
                      class="btn btn-outline-info btn-sm"
                      @click="viewQuiz(quiz.id)"
                    >
                      View
                    </button>
                    <button
                      class="btn btn-success btn-sm"
                      @click="startQuiz(quiz.id)"
                    >
                      Start
                    </button>
                  </div>
                </td>
              </tr>

              <tr v-if="filteredQuizzes.length === 0">
                <td colspan="5" class="text-muted py-3">
                  No quizzes found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserDashboard",

  data() {
    return {
      search: "",
      quizzes: [],
    }
  },

  computed: {
    filteredQuizzes() {
      return this.quizzes.filter(q =>
        q.id.toString().includes(this.search)
      )
    },
  },

  async mounted() {
    await this.fetchQuizzes()
  },

  methods: {
    async fetchQuizzes() {
      try {
        const token = localStorage.getItem("access_token")

        const res = await fetch("/api/quizzes", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        const data = await res.json()
        this.quizzes = data
      } catch (err) {
        console.error("Failed to load quizzes")
      }
    },

    viewQuiz(id) {
      this.$router.push(`/quiz/view/${id}`)
    },

    async startQuiz(id) {
      const token = localStorage.getItem("access_token")

      await fetch(`/api/quiz/attempt/${id}`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      this.$router.push(`/quiz/start/${id}`)
    },

    logout() {
      localStorage.clear()
      this.$router.push("/login")
    },
  },
}
</script>

<style scoped>
.dashboard-bg {
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
}

.navbar input {
  width: 200px;
}

.table th,
.table td {
  vertical-align: middle;
}

.card {
  border-radius: 12px;
}
</style>
