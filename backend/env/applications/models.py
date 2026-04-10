from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    qualification = db.Column(db.String(100))
    dob = db.Column(db.Date)

    role = db.Column(db.String(20), nullable=False, default="user")  # admin / user
    is_admin = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    scores = db.relationship("Score", backref="user", cascade="all, delete-orphan")

    def to_json(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "qualification": self.qualification,
            "dob": self.dob.isoformat() if self.dob else None,
            "role": self.role,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<User {self.email}>"

class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False)

    created_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    chapters = db.relationship("Chapter", backref="subject", cascade="all, delete-orphan")

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_by": self.created_by,
            "chapters": [c.to_json() for c in self.chapters]
        }

    def __repr__(self):
        return f"<Subject {self.name}>"

class Chapter(db.Model):
    __tablename__ = "chapters"

    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    difficulty = db.Column(db.Integer, nullable=False)

    quizzes = db.relationship("Quiz", backref="chapter", cascade="all, delete-orphan")

    def to_json(self):
        return {
            "id": self.id,
            "subject_id": self.subject_id,
            "name": self.name,
            "description": self.description,
            "difficulty": self.difficulty
        }

    def __repr__(self):
        return f"<Chapter {self.name}>"


class Quiz(db.Model):
    __tablename__ = "quizzes"

    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)

    date_of_quiz = db.Column(db.DateTime, nullable=False)
    time_duration = db.Column(db.String(10), nullable=False)  # HH:MM
    remarks = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship("Question", backref="quiz", cascade="all, delete-orphan")
    scores = db.relationship("Score", backref="quiz", cascade="all, delete-orphan")

    def to_json(self):
        return {
            "id": self.id,
            "chapter_id": self.chapter_id,
            "date_of_quiz": self.date_of_quiz.isoformat(),
            "time_duration": self.time_duration,
            "remarks": self.remarks,
            "questions": [q.to_json() for q in self.questions]
        }

    def __repr__(self):
        return f"<Quiz {self.id}>"

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)

    question_statement = db.Column(db.String(500), nullable=False)

    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)

    correct_option = db.Column(db.Integer, nullable=False)  # 1–4

    def to_json(self):
        return {
            "id": self.id,
            "quiz_id": self.quiz_id,
            "question_statement": self.question_statement,
            "options": {
                "1": self.option1,
                "2": self.option2,
                "3": self.option3,
                "4": self.option4
            },
            "correct_option": self.correct_option
        }

    def __repr__(self):
        return f"<Question {self.id}>"


class Score(db.Model):
    __tablename__ = "scores"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)

    score = db.Column(db.Integer, nullable=False)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("user_id", "quiz_id", name="unique_user_quiz_attempt"),
    )

    def to_json(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "quiz_id": self.quiz_id,
            "score": self.score,
            "attempted_at": self.attempted_at.isoformat()
        }

    def __repr__(self):
        return f"<Score {self.score}>"
