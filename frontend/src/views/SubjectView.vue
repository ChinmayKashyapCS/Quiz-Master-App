<template>
<div class="subject-page">

<!-- NAVBAR -->
<nav class="navbar navbar-dark bg-dark px-4 shadow">
  <div class="d-flex align-items-center w-100">

    <button class="btn btn-outline-light me-4"
      @click="$router.push('/admin/dashboard')">
      Admin Dashboard
    </button>
    

    <button class="btn btn-outline-light me-2"
      @click="$router.push('/admin/chapters')">
      Chapters
    </button>

    <button class="btn btn-outline-light me-2"
      @click="$router.push('/admin/quizzes')">
      Quizzes
    </button>

    

    <h4 class="text-white fw-bold flex-grow-1 text-center m-0">
      Subjects
    </h4>

    <input
      v-model="subjectSearch"
      class="form-control w-25 me-3"
      placeholder="Search subject by name or ID"
    />

    <button class="btn btn-danger" @click="logout">
      Logout
    </button>

  </div>
</nav>


<!-- SUBJECT LIST -->
<div class="container py-4">

  <div class="row g-4">

    <div
      class="col-lg-4"
      v-for="subject in filteredSubjects"
      :key="subject.id"
    >

      <div class="subject-card">

        <!-- SUBJECT HEADER -->
        <div class="subject-header">

          <h5 class="fw-bold text-center flex-grow-1">
            {{ subject.name }}
            <span class="chapter-count">
              ({{ subject.chapters?.length || 0 }})
            </span>
          </h5>

          <div class="d-flex gap-2">

            <button
              class="btn btn-sm btn-outline-primary"
              @click="openEditSubject(subject)"
            >
              Edit
            </button>

            <button
              class="btn btn-sm btn-outline-danger"
              @click="deleteSubject(subject.id)"
            >
              Delete
            </button>

          </div>

        </div>

        <!-- CHAPTER SEARCH -->
        <input
          v-model="chapterSearch[subject.id]"
          class="form-control form-control-sm my-2"
          placeholder="Search chapter..."
        />

        <!-- CHAPTER LIST -->
        <div class="chapter-list">

          <div
            class="chapter-item"
            v-for="chapter in filteredChapters(subject)"
            :key="chapter.id"
          >

            <div class="chapter-name">
              {{ chapter.name }}
            </div>

            <button
              class="btn btn-sm btn-outline-secondary"
              @click="openChapterOverview(chapter)"
            >
              Overview
            </button>

          </div>

        </div>

        <!-- ADD CHAPTER BUTTON -->
        <div class="text-center mt-3">
          <button
            class="btn btn-sm btn-success"
            @click="openAddChapter(subject)"
          >
            + Chapter
          </button>
        </div>

      </div>

    </div>

  </div>

</div>


<!-- BIG ADD SUBJECT BUTTON -->
<div class="add-subject-btn">

  <button
    class="btn btn-warning add-subject-circle"
    @click="showAddModal = true"
  >
    +
  </button>

</div>


<!-- ADD SUBJECT MODAL -->
<div v-if="showAddModal" class="modal-overlay">

  <div class="custom-modal">

    <h4 class="mb-3 text-center">New Subject</h4>

    <input
      v-model="newSubject.name"
      class="form-control mb-3"
      placeholder="Subject Name"
    />

    <textarea
      v-model="newSubject.description"
      class="form-control mb-3"
      placeholder="Subject Description"
    ></textarea>

    <div class="d-flex justify-content-end gap-2">

      <button
        class="btn btn-secondary"
        @click="showAddModal = false"
      >
        Cancel
      </button>

      <button
        class="btn btn-primary"
        @click="createSubject"
      >
        Save
      </button>

    </div>

  </div>

</div>


<!-- ADD CHAPTER MODAL -->
<div v-if="addChapterSubject" class="modal-overlay">

  <div class="custom-modal">

    <h4>Add Chapter</h4>

    <input
      v-model="newChapter.name"
      class="form-control mb-2"
      placeholder="Chapter Name"
    />

    <textarea
      v-model="newChapter.description"
      class="form-control mb-2"
      placeholder="Description"
    ></textarea>

    <input
      v-model="newChapter.difficulty"
      type="number"
      class="form-control mb-3"
      placeholder="Difficulty (1-5)"
    />

    <div class="d-flex justify-content-end gap-2">

      <button
        class="btn btn-secondary"
        @click="addChapterSubject=null"
      >
        Cancel
      </button>

      <button
        class="btn btn-success"
        @click="createChapter"
      >
        Save
      </button>

    </div>

  </div>

</div>


<!-- EDIT SUBJECT MODAL -->
<div v-if="editSubject" class="modal-overlay">

  <div class="custom-modal">

    <h4>Edit Subject</h4>

    <input
      v-model="editSubject.name"
      class="form-control mb-2"
    />

    <textarea
      v-model="editSubject.description"
      class="form-control mb-3"
    ></textarea>

    <div class="d-flex justify-content-end gap-2">

      <button
        class="btn btn-secondary"
        @click="editSubject=null"
      >
        Close
      </button>

      <button
        class="btn btn-success"
        @click="updateSubject"
      >
        Save
      </button>

    </div>

  </div>

</div>


<!-- CHAPTER OVERVIEW -->
<div v-if="selectedChapter" class="modal-overlay">

  <div class="custom-modal">

    <h4>{{ selectedChapter.name }}</h4>

    <p>
      <strong>Description:</strong>
      {{ selectedChapter.description }}
    </p>

    <p>
      <strong>Quizzes:</strong>
      {{ getQuizCount(selectedChapter.id) }}
    </p>

    <button
      class="btn btn-dark w-100"
      @click="selectedChapter=null"
    >
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
quizzes:[],

subjectSearch:"",

chapterSearch:{},

showAddModal:false,

newSubject:{
name:"",
description:""
},

addChapterSubject:null,

newChapter:{
name:"",
description:"",

},

editSubject:null,

selectedChapter:null,

baseURL:"http://localhost:5000/api"

}
},

computed:{

filteredSubjects(){

if(!this.subjectSearch) return this.subjects

const q=this.subjectSearch.toLowerCase()

return this.subjects.filter(s =>
s.name.toLowerCase().includes(q) ||
s.id.toString().includes(q)
)

}

},

methods:{


filteredChapters(subject){

const search=this.chapterSearch[subject.id]?.toLowerCase()

if(!search) return subject.chapters || []

return subject.chapters.filter(c =>
c.name.toLowerCase().includes(search)
)

},


openEditSubject(subject){
this.editSubject={...subject}
},


openChapterOverview(chapter){
this.selectedChapter=chapter
},


openAddChapter(subject){
this.addChapterSubject=subject
},


getQuizCount(chapterId){
return this.quizzes.filter(q => q.chapter_id===chapterId).length
},


async createSubject(){

const token=localStorage.getItem("access_token")

await fetch(`${this.baseURL}/subjects`,{

method:"POST",

headers:{
"Content-Type":"application/json",
Authorization:`Bearer ${token}`
},

body:JSON.stringify(this.newSubject)

})

this.showAddModal=false
this.fetchSubjects()

},


async deleteSubject(subjectId){

const confirmDelete = confirm("Delete this subject? All chapters and quizzes will be removed.")

if(!confirmDelete) return

const token = localStorage.getItem("access_token")

await fetch(`${this.baseURL}/subjects/${subjectId}`,{

method:"DELETE",

headers:{
Authorization:`Bearer ${token}`
}

})

this.fetchSubjects()
this.fetchQuizzes()

},


async createChapter(){

const token=localStorage.getItem("access_token")

await fetch(`${this.baseURL}/chapters`,{

method:"POST",

headers:{
"Content-Type":"application/json",
Authorization:`Bearer ${token}`
},

body:JSON.stringify({
subject_id:this.addChapterSubject.id,
name:this.newChapter.name,
description:this.newChapter.description,
difficulty:this.newChapter.difficulty
})

})

this.addChapterSubject=null
this.fetchSubjects()

},


async updateSubject(){

const token=localStorage.getItem("access_token")

await fetch(`${this.baseURL}/subjects/${this.editSubject.id}`,{

method:"PATCH",

headers:{
"Content-Type":"application/json",
Authorization:`Bearer ${token}`
},

body:JSON.stringify({
name:this.editSubject.name,
description:this.editSubject.description
})

})

this.editSubject=null
this.fetchSubjects()

},


async fetchSubjects(){

const token=localStorage.getItem("access_token")

const res=await fetch(`${this.baseURL}/subjects`,{
headers:{Authorization:`Bearer ${token}`}
})

const data=await res.json()

this.subjects=data.subjects || []

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
await this.fetchQuizzes()

}

}
</script>



<style scoped>

.subject-page{
background:#f5f7fb;
min-height:100vh;
}

.subject-card{
background:white;
border-radius:14px;
padding:18px;
box-shadow:0 4px 12px rgba(0,0,0,0.08);
transition:0.2s;
}

.subject-card:hover{
transform:translateY(-4px);
box-shadow:0 8px 18px rgba(0,0,0,0.12);
}

.subject-header{
display:flex;
align-items:center;
justify-content:space-between;
}

.chapter-count{
font-size:0.8rem;
color:#666;
margin-left:5px;
}

.chapter-list{
max-height:200px;
overflow:auto;
margin-top:10px;
}

.chapter-item{
display:flex;
justify-content:space-between;
align-items:center;
padding:6px 4px;
border-bottom:1px solid #eee;
}

.add-subject-btn{
position:fixed;
bottom:30px;
left:50%;
transform:translateX(-50%);
}

.add-subject-circle{
width:80px;
height:80px;
font-size:36px;
border-radius:10%;
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