from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


class WelcomeAPI(Resource):

    @jwt_required()
    def get(self):

        # -------- GET DATA --------
        identity = get_jwt_identity()   # this is STRING (user id)
        claims = get_jwt()              # contains role

        # -------- SAFE CONVERSION --------
        try:
            user_id = int(identity)
        except:
            user_id = identity  # fallback (just in case)

        role = claims.get("role", "user")

        # -------- RESPONSE --------
        return {
            "message": "Welcome to Quiz Master - V2",
            "user_id": user_id,
            "role": role
        }, 200