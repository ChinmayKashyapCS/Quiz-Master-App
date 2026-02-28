from env.applications.models import db, Score, Quiz, User
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt
from flask_restful import Resource


class ScoreAPI(Resource):

    # -------------------- USER: VIEW OWN SCORES --------------------
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]

        # USER → view own scores
        if role== "user":
            scores = Score.query.filter_by(user_id=user_id).all()

            return {
                "scores": [s.to_json() for s in scores]
            }, 200

        # ADMIN → view all scores
        if role == "admin":
            scores = Score.query.all()

            result = []
            for s in scores:
                quiz = Quiz.query.get(s.quiz_id)
                user = User.query.get(s.user_id)

                result.append({
                    "score_id": s.id,
                    "user_id": s.user_id,
                    "user_name": user.full_name if user else None,
                    "quiz_id": s.quiz_id,
                    "chapter_id": quiz.chapter_id if quiz else None,
                    "score": s.score,
                    "attempted_at": s.attempted_at.isoformat()
                })

            return {
                "scores": result
            }, 200

        return {"message": "Unauthorized access"}, 403
