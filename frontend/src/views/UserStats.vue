<template>

<div class="stats-page">

<!-- NAVBAR -->
<nav class="navbar navbar-dark bg-dark px-4 shadow">
<div class="d-flex align-items-center w-100">

<button class="btn btn-outline-light me-3"
@click="$router.push('/dashboard')">
Dashboard
</button>

<h5 class="text-white m-0 flex-grow-1 text-center">
User Performance Analytics
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
<h6>Total Quizzes</h6>
<h3>{{ scores.length }}</h3>
</div>
</div>

<div class="col-md-3">
<div class="summary-card bg-success text-white">
<h6>Average %</h6>
<h3>{{ averagePercentage }}</h3>
</div>
</div>

<div class="col-md-3">
<div class="summary-card bg-warning text-dark">
<h6>Highest %</h6>
<h3>{{ highestPercentage }}</h3>
</div>
</div>

<div class="col-md-3">
<div class="summary-card bg-danger text-white">
<h6>Lowest %</h6>
<h3>{{ lowestPercentage }}</h3>
</div>
</div>

</div>


<!-- CHARTS -->

<div class="row">

<!-- BAR CHART -->
<div class="col-md-6 mb-4">
<div class="card p-3 shadow-sm">
<h6 class="text-center fw-bold">Quiz-wise Performance</h6>
<canvas id="quizBarChart"></canvas>
</div>
</div>

<!-- LINE CHART -->
<div class="col-md-6 mb-4">
<div class="card p-3 shadow-sm">
<h6 class="text-center fw-bold">Performance Trend</h6>
<canvas id="trendChart"></canvas>
</div>
</div>

<!-- PIE CHART -->
<div class="col-md-6 mb-4">
<div class="card p-3 shadow-sm">
<h6 class="text-center fw-bold">Subject-wise Average</h6>
<canvas id="subjectPieChart"></canvas>
</div>
</div>

<!-- CHAPTER BAR -->
<div class="col-md-6 mb-4">
<div class="card p-3 shadow-sm">
<h6 class="text-center fw-bold">Chapter-wise Performance</h6>
<canvas id="chapterBarChart"></canvas>
</div>
</div>

</div>

</div>

</div>

</template>



<script>

import Chart from "chart.js/auto"

export default {

data(){

return{

scores:[],
quizzes:[],
subjects:[],
chapters:[],

baseURL:"http://localhost:5000/api",

/* EXTRA STATE */
charts:{},
debugMode:false

}

},

computed:{

averagePercentage(){

if(!this.scores.length) return 0

const total=this.scores.reduce((sum,s)=>sum+this.getPercentage(s),0)

return (total/this.scores.length).toFixed(2)

},

highestPercentage(){

if(!this.scores.length) return 0

return Math.max(...this.scores.map(s=>this.getPercentage(s)))

},

lowestPercentage(){

if(!this.scores.length) return 0

return Math.min(...this.scores.map(s=>this.getPercentage(s)))

}

},

methods:{

/* ---------------- CORE HELPERS ---------------- */

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

getPercentage(scoreObj){

const total = this.getTotalQuestions(scoreObj.quiz_id)

/* EXTRA SAFETY */
if(!total || total === 0){
return 0
}

/* CALCULATION */
let percent = (scoreObj.score / total) * 100

/* 🔥 IMPORTANT FIX: keep as NUMBER */
percent = Math.round(percent * 100) / 100

/* EXTRA DEBUG */
if(isNaN(percent)){
console.warn("Invalid percentage for:", scoreObj)
return 0
}

return percent

},


/* ---------------- DATA GROUPING ---------------- */

getSubjectStats(){

const map={}

this.scores.forEach(s=>{

const subject=this.getSubject(s.quiz_id)?.name || "Unknown"

if(!map[subject]) map[subject]=[]

map[subject].push(parseFloat(this.getPercentage(s)))

})

return Object.keys(map).map(k=>({
label:k,
value: map[k].reduce((a,b)=>a+b,0)/map[k].length
}))

},


getChapterStats(){

const map={}

this.scores.forEach(s=>{

const chapter=this.getChapter(s.quiz_id)?.name || "Unknown"

if(!map[chapter]) map[chapter]=[]

map[chapter].push(parseFloat(this.getPercentage(s)))

})

return Object.keys(map).map(k=>({
label:k,
value: map[k].reduce((a,b)=>a+b,0)/map[k].length
}))

},


/* ---------------- CHART RENDER ---------------- */

renderCharts(){

this.renderBarChart()
this.renderTrendChart()
this.renderPieChart()
this.renderChapterChart()

},


renderBarChart(){

const labels=this.scores.map(s=>"Quiz "+s.quiz_id)
const data=this.scores.map(s=>this.getPercentage(s))

this.charts.bar = new Chart(document.getElementById("quizBarChart"),{
type:"bar",
data:{
labels,
datasets:[{label:"%",data}]
}
})

},


renderTrendChart(){

const sorted=[...this.scores].sort((a,b)=>
new Date(a.attempted_at)-new Date(b.attempted_at)
)

const labels=sorted.map(s=>new Date(s.attempted_at).toLocaleDateString())
const data=sorted.map(s=>this.getPercentage(s))

this.charts.line = new Chart(document.getElementById("trendChart"),{
type:"line",
data:{labels,datasets:[{label:"Trend",data}]}
})

},


renderPieChart(){

const stats=this.getSubjectStats()

this.charts.pie = new Chart(document.getElementById("subjectPieChart"),{
type:"pie",
data:{
labels:stats.map(s=>s.label),
datasets:[{data:stats.map(s=>s.value)}]
}
})

},


renderChapterChart(){

const stats=this.getChapterStats()

this.charts.chapter = new Chart(document.getElementById("chapterBarChart"),{
type:"bar",
data:{
labels:stats.map(s=>s.label),
datasets:[{label:"%",data:stats.map(s=>s.value)}]
}
})

},


/* ---------------- FETCH ---------------- */

async fetchAll(){

const token=localStorage.getItem("access_token")

const headers={Authorization:`Bearer ${token}`}

const [s,q,c,sub]=await Promise.all([
fetch(`${this.baseURL}/scores`,{headers}),
fetch(`${this.baseURL}/quizzes`,{headers}),
fetch(`${this.baseURL}/chapters`,{headers}),
fetch(`${this.baseURL}/subjects`,{headers})
])

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

/* DELAY FOR DOM */
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