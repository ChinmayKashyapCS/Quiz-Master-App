from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


class WelcomeAPI(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()

        return {
            "message": "Welcome to Quiz Master - V2",
            "user_id": identity["id"],
            "role": identity["role"]
        }, 200
