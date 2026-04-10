<template>

<div class="dashboard-page">

<!-- NAVBAR -->
<nav class="navbar navbar-dark bg-dark px-4 shadow">
<div class="d-flex align-items-center w-100">

<div class="text-white fw-bold fs-5">
Welcome {{ user.full_name || "User" }}
<span class="ms-2 text-light">| User Dashboard</span>
</div>

<div class="ms-auto d-flex gap-3">

<button class="btn btn-outline-light btn-sm" @click="$router.push('/scores')">
Scores
</button>

<button class="btn btn-outline-light btn-sm" @click="$router.push('/user/stats')">
Stats
</button>

<button class="btn btn-success btn-sm" @click="downloadCSV">
📄 Download Score Card
</button>

<!-- ✅ PROFILE BUTTON ADDED -->
<button class="btn btn-outline-info btn-sm" @click="openProfile">
👤 Profile
</button>

<button class="btn btn-danger btn-sm" @click="logout">
Logout
</button>

</div>
</div>
</nav>

<div class="container py-4">

<h4 class="fw-bold mb-3">🆕 Available Quizzes</h4>

<div class="slider-container">
<div class="slider-track">

<div v-for="quiz in unattemptedQuizzes" :key="quiz.id" class="quiz-slide-card">

<h6>Quiz #{{ quiz.id }}</h6>

<p class="small text-muted">
{{ getSubjectName(quiz.chapter_id) }} / {{ getChapterName(quiz.chapter_id) }}
</p>

<button class="btn btn-primary btn-sm w-100"
@click="startQuiz(quiz)">
Start
</button>

</div>

</div>
</div>

<h4 class="fw-bold mt-5 mb-3">📊 Attempted Quizzes</h4>

<div class="card shadow-sm">
<div class="table-responsive">

<table class="table text-center">

<thead>
<tr>
<th>Quiz</th>
<th>Subject</th>
<th>Chapter</th>
<th>Score</th>
<th>%</th>
<th>Date</th>
<th>Action</th>
</tr>
</thead>

<tbody>

<tr v-for="att in scores" :key="att.id">

<td>#{{ att.quiz_id }}</td>
<td>{{ getSubjectNameByQuiz(att.quiz_id) }}</td>
<td>{{ getChapterNameByQuiz(att.quiz_id) }}</td>
<td>{{ att.score }}/{{ getTotalQuestions(att.quiz_id) }}</td>
<td>{{ getPercentage(att) }}%</td>
<td>{{ formatDate(att.attempted_at) }}</td>
<td>
  <button 
    class="btn btn-warning btn-sm"
    @click="reattemptQuiz(att.quiz_id)"
  >
    Reattempt
  </button>
</td>

</tr>

</tbody>

</table>

</div>
</div>

<div class="row mt-4">

<div class="col-md-4">

<label class="fw-bold">Select Subject</label>

<select v-model="selectedSubject" class="form-control">

<option value="">All Subjects</option>

<option v-for="s in subjects" :key="s.id" :value="s.id">
{{ s.name }}
</option>

</select>

</div>

<div class="col-md-4" v-if="selectedSubject">

<label class="fw-bold">Select Chapter</label>

<select v-model="selectedChapter" class="form-control">

<option value="">All Chapters</option>

<option v-for="c in filteredChapters" :key="c.id" :value="c.id">
{{ c.name }}
</option>

</select>

</div>

</div>

<h4 class="fw-bold mt-4 mb-3">📚 All Quizzes</h4>

<div class="slider-container">
<div class="slider-track">

<div v-for="quiz in filteredAllQuizzes" :key="quiz.id" class="quiz-slide-card">

<h6>Quiz #{{ quiz.id }}</h6>

<p class="small text-muted">
{{ getSubjectName(quiz.chapter_id) }} / {{ getChapterName(quiz.chapter_id) }}
</p>

<button class="btn btn-success btn-sm w-100"
@click="startQuiz(quiz)">
Start
</button>

</div>

</div>
</div>

</div>

<!-- ✅ PROFILE VIEW MODAL -->
<div v-if="showProfile" class="modal-overlay">
  <div class="modal-box">

    <h4>User Profile</h4>

    <p><strong>Name:</strong> {{ user.full_name }}</p>
    <p><strong>Email:</strong> {{ user.email }}</p>
    <p><strong>Qualification:</strong> {{ user.qualification }}</p>
    <p><strong>DOB:</strong> {{ user.dob }}</p>

    <div class="d-flex gap-2 mt-3">

      <button class="btn btn-primary" @click="openEditProfile">
        Edit
      </button>

      <button class="btn btn-secondary" @click="showProfile=false">
        Close
      </button>

    </div>

  </div>
</div>

<!-- ✅ EDIT PROFILE MODAL -->
<div v-if="editProfileModal" class="modal-overlay">
  <div class="modal-box">

    <h4>Edit Profile</h4>

    <input v-model="editProfile.full_name" class="form-control mb-2" placeholder="Full Name"/>

    <input v-model="editProfile.qualification" class="form-control mb-2" placeholder="Qualification"/>

    <input v-model="editProfile.dob" type="date" class="form-control mb-2"/>

    <div class="d-flex gap-2 mt-3">

      <button class="btn btn-success" @click="updateProfile">
        Save
      </button>

      <button class="btn btn-secondary" @click="editProfileModal=false">
        Cancel
      </button>

    </div>

  </div>
</div>

</div>
</template>

<script>

export default{

data(){
return{

user:{},
subjects:[],
chapters:[],
quizzes:[],
scores:[],

selectedSubject:"",
selectedChapter:"",

// ✅ PROFILE STATES
showProfile:false,
editProfileModal:false,
editProfile:{},

baseURL:"http://localhost:5000/api"

}
},

computed:{
attemptedIds(){
return this.scores.map(s=>s.quiz_id)
},
unattemptedQuizzes(){
return this.quizzes.filter(q=>!this.attemptedIds.includes(q.id))
},
filteredChapters(){
return this.chapters.filter(c=>c.subject_id==this.selectedSubject)
},
filteredAllQuizzes(){

let list = this.quizzes

if(this.selectedSubject){
const chapterIds = this.filteredChapters.map(c=>c.id)
list = list.filter(q=>chapterIds.includes(q.chapter_id))
}

if(this.selectedChapter){
list = list.filter(q=>q.chapter_id==this.selectedChapter)
}

return list

}
},

methods:{

// ✅ PROFILE METHODS
openProfile(){
this.fetchUser()
this.showProfile = true
},

openEditProfile(){

this.editProfile = {...this.user}

// convert ISO → YYYY-MM-DD
if(this.editProfile.dob){
this.editProfile.dob = this.editProfile.dob.split("T")[0]
}

this.editProfileModal = true
},

async updateProfile(){

const token = localStorage.getItem("access_token")

try{

const res = await fetch(`${this.baseURL}/editprofile`,{
method:"PATCH",
headers:{
"Content-Type":"application/json",
Authorization:`Bearer ${token}`
},
body:JSON.stringify({
full_name:this.editProfile.full_name,
qualification:this.editProfile.qualification,
dob:this.editProfile.dob
})
})

const data = await res.json()

if(!res.ok){
alert(data.message || "Update failed")
return
}

this.user = data.user
localStorage.setItem("user", JSON.stringify(this.user))

this.editProfileModal=false
this.showProfile=false

}catch(err){
console.error("Profile update error:",err)
}

},

// EXISTING METHODS (UNCHANGED)
getChapterName(id){
const c=this.chapters.find(c=>c.id==id)
return c?c.name:"Unknown"
},

getChapterNameByQuiz(id){
const q=this.quizzes.find(q=>q.id==id)
return q?this.getChapterName(q.chapter_id):"Unknown"
},

reattemptQuiz(quizId){
if(!quizId) return
this.$router.push({ name: "exam", params: { quiz_id: quizId } })
},

getSubjectName(chapterId){
const chapter=this.chapters.find(c=>c.id==chapterId)
if(!chapter) return "Unknown"
const subject=this.subjects.find(s=>s.id==chapter.subject_id)
return subject?subject.name:"Unknown"
},

getSubjectNameByQuiz(id){
const q=this.quizzes.find(q=>q.id==id)
return q?this.getSubjectName(q.chapter_id):"Unknown"
},

getTotalQuestions(qid){
const q=this.quizzes.find(q=>q.id==qid)
return q?.questions?.length || 0
},

getPercentage(att){
const total=this.getTotalQuestions(att.quiz_id)
return total ? ((att.score/total)*100).toFixed(1) : 0
},

formatDate(d){
return new Date(d).toLocaleString()
},

startQuiz(q){
this.$router.push(`/exam/${q.id}`)
},

logout(){
localStorage.clear()
this.$router.push("/")
},

async downloadCSV(){
const token = localStorage.getItem("access_token")
await fetch(`${this.baseURL}/export/csv`,{
method:"POST",
headers:{Authorization:`Bearer ${token}`}
})
alert("CSV will be sent to your email")
},

async fetchUser(){
const stored = localStorage.getItem("user")
if(stored){
this.user = JSON.parse(stored)
}
},

async fetchAll(){

const token=localStorage.getItem("access_token")
const headers={Authorization:`Bearer ${token}`}

const [s,c,q,sc] = await Promise.all([
fetch(`${this.baseURL}/subjects`,{headers}),
fetch(`${this.baseURL}/chapters`,{headers}),
fetch(`${this.baseURL}/quizzes`,{headers}),
fetch(`${this.baseURL}/scores`,{headers})
])

this.subjects=(await s.json()).subjects||[]
this.chapters=(await c.json()).chapters||[]
this.quizzes=(await q.json()).quizzes||[]
this.scores=(await sc.json()).scores||[]

}

},

mounted(){
this.fetchUser()
this.fetchAll()
}

}

</script>

<style scoped>

.dashboard-page{
background:#f4f6fb;
min-height:100vh;
}

.slider-container{
overflow-x:auto;
}
.slider-track{
display:flex;
gap:15px;
}
.quiz-slide-card{
min-width:200px;
background:white;
border-radius:12px;
padding:15px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
transition:0.2s;
}
.quiz-slide-card:hover{
transform:scale(1.05);
}

.modal-overlay{
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:rgba(0,0,0,0.6);
display:flex;
align-items:center;
justify-content:center;
z-index:2000;
}

.modal-box{
background:white;
padding:25px;
width:400px;
border-radius:10px;
}

</style>