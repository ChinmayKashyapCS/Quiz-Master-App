<template>

<div class="chapter-page">

<!-- NAVBAR -->
<nav class="navbar navbar-dark bg-dark px-4 shadow">
<div class="d-flex align-items-center w-100">

<button class="btn btn-outline-light me-4" @click="$router.push('/admin/dashboard')">
Admin Dashboard
</button>

<button class="btn btn-outline-light me-2" @click="$router.push('/admin/subjects')">
Subjects
</button>

<button class="btn btn-outline-light me-2" @click="$router.push('/admin/quizzes')">
Quizzes
</button>



<h4 class="text-white fw-bold flex-grow-1 text-center m-0">
Chapters
</h4>

<input v-model="chapterSearch" class="form-control w-25 me-3" placeholder="Search chapter"/>

<button class="btn btn-danger" @click="logout">
Logout
</button>

</div>
</nav>


<!-- BODY -->
<div class="container py-4">

<div class="row g-4">

<div class="col-lg-4" v-for="chapter in filteredChapters" :key="chapter.id">

<div class="chapter-card">

<!-- HEADER -->
<div class="chapter-header">

<div>
<div class="subject-label">
{{ getSubjectName(chapter.subject_id) }}
</div>

<h5 class="fw-bold m-0">
{{ chapter.name }}
<span class="quiz-count">
({{ getQuizzes(chapter.id).length }})
</span>
</h5>
</div>

<div class="d-flex gap-2">

<button class="btn btn-sm btn-outline-primary" @click="openEditChapter(chapter)">
Edit
</button>

<button class="btn btn-sm btn-outline-danger" @click="deleteChapter(chapter.id)">
Delete
</button>

</div>

</div>


<!-- SEARCH QUIZ -->
<input
v-model="quizSearch[chapter.id]"
class="form-control form-control-sm my-2"
placeholder="Search quiz..."
/>


<!-- QUIZ LIST -->
<div class="quiz-list">

<div
class="quiz-item"
v-for="quiz in filteredQuizzes(chapter)"
:key="quiz.id"
>

<div>
Quiz #{{ quiz.id }}
</div>

<button
class="btn btn-sm btn-outline-secondary"
@click="openQuizOverview(quiz)"
>
Overview
</button>

</div>

</div>


<!-- ADD QUIZ -->
<div class="text-center mt-3">

<button
class="btn btn-success btn-sm"
@click="openAddQuiz(chapter)"
>
+ Quiz
</button>

</div>

</div>

</div>

</div>

</div>


<!-- ADD CHAPTER BUTTON -->
<div class="add-btn">

<button class="btn btn-warning add-circle" @click="showAddModal=true">
+
</button>

</div>


<!-- ADD CHAPTER MODAL -->
<div v-if="showAddModal" class="modal-overlay">

<div class="custom-modal">

<h4>Add Chapter</h4>

<select v-model="newChapter.subject_id" class="form-control mb-3">

<option disabled value="">Select Subject</option>

<option v-for="subject in subjects" :key="subject.id" :value="subject.id">
{{ subject.name }}
</option>

</select>

<input v-model="newChapter.name" class="form-control mb-2" placeholder="Chapter Name"/>

<textarea v-model="newChapter.description" class="form-control mb-2" placeholder="Description"/>

<input v-model="newChapter.difficulty" type="number" class="form-control mb-3" placeholder="Difficulty"/>

<div class="d-flex justify-content-end gap-2">

<button class="btn btn-secondary" @click="showAddModal=false">
Cancel
</button>

<button class="btn btn-primary" @click="createChapter">
Save
</button>

</div>

</div>

</div>


<!-- EDIT CHAPTER MODAL -->
<div v-if="editChapter" class="modal-overlay">

<div class="custom-modal">

<h4>Edit Chapter</h4>

<input v-model="editChapter.name" class="form-control mb-2"/>

<textarea v-model="editChapter.description" class="form-control mb-2"></textarea>

<input v-model="editChapter.difficulty" type="number" class="form-control mb-3"/>

<div class="d-flex justify-content-end gap-2">

<button class="btn btn-secondary" @click="editChapter=null">
Close
</button>

<button class="btn btn-success" @click="updateChapter">
Save
</button>

</div>

</div>

</div>


<!-- ADD QUIZ MODAL -->
<div v-if="addQuizChapter" class="modal-overlay">

<div class="custom-modal">

<h4 class="mb-3 text-center">Create Quiz</h4>

<label class="form-label">Quiz Date & Time</label>
<input
v-model="newQuiz.date_of_quiz"
type="datetime-local"
class="form-control mb-3"
/>

<label class="form-label">Time Duration (HH:MM)</label>
<input
v-model="newQuiz.time_duration"
class="form-control mb-3"
placeholder="Example: 00:30"
/>

<label class="form-label">Description</label>
<textarea
v-model="newQuiz.remarks"
class="form-control mb-3"
placeholder="Optional notes about the quiz"
></textarea>

<div class="d-flex justify-content-end gap-2">

<button
class="btn btn-secondary"
@click="closeQuizModal"
>
Cancel
</button>

<button
class="btn btn-success"
@click="createQuiz"
>
Create Quiz
</button>

</div>

</div>

</div>


<!-- QUIZ OVERVIEW -->
<div v-if="selectedQuiz" class="modal-overlay">

<div class="custom-modal">

<h4>Quiz #{{ selectedQuiz.id }}</h4>

<p><strong>Date:</strong> {{ selectedQuiz.date_of_quiz }}</p>

<p><strong>Duration:</strong> {{ selectedQuiz.time_duration }}</p>

<p><strong>Questions:</strong> {{ selectedQuiz.questions?.length || 0 }}</p>

<button class="btn btn-dark w-100" @click="selectedQuiz=null">
Close
</button>

</div>

</div>

</div>

</template>



<script>

export default{

data(){
return{

subjects:[],
chapters:[],
quizzes:[],

chapterSearch:"",
quizSearch:{},

showAddModal:false,
editChapter:null,

newChapter:{
subject_id:"",
name:"",
description:"",
difficulty:1
},

addQuizChapter:null,

newQuiz:{
date_of_quiz:"",
time_duration:"",
remarks:""
},

selectedQuiz:null,

baseURL:"http://localhost:5000/api"

}
},

computed:{

filteredChapters(){

if(!this.chapterSearch) return this.chapters

const q=this.chapterSearch.toLowerCase()

return this.chapters.filter(c =>
c.name.toLowerCase().includes(q)
)

}

},

methods:{


getSubjectName(id){
const subject=this.subjects.find(s => s.id===id)
return subject ? subject.name : "Unknown"
},

getQuizzes(chapterId){
return this.quizzes.filter(q => q.chapter_id===chapterId)
},
async createChapter(){

  const token = localStorage.getItem("access_token")

  // -------- VALIDATION --------
  if(!this.newChapter.subject_id || !this.newChapter.name || this.newChapter.difficulty === ""){
    alert("All fields are required")
    return
  }

  // -------- DUPLICATE CHECK --------
  const duplicate = this.chapters.find(c =>
    c.subject_id === this.newChapter.subject_id &&
    c.name.toLowerCase().trim() === this.newChapter.name.toLowerCase().trim()
  )

  if(duplicate){
    alert("Chapter already exists in this subject")
    return
  }

  try{

    const res = await fetch(`${this.baseURL}/chapters`,{

      method:"POST",

      headers:{
        "Content-Type":"application/json",
        Authorization:`Bearer ${token}`
      },

      body:JSON.stringify({
        subject_id:this.newChapter.subject_id,
        name:this.newChapter.name,
        description:this.newChapter.description,
        difficulty:this.newChapter.difficulty
      })

    })

    const data = await res.json()

    if(!res.ok){
      alert(data.message || "Chapter creation failed")
      return
    }

    // -------- RESET FORM --------
    this.newChapter = {
      subject_id:"",
      name:"",
      description:"",
      difficulty:1
    }

    // -------- CLOSE MODAL --------
    this.showAddModal = false

    // -------- REFRESH DATA --------
    await this.fetchChapters()

  }catch(err){

    console.error("Create chapter error:",err)

  }

},

filteredQuizzes(chapter){

const search=this.quizSearch[chapter.id]?.toLowerCase()

const quizzes=this.getQuizzes(chapter.id)

if(!search) return quizzes

return quizzes.filter(q =>
q.id.toString().includes(search)
)

},

openEditChapter(chapter){
this.editChapter={...chapter}
},

openAddQuiz(chapter){
this.addQuizChapter=chapter
},

openQuizOverview(quiz){
this.selectedQuiz=quiz
},


async updateChapter(){

const token = localStorage.getItem("access_token")

// check duplicate chapter name in same subject
const duplicate = this.chapters.find(c =>
  c.id !== this.editChapter.id &&
  c.subject_id === this.editChapter.subject_id &&
  c.name.toLowerCase().trim() === this.editChapter.name.toLowerCase().trim()
)

if(duplicate){
  alert("A chapter with this name already exists in this subject")
  return
}

try{

await fetch(`${this.baseURL}/chapters/${this.editChapter.id}`,{

method:"PATCH",

headers:{
"Content-Type":"application/json",
Authorization:`Bearer ${token}`
},

body:JSON.stringify({
name:this.editChapter.name,
description:this.editChapter.description,
difficulty:this.editChapter.difficulty
})

})

this.editChapter = null
await this.fetchChapters()

}catch(err){

console.error("Update error:",err)

}

},


async deleteChapter(chapterId){

const confirmDelete = confirm("Are you sure you want to delete this chapter?")
if(!confirmDelete) return

const token = localStorage.getItem("access_token")

try{

const res = await fetch(`${this.baseURL}/chapters/${chapterId}`,{
method:"DELETE",
headers:{
Authorization:`Bearer ${token}`
}
})

if(res.ok){

// refresh UI
await this.fetchChapters()
await this.fetchQuizzes()

}else{

const data = await res.json()
alert(data.message || "Delete failed")

}

}catch(err){

console.error("Delete error:",err)

}

},


async createQuiz(){

const token = localStorage.getItem("access_token")

if(!this.newQuiz.date_of_quiz || !this.newQuiz.time_duration){
  alert("Date and duration are required")
  return
}

try{

const res = await fetch(`${this.baseURL}/quizzes`,{

method:"POST",

headers:{
"Content-Type":"application/json",
Authorization:`Bearer ${token}`
},

body:JSON.stringify({
chapter_id:this.addQuizChapter.id,
date_of_quiz:new Date(this.newQuiz.date_of_quiz).toISOString(),
time_duration:this.newQuiz.time_duration,
remarks:this.newQuiz.remarks
})

})

if(!res.ok){
const data = await res.json()
alert(data.message || "Quiz creation failed")
return
}

this.newQuiz = {
date_of_quiz:"",
time_duration:"",
remarks:""
}

this.addQuizChapter = null

await this.fetchQuizzes()

}catch(err){

console.error("Quiz creation error:",err)

}

},


async fetchSubjects(){

const token=localStorage.getItem("access_token")

const res=await fetch(`${this.baseURL}/subjects`,{
headers:{Authorization:`Bearer ${token}`}
})

const data=await res.json()

this.subjects=data.subjects || []

},


async fetchChapters(){

const token=localStorage.getItem("access_token")

const res=await fetch(`${this.baseURL}/chapters`,{
headers:{Authorization:`Bearer ${token}`}
})

const data=await res.json()

this.chapters=data.chapters || []

},


async fetchQuizzes(){

const token=localStorage.getItem("access_token")

const res=await fetch(`${this.baseURL}/quizzes`,{
headers:{Authorization:`Bearer ${token}`}
})

const data=await res.json()

this.quizzes=data.quizzes || []

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

}

}

</script>



<style scoped>

.chapter-page{
background:#f5f7fb;
min-height:100vh;
}

.chapter-card{
background:white;
border-radius:14px;
padding:18px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
transition:0.2s;
}

.chapter-card:hover{
transform:translateY(-4px);
box-shadow:0 8px 18px rgba(0,0,0,0.12);
}

.chapter-header{
display:flex;
justify-content:space-between;
align-items:center;
}

.subject-label{
font-size:12px;
color:#888;
font-weight:600;
}

.quiz-count{
font-size:0.8rem;
color:#777;
margin-left:5px;
}

.quiz-list{
max-height:200px;
overflow:auto;
margin-top:10px;
}

.quiz-item{
display:flex;
justify-content:space-between;
padding:6px 4px;
border-bottom:1px solid #eee;
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
box-shadow:0 6px 20px rgba(0,0,0,0.3);
}

.modal-overlay{
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
background:rgba(0,0,0,0.5);
display:flex;
align-items:center;
justify-content:center;
z-index:2000;
}

.custom-modal{
background:white;
padding:25px;
border-radius:12px;
width:420px;
box-shadow:0 10px 25px rgba(0,0,0,0.2);
}

</style>