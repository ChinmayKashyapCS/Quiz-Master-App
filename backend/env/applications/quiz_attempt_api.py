from env.applications.models import db, Quiz, Question, Score
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt
from flask_restful import Resource
from flask import request, current_app
from flask_caching import Cache
from datetime import datetime

from env.extensions import cache



class QuizAttemptAPI(Resource):

    # -------------------- START QUIZ (CACHED) --------------------
    @jwt_required()
    @cache.cached(
        timeout=300,
        key_prefix=lambda: f"quiz_start_{request.view_args.get('quiz_id')}"
    )
    def get(self, quiz_id):
        """
        User starts a quiz.
        Sends quiz metadata + questions (without correct answers).
        Cached because quiz content is same for all users.
        """

        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]

        if role != "user":
            return {"message": "Only users can attempt quizzes"}, 403

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404

        # ❌ DO NOT CACHE attempt check → must be dynamic
        existing_attempt = Score.query.filter_by(
            user_id=user_id,
            quiz_id=quiz_id
        ).first()

        if existing_attempt:
            return {"message": "Quiz already attempted"}, 409

        return {
            "quiz": {
                "id": quiz.id,
                "chapter_id": quiz.chapter_id,
                "date_of_quiz": quiz.date_of_quiz.isoformat(),
                "time_duration": quiz.time_duration,
                "remarks": quiz.remarks,
                "questions": [q.to_json() for q in quiz.questions]
            }
        }, 200


    # -------------------- SUBMIT QUIZ (NOT CACHED) --------------------
    @jwt_required()
    def post(self, quiz_id):
        """
        User submits quiz answers.
        Calculates score and stores result.
        NEVER cached.
        """

        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]

        if role!= "user":
            return {"message": "Only users can submit quizzes"}, 403

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404

        # Prevent multiple attempts
        if Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).first():
            return {"message": "Quiz already attempted"}, 409

        data = request.get_json() or {}
        answers = data.get("answers")

        if not answers or not isinstance(answers, dict):
            return {"message": "Answers must be provided"}, 400

        total_score = 0
        questions = Question.query.filter_by(quiz_id=quiz_id).all()

        for question in questions:
            selected_option = answers.get(str(question.id))
            if selected_option and int(selected_option) == question.correct_option:
                total_score += 1

        score_entry = Score(
            user_id=user_id,
            quiz_id=quiz_id,
            score=total_score,
            attempted_at=datetime.utcnow()
        )

        db.session.add(score_entry)
        db.session.commit()

        return {
            "message": "Quiz submitted successfully",
            "result": {
                "quiz_id": quiz_id,
                "total_questions": len(questions),
                "score": total_score
            }
        }, 201
