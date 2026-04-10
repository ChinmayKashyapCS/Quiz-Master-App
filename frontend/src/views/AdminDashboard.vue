<template>
  <div class="dashboard-bg min-vh-100 pb-5">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark px-4 shadow sticky-top">
      <div class="container-fluid">
        <router-link to="/admin/dashboard" class="navbar-brand fw-bold">
          Admin Dashboard
        </router-link>

        <div class="mx-auto text-center d-none d-md-block">
          <span class="text-white-50 small d-block">Quiz Master V2</span>
          <span class="text-white fw-semibold">Welcome, {{ adminName }}</span>
        </div>

        <div class="d-flex align-items-center gap-3">
          <router-link to="/admin/stats" class="btn btn-outline-info btn-sm px-3">
            Stats
          </router-link>
          <button class="btn btn-danger btn-sm px-3" @click="logout">
            Logout
          </button>
        </div>
      </div>
    </nav>

    <div class="container mt-4">
      <div class="row mb-5 g-4 text-center">
        <div class="col-md-4">
          <router-link to="/admin/subjects" class="action-card btn btn-primary w-100 py-4 shadow-sm">
            <i class="bi bi-book fs-2"></i>
            <div class="fs-4 mt-2">Subjects</div>
          </router-link>
        </div>
        <div class="col-md-4">
          <router-link to="/admin/chapters" class="action-card btn btn-success w-100 py-4 shadow-sm">
            <i class="bi bi-journal-text fs-2"></i>
            <div class="fs-4 mt-2">Chapters</div>
          </router-link>
        </div>
        <div class="col-md-4">
          <router-link to="/admin/quizzes" class="action-card btn btn-warning w-100 py-4 shadow-sm text-dark">
            <i class="bi bi-question-circle fs-2"></i>
            <div class="fs-4 mt-2">Quizzes</div>
          </router-link>
        </div>
      </div>

      <!-- QUIZ LIST -->
      <div class="card shadow-sm mb-5 border-0">
        <div class="card-header bg-white d-flex justify-content-between align-items-center py-3">
          <h5 class="mb-0 fw-bold"><i class="bi bi-list-ul me-2"></i>List of Quizzes</h5>
          <div class="d-flex gap-2 w-50 justify-content-end">
            <input v-model="quizSearch" class="form-control form-control-sm w-50" placeholder="Search quizzes by ID...">
          </div>
        </div>

        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0 text-center">
            <thead class="table-light">
              <tr>
                <th>Quiz ID</th>
                <th>Chapter ID</th>
                <th>Duration</th>
                <th>Average %</th>
                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="quiz in filteredQuizzes" :key="quiz.id">
                <td>#{{ quiz.id }}</td>
                <td>{{ quiz.chapter_id }}</td>
                <td>{{ quiz.time_duration }} mins</td>
                <td>{{ getQuizStats(quiz.id).avg }}%</td>
                <td>
                  <button class="btn btn-sm btn-outline-primary" @click="viewQuizSummary(quiz)">
                    Summary
                  </button>
                </td>
              </tr>

              <tr v-if="filteredQuizzes.length === 0">
                <td colspan="5" class="text-muted py-3">No quizzes found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- REGISTERED USERS -->
      <div class="card shadow-sm mb-5 border-0">
        <div class="card-header bg-white d-flex justify-content-between align-items-center py-3">
          <h5 class="mb-0 fw-bold"><i class="bi bi-people me-2"></i>Registered Users</h5>
          <input v-model="userSearch" class="form-control form-control-sm w-25" placeholder="Search users...">
        </div>

        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0 text-center">
            <thead class="table-light">
              <tr>
                <th>ID</th><th>Name</th><th>Email</th><th>DoB</th><th>Qualification</th><th>Action</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="user in filteredUsers" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.full_name || user.username }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.dob || 'N/A' }}</td>
                <td>{{ user.qualification || 'N/A' }}</td>
                <td>
                  <button class="btn btn-sm btn-info text-white px-3" @click="viewUserQuizzes(user)">
                    View
                  </button>
                </td>
              </tr>

              <tr v-if="filteredUsers.length === 0">
                <td colspan="6" class="text-muted py-3">No users found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- QUIZ ATTEMPTS -->
      <div class="card shadow-sm border-0">
        <div class="card-header bg-white d-flex justify-content-between align-items-center py-3">
          <h5 class="mb-0 fw-bold">
            <i class="bi bi-clipboard-check me-2"></i>Quiz Attempts
          </h5>
          <input
            v-model="attemptSearch"
            class="form-control form-control-sm w-25"
            placeholder="Search attempts..."
          >
        </div>

        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0 text-center">
            <thead class="table-light">
              <tr>
                <th>Quiz ID</th>
                <th>User ID</th>
                <th>User Name</th>
                <th>Chapter ID</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="attempt in filteredAttempts" :key="attempt.id">
                <td>#{{ attempt.quiz_id }}</td>
                <td>{{ attempt.user_id }}</td>
                <td>{{ getUserName(attempt.user_id) }}</td>
                <td>{{ attempt.chapter_id || 'N/A' }}</td>

                <td>
                  <button
                    class="btn btn-sm btn-outline-secondary"
                    @click="viewAttemptOverview({ ...attempt })"
                  >
                    Overview
                  </button>
                  <div v-if="selectedAttemptOverview" class="custom-modal-overlay">
                      <div class="custom-modal-content shadow-lg">
                        <h4 class="border-bottom pb-2 mb-3">Attempt Overview</h4>

                        <div class="mb-3">
                          <p>
                            <strong>Quiz ID:</strong>
                            #{{ selectedAttemptOverview.quiz_id }}
                          </p>

                          <p>
                            <strong>User ID:</strong>
                            {{ selectedAttemptOverview.user_id }}
                          </p>

                          <p>
                            <strong>User Name:</strong>
                            {{ getUserName(selectedAttemptOverview.user_id) }}
                          </p>

                          <p>
                            <strong>Score:</strong>
                            {{ selectedAttemptOverview.score }}/{{ getTotalQuestions(selectedAttemptOverview.quiz_id) }}
                            ({{ getScorePercent(selectedAttemptOverview) }}%)
                          </p>
                        </div>

                        <button class="btn btn-dark w-100" @click="selectedAttemptOverview = null">
                          Close
                        </button>
                      </div>
                    </div>
                </td>
              </tr>

              <tr v-if="filteredAttempts.length === 0">
                <td colspan="5" class="text-muted py-3">
                  No attempts found.
                </td>
              </tr>
            </tbody>

          </table>
        </div>
      </div>
    </div>

    <!-- USER QUIZ LIST -->
    <div v-if="selectedUserProfile" class="custom-modal-overlay">
      <div class="custom-modal-content shadow-lg">
        <h4 class="border-bottom pb-2 mb-3">
          Quizzes Attended by {{ selectedUserProfile.full_name }}
        </h4>

        <div class="table-responsive" style="max-height:300px;">
          <table class="table table-sm">
            <thead>
              <tr>
                <th>Quiz ID</th>
                <th>Score</th>
                <th>Percentage</th>
              </tr>
            </thead>

            <tbody>
              <tr v-for="att in getUserAttempts(selectedUserProfile.id)" :key="att.id">
                <td>#{{ att.quiz_id }}</td>
                <td>{{ att.score }}/{{ getTotalQuestions(att.quiz_id) }}</td>
                <td>{{ getScorePercent(att) }}%</td>
              </tr>

              <tr v-if="getUserAttempts(selectedUserProfile.id).length === 0">
                <td colspan="3" class="text-center text-muted">
                  No quizzes attended.
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <button class="btn btn-dark w-100 mt-3" @click="selectedUserProfile = null">
          Close
        </button>
      </div>
    </div>

    <!-- ATTEMPT OVERVIEW -->
    <div v-if="selectedQuizSummary" class="custom-modal-overlay">
    <div class="custom-modal-content shadow-lg">
      <h4 class="border-bottom pb-2 mb-3">
        Quiz #{{ selectedQuizSummary.id }} Summary
      </h4>

      <div class="mb-3">
        <h6>Performance Stats:</h6>

        <p>
          <strong>Total Attempts:</strong>
          {{ getQuizStats(selectedQuizSummary.id).count }}
        </p>

        <p>
          <strong>Average Percentage:</strong>
          {{ getQuizStats(selectedQuizSummary.id).avg }}%
        </p>

        <hr>

        <h6>Attempts</h6>

        <ul class="list-group list-group-flush">
          <li
            v-for="att in attempts.filter(a => a.quiz_id === selectedQuizSummary.id)"
            :key="att.id"
            class="list-group-item small"
          >
            User: {{ getUserName(att.user_id) }}
            —
            Score:
            {{ att.score }}/{{ getTotalQuestions(att.quiz_id) }}
            ({{ getScorePercent(att) }}%)
          </li>

          <li
            v-if="attempts.filter(a => a.quiz_id === selectedQuizSummary.id).length === 0"
            class="list-group-item text-muted"
          >
            No attempts available
          </li>
        </ul>
      </div>

      <button
        class="btn btn-dark w-100"
        @click="selectedQuizSummary = null"
      >
        Close and Return
      </button>
    </div>
</div>

  </div>
</template>

<script>
export default {
  name: "AdminDashboard",

  data(){
    return{
      adminName: localStorage.getItem("username") || "Admin",
      quizzes:[],
      users:[],
      attempts:[],
      questions:{},
      quizSearch:"",
      userSearch:"",
      attemptSearch:"",
      selectedQuizSummary:null,
      selectedUserProfile:null,
      selectedAttemptOverview:null,
      baseURL:"http://localhost:5000/api"
    }
  },

  computed:{
    filteredQuizzes(){
      if(!Array.isArray(this.quizzes)) return [];
      return this.quizzes.filter(q => q.id?.toString().includes(this.quizSearch))
    },

    filteredUsers(){
      if(!Array.isArray(this.users)) return [];
      return this.users.filter(u =>
        (u.full_name || "").toLowerCase().includes(this.userSearch.toLowerCase())
      )
    },

    filteredAttempts(){
      if(!Array.isArray(this.attempts)) return [];
      return this.attempts.filter(a =>
        a.quiz_id?.toString().includes(this.attemptSearch)
      )
    }
  },

  async mounted(){

    const token = localStorage.getItem("access_token")
    if(!token) return this.$router.push("/login")

    const headers={
      "Authorization":`Bearer ${token}`,
      "Content-Type":"application/json"
    }

    try{

      const [qRes,uRes,aRes]=await Promise.all([
        fetch(`${this.baseURL}/quizzes`,{headers}),
        fetch(`${this.baseURL}/admin/users`,{headers}),
        fetch(`${this.baseURL}/scores`,{headers})
      ])

      if(qRes.ok){
        const data=await qRes.json()
        this.quizzes = data.quizzes || []
      }

      if(uRes.ok){
        const data=await uRes.json()
        this.users = data
      }

      if(aRes.ok){
        const data=await aRes.json()
        this.attempts = data.scores || []
      }

    }catch(err){
      console.error("Fetch Error:",err)
    }

  },

  methods:{

    viewQuizSummary(q){ this.selectedQuizSummary=q },

    viewUserQuizzes(user){ this.selectedUserProfile=user },

    viewAttemptOverview(a){ this.selectedAttemptOverview=a },

    getUserName(uid){
      const u=this.users.find(x=>x.id===uid)
      return u ? u.full_name : "Unknown"
    },

    getUserAttempts(uid){
      return this.attempts.filter(a=>a.user_id===uid)
    },

    getTotalQuestions(qid){
      const q=this.quizzes.find(x=>x.id===qid)
      return q?.questions?.length || 0
    },

    getScorePercent(att){
      const total=this.getTotalQuestions(att.quiz_id)
      if(!total) return 0
      return ((att.score/total)*100).toFixed(1)
    },

    getQuizStats(quizId){

      const quizAttempts=this.attempts.filter(a=>a.quiz_id===quizId)

      const percentages = quizAttempts.map(a => {
        const total=this.getTotalQuestions(a.quiz_id)
        return total ? (a.score/total)*100 : 0
      })

      const avg = percentages.length
        ? (percentages.reduce((a,b)=>a+b,0)/percentages.length).toFixed(1)
        : 0

      return {count:quizAttempts.length,avg,remarks:[]}
    },

    logout(){
      localStorage.clear()
      this.$router.push("/")
    }

  }
}
</script>

<style scoped>
.dashboard-bg { background-color: #f0f2f5; }
.action-card { border-radius: 15px; transition: transform 0.2s; border: none; }
.action-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
.custom-modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.7);
  display: flex; justify-content: center; align-items: center; z-index: 2000;
}
.custom-modal-content { background: white; padding: 2rem; border-radius: 12px; width: 90%; max-width: 500px; }
.table thead th { font-size: 0.85rem; text-transform: uppercase; color: #6c757d; }
</style>