<template>

<div class="quiz-page">

<!-- NAVBAR -->
<nav class="navbar navbar-dark bg-dark px-4 shadow">
<div class="d-flex align-items-center w-100">

<button class="btn btn-outline-light me-4" @click="$router.push('/admin/dashboard')">Admin Dashboard</button>
 
<button class="btn btn-outline-light me-2" @click="$router.push('/admin/subjects')">Subjects</button>
<button class="btn btn-outline-light me-2" @click="$router.push('/admin/chapters')">Chapters</button>

<h4 class="text-white fw-bold flex-grow-1 text-center m-0">Quizzes</h4>

<input v-model="quizSearch" class="form-control w-25 me-3" placeholder="Search quiz"/>

<button class="btn btn-danger" @click="logout">Logout</button>

</div>
</nav>


<div class="container py-4">

<div class="row g-4">

<div class="col-lg-4" v-for="quiz in filteredQuizzes" :key="quiz.id">

<div class="quiz-card">

<div class="quiz-header">

<h5 class="fw-bold">Quiz #{{ quiz.id }}</h5>

<div class="d-flex gap-2">

<button class="btn btn-sm btn-outline-primary" @click="openEditQuiz(quiz)">
Edit
</button>

<button class="btn btn-sm btn-outline-danger" @click="deleteQuiz(quiz.id)">
Delete
</button>

</div>

</div>

<p class="small text-muted">
Subject: {{ getSubjectNameByChapter(quiz.chapter_id) }}
</p>

<p class="small text-muted">
Chapter: {{ getChapterName(quiz.chapter_id) }}
</p>

<p><strong>Date:</strong> {{ quiz.date_of_quiz }}</p>
<p><strong>Duration:</strong> {{ quiz.time_duration }}</p>


<div class="question-list">

<div class="question-item" v-for="q in getQuestions(quiz.id)" :key="q.id">

<div class="small">{{ q.question_statement }}</div>

<div class="d-flex gap-1">

<button class="btn btn-sm btn-outline-primary" @click="openEditQuestion(q)">
Edit
</button>

<button class="btn btn-sm btn-outline-danger" @click="deleteQuestion(q.id)">
Delete
</button>

</div>

</div>

</div>


<div class="text-center mt-3">

<button class="btn btn-success btn-sm" @click="openAddQuestion(quiz)">
+ Question
</button>

</div>

</div>

</div>

</div>

</div>


<!-- ADD QUIZ BUTTON -->
<div class="add-btn">
<button class="btn btn-warning add-circle" @click="showQuizModal=true">+</button>
</div>


<!-- CREATE QUIZ -->
<div v-if="showQuizModal" class="modal-overlay">

<div class="custom-modal">

<h4>Create Quiz</h4>

<select v-model="selectedSubject" class="form-control mb-3">
<option disabled value="">Select Subject</option>
<option v-for="s in subjects" :key="s.id" :value="s.id">{{ s.name }}</option>
</select>

<select v-if="selectedSubject" v-model="newQuiz.chapter_id" class="form-control mb-3">
<option disabled value="">Select Chapter</option>
<option v-for="c in filteredChapters" :key="c.id" :value="c.id">{{ c.name }}</option>
</select>

<input type="datetime-local" v-model="newQuiz.date_of_quiz" class="form-control mb-2"/>
<input v-model="newQuiz.time_duration" class="form-control mb-2" placeholder="Duration HH:MM"/>
<textarea v-model="newQuiz.remarks" class="form-control mb-3" placeholder="Remarks"/>

<div class="d-flex justify-content-end gap-2">

<button class="btn btn-secondary" @click="closeQuizModal">Cancel</button>

<button class="btn btn-success" @click="createQuiz">Save</button>

</div>

</div>

</div>


<!-- EDIT QUIZ -->
<div v-if="editQuiz" class="modal-overlay">

<div class="custom-modal">

<h4>Edit Quiz</h4>

<input type="datetime-local" v-model="editQuiz.date_of_quiz" class="form-control mb-2"/>

<input v-model="editQuiz.time_duration" class="form-control mb-2"/>

<textarea v-model="editQuiz.remarks" class="form-control mb-3"/>

<div class="d-flex justify-content-end gap-2">

<button class="btn btn-secondary" @click="editQuiz=null">Cancel</button>

<button class="btn btn-success" @click="updateQuiz">Save</button>

</div>

</div>

</div>


<!-- ADD / EDIT QUESTION -->
<div v-if="addQuestionQuiz || editQuestionData" class="modal-overlay">

<div class="custom-modal">

<h4>{{ editQuestionData ? "Edit Question" : "Add Question" }}</h4>

<textarea v-model="newQuestion.question_statement" class="form-control mb-3" placeholder="Question"/>

<div class="option-row">
<span class="option-number">1</span>
<input v-model="newQuestion.option1" class="form-control" placeholder="Option 1"/>
</div>

<div class="option-row">
<span class="option-number">2</span>
<input v-model="newQuestion.option2" class="form-control" placeholder="Option 2"/>
</div>

<div class="option-row">
<span class="option-number">3</span>
<input v-model="newQuestion.option3" class="form-control" placeholder="Option 3"/>
</div>

<div class="option-row">
<span class="option-number">4</span>
<input v-model="newQuestion.option4" class="form-control" placeholder="Option 4"/>
</div>

<select v-model="newQuestion.correct_option" class="form-control mt-3">
<option value="1">Correct Option 1</option>
<option value="2">Correct Option 2</option>
<option value="3">Correct Option 3</option>
<option value="4">Correct Option 4</option>
</select>

<div class="d-flex justify-content-end gap-2 mt-3">

<button class="btn btn-secondary" @click="closeQuestionModal">Cancel</button>

<button class="btn btn-success" @click="saveQuestion">
Save
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

quizzes:[],
chapters:[],
subjects:[],
questions:[],

quizSearch:"",

selectedSubject:"",

showQuizModal:false,
editQuiz:null,

addQuestionQuiz:null,
editQuestionData:null,

newQuiz:{
chapter_id:"",
date_of_quiz:"",
time_duration:"",
remarks:""
},

newQuestion:{
question_statement:"",
option1:"",
option2:"",
option3:"",
option4:"",
correct_option:1
},

baseURL:"http://localhost:5000/api"

}

},

computed:{

filteredQuizzes(){
if(!this.quizSearch) return this.quizzes
return this.quizzes.filter(q=>q.id.toString().includes(this.quizSearch))
},

filteredChapters(){
return this.chapters.filter(c=>c.subject_id===this.selectedSubject)
}

},

methods:{


getChapterName(id){
const c=this.chapters.find(c=>c.id===id)
return c?c.name:"Unknown"
},

getSubjectNameByChapter(chapterId){
const chapter=this.chapters.find(c=>c.id===chapterId)
if(!chapter) return "Unknown"
const subject=this.subjects.find(s=>s.id===chapter.subject_id)
return subject?subject.name:"Unknown"
},

getQuestions(quizId){
return this.questions.filter(q=>q.quiz_id===quizId)
},

openEditQuiz(quiz){

const d = new Date(quiz.date_of_quiz)

this.editQuiz={
id:quiz.id,
date_of_quiz:d.toISOString().slice(0,16),
time_duration:quiz.time_duration,
remarks:quiz.remarks || ""
}

},

openEditQuestion(q){

this.editQuestionData=q

this.newQuestion={
question_statement:q.question_statement,
option1:q.options["1"],
option2:q.options["2"],
option3:q.options["3"],
option4:q.options["4"],
correct_option:Number(q.correct_option)
}

},

openAddQuestion(quiz){
this.addQuestionQuiz=quiz
},

closeQuestionModal(){
this.addQuestionQuiz=null
this.editQuestionData=null
this.resetQuestionForm()
},

closeQuizModal(){
this.showQuizModal=false
this.selectedSubject=""
this.newQuiz={
chapter_id:"",
date_of_quiz:"",
time_duration:"",
remarks:""
}
},

resetQuestionForm(){
this.newQuestion={
question_statement:"",
option1:"",
option2:"",
option3:"",
option4:"",
correct_option:1
}
},

async createQuiz(){

const token=localStorage.getItem("access_token")

const res=await fetch(`${this.baseURL}/quizzes`,{

method:"POST",

headers:{
"Content-Type":"application/json",
Authorization:`Bearer ${token}`
},

body:JSON.stringify({
chapter_id:this.newQuiz.chapter_id,
date_of_quiz:new Date(this.newQuiz.date_of_quiz).toISOString(),
time_duration:this.newQuiz.time_duration,
remarks:this.newQuiz.remarks
})

})

if(res.ok){
this.closeQuizModal()
await this.fetchQuizzes()
}

},

async updateQuiz(){

const token = localStorage.getItem("access_token")

try{

const res = await fetch(`${this.baseURL}/quizzes/${this.editQuiz.id}`,{

method:"PATCH",

headers:{
"Content-Type":"application/json",
Authorization:`Bearer ${token}`
},

body:JSON.stringify({
date_of_quiz:new Date(this.editQuiz.date_of_quiz).toISOString(),
time_duration:this.editQuiz.time_duration,
remarks:this.editQuiz.remarks
})

})

if(!res.ok){

const data = await res.json()
alert(data.message || "Quiz update failed")
return

}

this.editQuiz=null

await this.fetchQuizzes()

}catch(err){

console.error("Quiz update error:",err)

}

},

async deleteQuiz(id){

if(!confirm("Delete this quiz?")) return

const token=localStorage.getItem("access_token")

const res = await fetch(`${this.baseURL}/quizzes/${id}`,{
method:"DELETE",
headers:{Authorization:`Bearer ${token}`}
})

if(res.ok){
await this.fetchQuizzes()
await this.fetchQuestions()
}

},

async saveQuestion(){

const token=localStorage.getItem("access_token")

const payload={
quiz_id: this.addQuestionQuiz ? this.addQuestionQuiz.id : this.editQuestionData.quiz_id,
question_statement:this.newQuestion.question_statement,
options:{
"1":this.newQuestion.option1,
"2":this.newQuestion.option2,
"3":this.newQuestion.option3,
"4":this.newQuestion.option4
},
correct_option:Number(this.newQuestion.correct_option)
}

if(this.editQuestionData){

await fetch(`${this.baseURL}/questions/${this.editQuestionData.id}`,{
method:"PATCH",
headers:{
"Content-Type":"application/json",
Authorization:`Bearer ${token}`
},
body:JSON.stringify(payload)
})

}else{

await fetch(`${this.baseURL}/questions`,{
method:"POST",
headers:{
"Content-Type":"application/json",
Authorization:`Bearer ${token}`
},
body:JSON.stringify(payload)
})

}

await this.fetchQuestions()
this.closeQuestionModal()

},

async deleteQuestion(id){

if(!confirm("Delete question?")) return

const token=localStorage.getItem("access_token")

await fetch(`${this.baseURL}/questions/${id}`,{
method:"DELETE",
headers:{Authorization:`Bearer ${token}`}
})

await this.fetchQuestions()

},

async fetchQuizzes(){
const token=localStorage.getItem("access_token")
const res=await fetch(`${this.baseURL}/quizzes`,{headers:{Authorization:`Bearer ${token}`}})
const data=await res.json()
this.quizzes=data.quizzes||[]
},

async fetchQuestions(){
const token=localStorage.getItem("access_token")
const res=await fetch(`${this.baseURL}/questions`,{headers:{Authorization:`Bearer ${token}`}})
const data=await res.json()
this.questions=data.questions||[]
},

async fetchChapters(){
const token=localStorage.getItem("access_token")
const res=await fetch(`${this.baseURL}/chapters`,{headers:{Authorization:`Bearer ${token}`}})
const data=await res.json()
this.chapters=data.chapters||[]
},

async fetchSubjects(){
const token=localStorage.getItem("access_token")
const res=await fetch(`${this.baseURL}/subjects`,{headers:{Authorization:`Bearer ${token}`}})
const data=await res.json()
this.subjects=data.subjects||[]
},

logout(){
localStorage.clear()
this.$router.push("/")
}

},

async mounted(){

await this.fetchSubjects()
await this.fetchChapters()
await this.fetchQuizzes()
await this.fetchQuestions()

}

}

</script>


<style scoped>

.quiz-page{
background:#f5f7fb;
min-height:100vh;
}

.quiz-card{
background:white;
border-radius:14px;
padding:18px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
}

.quiz-header{
display:flex;
justify-content:space-between;
align-items:center;
}

.question-list{
max-height:200px;
overflow:auto;
margin-top:10px;
}

.question-item{
display:flex;
justify-content:space-between;
border-bottom:1px solid #eee;
padding:6px;
}

.option-row{
display:flex;
align-items:center;
gap:10px;
margin-bottom:8px;
}

.option-number{
width:25px;
text-align:center;
font-weight:bold;
}

.add-btn{
position:fixed;
bottom:30px;
left:50%;
transform:translateX(-50%);
}

.add-circle{
width:80px;
height:80px;
font-size:36px;
border-radius:50%;
}

.modal-overlay{
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:rgba(0,0,0,0.5);
display:flex;
justify-content:center;
align-items:center;
}

.custom-modal{
background:white;
padding:25px;
border-radius:12px;
width:420px;
}

</style>
