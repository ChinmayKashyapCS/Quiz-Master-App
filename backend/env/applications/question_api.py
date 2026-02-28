from env.applications.models import db, Quiz, Question
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt
from flask_restful import Resource
from flask import request, current_app
from flask_caching import Cache
from env.extensions import cache




class QuestionAPI(Resource):

    # -------------------- GET QUESTIONS (CACHED) --------------------
    @jwt_required()
    @cache.cached(
        timeout=300,
        key_prefix=lambda: (
            f"questions_quiz_{request.view_args.get('quiz_id')}"
            if request.view_args and request.view_args.get("quiz_id")
            else "all_questions"
        )
    )
    def get(self, quiz_id=None):
        """
        Admin/User can view questions.
        If quiz_id is provided → questions under that quiz.
        Correct answer is NOT exposed.
        Cached for performance.
        """

        if quiz_id:
            quiz = Quiz.query.get(quiz_id)
            if not quiz:
                return {"message": "Quiz not found"}, 404

            questions = Question.query.filter_by(quiz_id=quiz_id).all()
        else:
            questions = Question.query.all()

        return {
            "questions": [q.to_json() for q in questions]
        }, 200


    # -------------------- CREATE QUESTION (ADMIN ONLY) --------------------
    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]

        if role != "admin":
            return {"message": "Admin access required"}, 403

        data = request.get_json() or {}

        quiz_id = data.get("quiz_id")
        question_statement = data.get("question_statement")
        options = data.get("options")
        correct_option = data.get("correct_option")

        if not quiz_id or not question_statement or not options or correct_option is None:
            return {"message": "Missing required fields"}, 400

        if not isinstance(options, dict) or len(options) != 4:
            return {"message": "Exactly 4 options are required"}, 400

        if correct_option not in [1, 2, 3, 4]:
            return {"message": "correct_option must be between 1 and 4"}, 400

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404

        question = Question(
            quiz_id=quiz_id,
            question_statement=question_statement.strip(),
            option1=options["1"],
            option2=options["2"],
            option3=options["3"],
            option4=options["4"],
            correct_option=correct_option
        )

        db.session.add(question)
        db.session.commit()

        # 🔴 Clear cache after data modification
        cache.clear()

        return {
            "message": "Question added successfully",
            "question": question.to_json()
        }, 201


    # -------------------- UPDATE QUESTION (ADMIN ONLY) --------------------
    @jwt_required()
    def patch(self, question_id):
        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]

        if role != "admin":
            return {"message": "Admin access required"}, 403

        question = Question.query.get(question_id)
        if not question:
            return {"message": "Question not found"}, 404

        data = request.get_json() or {}

        if "question_statement" in data:
            question.question_statement = data["question_statement"].strip()

        if "options" in data:
            options = data["options"]
            if len(options) != 4:
                return {"message": "Exactly 4 options required"}, 400

            question.option1 = options["1"]
            question.option2 = options["2"]
            question.option3 = options["3"]
            question.option4 = options["4"]

        if "correct_option" in data:
            if data["correct_option"] not in [1, 2, 3, 4]:
                return {"message": "Invalid correct option"}, 400
            question.correct_option = data["correct_option"]

        db.session.commit()

        # 🔴 Clear cache after update
        cache.clear()

        return {
            "message": "Question updated successfully",
            "question": question.to_json()
        }, 200


    # -------------------- DELETE QUESTION (ADMIN ONLY) --------------------
    @jwt_required()
    def delete(self, question_id):
        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]

        if role != "admin":
            return {"message": "Admin access required"}, 403

        question = Question.query.get(question_id)
        if not question:
            return {"message": "Question not found"}, 404

        db.session.delete(question)
        db.session.commit()

        # 🔴 Clear cache after deletion
        cache.clear()

        return {"message": "Question deleted successfully"}, 200
