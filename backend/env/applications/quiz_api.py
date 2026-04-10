from env.applications.models import db, Quiz, Chapter
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt
from flask_restful import Resource
from flask import request, current_app
from flask_caching import Cache
from datetime import datetime
from tasks.daily_reminder_task import daily_reminder_job
from env.extensions import cache



class QuizAPI(Resource):

    @jwt_required()
    @cache.cached(
        timeout=300,
        key_prefix=lambda: (
            f"quizzes_chapter_{request.view_args.get('chapter_id')}"
            if request.view_args and request.view_args.get("chapter_id")
            else "all_quizzes"
        )
    )
    def get(self, chapter_id=None):
        """
        GET /api/quizzes
        GET /api/quizzes/chapter/<chapter_id>
        """

        if chapter_id:
            chapter = Chapter.query.get(chapter_id)
            if not chapter:
                return {"message": "Chapter not found"}, 404

            quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
        else:
            quizzes = Quiz.query.all()

        return {"quizzes": [q.to_json() for q in quizzes]}, 200

    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]

        if role != "admin":
            return {"message": "Admin access required"}, 403

        data = request.get_json() or {}

        chapter_id = data.get("chapter_id")
        date_of_quiz = data.get("date_of_quiz")
        time_duration = data.get("time_duration")
        remarks = data.get("remarks")

        if not chapter_id or not date_of_quiz or not time_duration:
            return {"message": "Missing required fields"}, 400

        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message": "Chapter not found"}, 404

        try:
            quiz_date = datetime.fromisoformat(date_of_quiz)
        except ValueError:
            return {"message": "Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"}, 400

        quiz = Quiz(
            chapter_id=chapter_id,
            date_of_quiz=quiz_date,
            time_duration=time_duration.strip(),
            remarks=remarks.strip() if remarks else None
        )

        db.session.add(quiz)
        db.session.commit()
        daily_reminder_job.delay()
        # 🔴 Clear cache after creation
        cache.clear()

        return {
            "message": "Quiz created successfully",
            "quiz": quiz.to_json()
        }, 201


    @jwt_required()
    def patch(self, quiz_id):
        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]

        if role!= "admin":
            return {"message": "Admin access required"}, 403

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404

        data = request.get_json() or {}

        if "date_of_quiz" in data:
            try:
                quiz.date_of_quiz = datetime.fromisoformat(data["date_of_quiz"])
            except ValueError:
                return {"message": "Invalid date format"}, 400

        if "time_duration" in data:
            quiz.time_duration = data["time_duration"].strip()

        if "remarks" in data:
            quiz.remarks = data["remarks"].strip()

        db.session.commit()

        # 🔴 Clear cache after update
        cache.clear()

        return {
            "message": "Quiz updated successfully",
            "quiz": quiz.to_json()
        }, 200


    @jwt_required()
    def delete(self, quiz_id):
        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]

        if role!= "admin":
            return {"message": "Admin access required"}, 403

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404

        db.session.delete(quiz)
        db.session.commit()

        cache.clear()

        return {"message": "Quiz deleted successfully"}, 200
