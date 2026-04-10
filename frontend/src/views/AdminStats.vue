<template>

<div class="stats-page">

<!-- NAVBAR -->
<nav class="navbar navbar-dark bg-dark px-4 shadow">
<div class="d-flex align-items-center w-100">

<button class="btn btn-outline-light me-3"
@click="$router.push('/admin/dashboard')">
Dashboard
</button>

<h5 class="text-white m-0 flex-grow-1 text-center">
Admin Analytics Dashboard
</h5>

<button class="btn btn-danger btn-sm"
@click="logout">
Logout
</button>

</div>
</nav>


<div class="container py-4">

<!-- SUMMARY CARDS -->
<div class="row mb-4">

<div class="col-md-3">
<div class="summary-card bg-primary text-white">
<h6>Total Users</h6>
<h3>{{ users.length }}</h3>
</div>
</div>

<div class="col-md-3">
<div class="summary-card bg-success text-white">
<h6>Total Quizzes</h6>
<h3>{{ quizzes.length }}</h3>
</div>
</div>

<div class="col-md-3">
<div class="summary-card bg-warning text-dark">
<h6>Total Attempts</h6>
<h3>{{ scores.length }}</h3>
</div>
</div>

<div class="col-md-3">
<div class="summary-card bg-danger text-white">
<h6>Avg Score (%)</h6>
<h3>{{ averagePercentage }}</h3>
</div>
</div>

</div>


<!-- CHARTS -->

<div class="row">

<!-- USERS PERFORMANCE -->
<div class="col-md-6 mb-4">
<div class="card p-3 shadow-sm">
<h6 class="fw-bold text-center">Top User Performance</h6>
<canvas id="userChart"></canvas>
</div>
</div>

<!-- QUIZ ATTEMPTS -->
<div class="col-md-6 mb-4">
<div class="card p-3 shadow-sm">
<h6 class="fw-bold text-center">Attempts per Quiz</h6>
<canvas id="quizChart"></canvas>
</div>
</div>

<!-- SUBJECT PERFORMANCE -->
<div class="col-md-6 mb-4">
<div class="card p-3 shadow-sm">
<h6 class="fw-bold text-center">Subject-wise Performance</h6>
<canvas id="subjectChart"></canvas>
</div>
</div>

<!-- TREND -->
<div class="col-md-6 mb-4">
<div class="card p-3 shadow-sm">
<h6 class="fw-bold text-center">Attempt Trend</h6>
<canvas id="trendChart"></canvas>
</div>
</div>

</div>

</div>

</div>

</template>



<script>

/* 🔥 SAFE IMPORT VERSION (LONGER, AS PER YOUR RULE) */
import {
Chart,
BarController,
BarElement,
CategoryScale,
LinearScale,
LineController,
LineElement,
PointElement,
PieController,
ArcElement
} from "chart.js"

Chart.register(
BarController,
BarElement,
CategoryScale,
LinearScale,
LineController,
LineElement,
PointElement,
PieController,
ArcElement
)

export default {

data(){

return{

users:[],
scores:[],
quizzes:[],
chapters:[],
subjects:[],

baseURL:"http://localhost:5000/api",

charts:{},
debugMode:false

}

},

computed:{

averagePercentage(){

if(!this.scores.length) return 0

const vals=this.scores.map(s=>this.getPercentage(s)).filter(v=>!isNaN(v))

if(!vals.length) return 0

const total=vals.reduce((a,b)=>a+b,0)

return (total/vals.length).toFixed(2)

}

},

methods:{

/* ---------------- HELPERS ---------------- */

getQuiz(id){
return this.quizzes.find(q=>q.id===id)
},

getChapter(quizId){
const quiz=this.getQuiz(quizId)
return this.chapters.find(c=>c.id===quiz?.chapter_id)
},

getSubject(quizId){
const chapter=this.getChapter(quizId)
return this.subjects.find(s=>s.id===chapter?.subject_id)
},

getTotalQuestions(quizId){
const quiz=this.getQuiz(quizId)
return quiz?.questions?.length || 0
},

getPercentage(s){
const total=this.getTotalQuestions(s.quiz_id)
if(!total) return 0
return (s.score/total)*100
},

/* ---------------- USER STATS ---------------- */

getUserStats(){

const map={}

this.scores.forEach(s=>{
if(!map[s.user_id]) map[s.user_id]=[]
map[s.user_id].push(this.getPercentage(s))
})

return Object.keys(map).map(uid=>{

const user=this.users.find(u=>u.id==uid)

const avg=map[uid].reduce((a,b)=>a+b,0)/map[uid].length

return{
name:user?.full_name || "User "+uid,
value:avg
}

}).sort((a,b)=>b.value-a.value).slice(0,5)

},

/* ---------------- QUIZ STATS ---------------- */

getQuizStats(){

const map={}

this.scores.forEach(s=>{
if(!map[s.quiz_id]) map[s.quiz_id]=0
map[s.quiz_id]++
})

return Object.keys(map).map(q=>({
label:"Quiz "+q,
value:map[q]
}))

},

/* ---------------- SUBJECT STATS ---------------- */

getSubjectStats(){

const map={}

this.scores.forEach(s=>{

const subject=this.getSubject(s.quiz_id)?.name || "Unknown"

if(!map[subject]) map[subject]=[]

map[subject].push(this.getPercentage(s))

})

return Object.keys(map).map(k=>({
label:k,
value: map[k].reduce((a,b)=>a+b,0)/map[k].length
}))

},

/* ---------------- TREND ---------------- */

getTrend(){

const sorted=[...this.scores].sort((a,b)=>
new Date(a.attempted_at)-new Date(b.attempted_at)
)

return{
labels:sorted.map(s=>new Date(s.attempted_at).toLocaleDateString()),
values:sorted.map(s=>this.getPercentage(s))
}

},

/* ---------------- CHARTS ---------------- */

renderCharts(){

this.renderUserChart()
this.renderQuizChart()
this.renderSubjectChart()
this.renderTrendChart()

},

renderUserChart(){

const data=this.getUserStats()

/* 🔥 ADD COLORS */
const bgColors=[
"#4e73df","#1cc88a","#36b9cc","#f6c23e","#e74a3b","#858796"
]

this.charts.user=new Chart(document.getElementById("userChart"),{
type:"bar",
data:{
labels:data.map(d=>d.name),
datasets:[{
label:"Avg %",
data:data.map(d=>d.value),
backgroundColor:bgColors,
borderColor:bgColors,
borderWidth:1
}]
}
})

},

renderQuizChart(){

const data=this.getQuizStats()

const bgColors=[
"#ff6384","#36a2eb","#ffce56","#4bc0c0","#9966ff","#ff9f40"
]

this.charts.quiz=new Chart(document.getElementById("quizChart"),{
type:"bar",
data:{
labels:data.map(d=>d.label),
datasets:[{
label:"Attempts",
data:data.map(d=>d.value),
backgroundColor:bgColors,
borderColor:bgColors,
borderWidth:1
}]
}
})

},

renderSubjectChart(){

const data=this.getSubjectStats()

const bgColors=[
"#ff6384","#36a2eb","#ffce56","#4bc0c0","#9966ff","#ff9f40"
]

this.charts.subject=new Chart(document.getElementById("subjectChart"),{
type:"pie",
data:{
labels:data.map(d=>d.label),
datasets:[{
data:data.map(d=>d.value),
backgroundColor:bgColors
}]
}
})

},

renderTrendChart(){

const t=this.getTrend()

this.charts.trend=new Chart(document.getElementById("trendChart"),{
type:"line",
data:{
labels:t.labels,
datasets:[{
label:"Performance",
data:t.values,

/* 🔥 ADD COLORS */
borderColor:"#4e73df",
backgroundColor:"rgba(78,115,223,0.2)",
fill:true,
tension:0.3
}]
}
})

},

/* ---------------- FETCH ---------------- */

async fetchAll(){

const token=localStorage.getItem("access_token")

const headers={Authorization:`Bearer ${token}`}

const [u,s,q,c,sub]=await Promise.all([
fetch(`${this.baseURL}/admin/users`,{headers}),
fetch(`${this.baseURL}/scores`,{headers}),
fetch(`${this.baseURL}/quizzes`,{headers}),
fetch(`${this.baseURL}/chapters`,{headers}),
fetch(`${this.baseURL}/subjects`,{headers})
])

this.users=await u.json()
this.scores=(await s.json()).scores || []
this.quizzes=(await q.json()).quizzes || []
this.chapters=(await c.json()).chapters || []
this.subjects=(await sub.json()).subjects || []

},

logout(){
localStorage.clear()
this.$router.push("/")
}

},

async mounted(){

await this.fetchAll()

setTimeout(()=>{
this.renderCharts()
},300)

}

}

</script>



<style scoped>

.stats-page{
background:#f5f7fb;
min-height:100vh;
}

.summary-card{
padding:20px;
border-radius:12px;
text-align:center;
box-shadow:0 4px 10px rgba(0,0,0,0.1);
}

.card{
border-radius:12px;
}

</style>