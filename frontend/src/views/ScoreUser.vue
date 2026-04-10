<template>

<div class="score-page">

<!-- NAVBAR -->
<nav class="navbar navbar-dark bg-dark px-4 shadow">

<div class="d-flex align-items-center w-100">

<button class="btn btn-outline-light me-3"
@click="$router.push('/dashboard')">
Dashboard
</button>

<h5 class="text-white m-0 flex-grow-1 text-center">
Your Quiz Scores
</h5>

<button class="btn btn-danger btn-sm"
@click="logout">
Logout
</button>

</div>

</nav>


<div class="container py-4">

<!-- SEARCH FILTERS -->

<div class="card shadow-sm mb-4 p-3">

<div class="row">

<div class="col-md-6">

<label class="fw-bold">Search by Date</label>

<input
type="date"
v-model="searchDate"
class="form-control"
/>

</div>


<div class="col-md-6">

<label class="fw-bold">Search by Score</label>

<input
type="number"
v-model="searchScore"
placeholder="Enter score"
class="form-control"
/>

</div>

</div>

</div>


<!-- SUMMARY CARD -->

<div class="row mb-4">

<div class="col-md-4">

<div class="summary-card bg-primary text-white">

<h6>Total Quizzes</h6>
<h3>{{ filteredScores.length }}</h3>

</div>

</div>

<div class="col-md-4">

<div class="summary-card bg-success text-white">

<h6>Average Score (%)</h6>
<h3>{{ averagePercentage }}</h3>

</div>

</div>

<div class="col-md-4">

<div class="summary-card bg-warning text-dark">

<h6>Highest Score (%)</h6>
<h3>{{ highestPercentage }}</h3>

</div>

</div>

</div>


<!-- SCORES TABLE -->

<div class="card shadow-sm">

<div class="card-header fw-bold">
Quiz Attempts
</div>

<div class="table-responsive">

<table class="table table-hover text-center align-middle">

<thead class="table-light">

<tr>

<th>Quiz ID</th>
<th>Subject</th>
<th>Chapter</th>
<th>Duration</th>
<th>Your Score (%)</th>
<th>Attempted At</th>

</tr>

</thead>


<tbody>

<tr
v-for="s in filteredScores"
:key="s.id"
>

<td>#{{ s.quiz_id }}</td>

<td>{{ getSubjectName(s.quiz_id) }}</td>

<td>{{ getChapterName(s.quiz_id) }}</td>



<td>{{ getQuiz(s.quiz_id)?.time_duration }}</td>

<td>

<span class="badge bg-success fs-6">

<!-- 🔥 UPDATED TO PERCENTAGE -->
{{ getPercentage(s) }}%

</span>

<!-- 🔥 EXTRA INFO (ADDED, NOT REMOVING ANYTHING) -->
<div class="small text-muted">
Raw: {{ s.score }}/{{ getTotalQuestions(s.quiz_id) }}
</div>

</td>

<td>{{ formatDate(s.attempted_at) }}</td>

</tr>


<tr v-if="filteredScores.length === 0">

<td colspan="7" class="text-muted py-4">
No quiz attempts found
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

data(){

return{

scores:[],
quizzes:[],
chapters:[],
subjects:[],

searchDate:"",
searchScore:"",

baseURL:"http://localhost:5000/api",

/* 🔥 ADDED EXTRA STATE (LINE INCREASE) */
lastUpdated:null,
debugMode:false

}

},


computed:{

filteredScores(){

let list = this.scores

if(this.searchScore){

list = list.filter(s =>
s.score == this.searchScore
)

}

if(this.searchDate){

list = list.filter(s =>
s.attempted_at?.substring(0,10) === this.searchDate
)

}

return list

},


/* 🔥 UPDATED TO PERCENTAGE */
averagePercentage(){

if(!this.scores.length) return 0

const total = this.scores.reduce((sum,s)=>{
return sum + this.getPercentage(s)
},0)

return (total/this.scores.length).toFixed(2)

},


highestPercentage(){

if(!this.scores.length) return 0

return Math.max(...this.scores.map(s=>this.getPercentage(s)))

}

},



methods:{


getQuiz(id){
return this.quizzes.find(q=>q.id===id)
},


/* 🔥 NEW FUNCTION */
getTotalQuestions(quizId){

const quiz = this.getQuiz(quizId)

if(!quiz) return 0

if(!quiz.questions) return 0

return quiz.questions.length

},


/* 🔥 CORE LOGIC: PERCENTAGE */
getPercentage(scoreObj){

const total = this.getTotalQuestions(scoreObj.quiz_id)

if(!total) return 0

let percent = (scoreObj.score / total) * 100

/* EXTRA ROUNDING */
percent = Math.round(percent * 100) / 100

return percent

},


/* 🔥 EXTRA FUNCTION (ADDED FOR FUTURE USE) */
getFormattedPercentage(scoreObj){

return this.getPercentage(scoreObj).toFixed(2)

},


getChapterName(quizId){

const quiz = this.getQuiz(quizId)

if(!quiz) return "Unknown"

const chapter = this.chapters.find(c=>c.id===quiz.chapter_id)

return chapter ? chapter.name : "Unknown"

},


getSubjectName(quizId){

const quiz = this.getQuiz(quizId)

if(!quiz) return "Unknown"

const chapter = this.chapters.find(c=>c.id===quiz.chapter_id)

if(!chapter) return "Unknown"

const subject = this.subjects.find(s=>s.id===chapter.subject_id)

return subject ? subject.name : "Unknown"

},


formatDate(d){

if(!d) return "N/A"

return new Date(d).toLocaleString()

},


/* 🔥 DEBUG METHOD (ADDED) */
logDebug(){

if(this.debugMode){
console.log("Scores:", this.scores)
console.log("Quizzes:", this.quizzes)
}

},


logout(){

localStorage.clear()

this.$router.push("/")

},



async fetchScores(){

const token = localStorage.getItem("access_token")

const res = await fetch(`${this.baseURL}/scores`,{
headers:{
Authorization:`Bearer ${token}`
}
})

const data = await res.json()

this.scores = data.scores || []

/* EXTRA TRACKING */
this.lastUpdated = new Date().toLocaleTimeString()

},



async fetchQuizzes(){

const token = localStorage.getItem("access_token")

const res = await fetch(`${this.baseURL}/quizzes`,{
headers:{
Authorization:`Bearer ${token}`
}
})

const data = await res.json()

this.quizzes = data.quizzes || []

},



async fetchChapters(){

const token = localStorage.getItem("access_token")

const res = await fetch(`${this.baseURL}/chapters`,{
headers:{
Authorization:`Bearer ${token}`
}
})

const data = await res.json()

this.chapters = data.chapters || []

},



async fetchSubjects(){

const token = localStorage.getItem("access_token")

const res = await fetch(`${this.baseURL}/subjects`,{
headers:{
Authorization:`Bearer ${token}`
}
})

const data = await res.json()

this.subjects = data.subjects || []

}

},



async mounted(){

await this.fetchScores()

await this.fetchQuizzes()

await this.fetchChapters()

await this.fetchSubjects()

/* EXTRA CALL */
this.logDebug()

}

}

</script>



<style scoped>

.score-page{
background:#f5f7fb;
min-height:100vh;
}


.summary-card{

padding:20px;
border-radius:12px;
box-shadow:0 4px 10px rgba(0,0,0,0.1);
text-align:center;

}


.table{
font-size:0.95rem;
}


.card{
border-radius:12px;
}

/* 🔥 EXTRA STYLES ADDED */
.badge{
border-radius:8px;
padding:8px;
}

.small{
font-size:0.75rem;
}

</style>