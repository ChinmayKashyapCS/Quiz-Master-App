from env.applications.models import db, User
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    get_jwt
)
from flask_restful import Resource
from flask import request
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# -------------------- LOGIN --------------------
class LoginAPI(Resource):
    def post(self):
        data = request.get_json() or {}

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email and password are required"}, 400


        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return {"message": "Invalid credentials"}, 401

        # JWT identity contains id and role
        access_token = create_access_token(
            identity=str(user.id),                 # MUST be string
            additional_claims={"role": user.role}  # extra data here
        )

        return {
            "message": "Login successful",
            "access_token": access_token,
            "user": user.to_json()
        }, 200


# -------------------- REGISTER (USER ONLY) --------------------
class RegisterAPI(Resource):
    def post(self):
        data = request.get_json() or {}

        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")
        qualification = data.get("qualification")

        # ---- DOB FIX ----
        dob_str = data.get("dob")
        dob = None
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%d-%m-%Y").date()
            except ValueError:
                return {"message": "DOB must be in DD-MM-YYYY format"}, 400

        if not full_name or not email or not password:
            return {"message": "Missing required fields"}, 400

        if len(password) < 4:
            return {"message": "Password must be at least 4 characters"}, 400

        if User.query.filter_by(email=email).first():
            return {"message": "User already exists"}, 400

        hashed_password = generate_password_hash(password)

        user = User(
            full_name=full_name.lower().strip(),
            email=email,
            password=hashed_password,
            qualification=qualification,
            dob=dob,
            role="user",
            is_admin=False
        )

        db.session.add(user)
        db.session.commit()

        return {
            "message": "User registered successfully",
            "user": user.to_json()
        }, 201


# -------------------- EDIT PROFILE --------------------
class EditAPI(Resource):
    @jwt_required()
    def patch(self):
        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]
        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 404

        data = request.get_json() or {}

        if "full_name" in data:
            user.full_name = data["full_name"].lower().strip()

        if "password" in data:
            if len(data["password"]) <= 4:
                return {"message": "Password too short"}, 400
            user.password = generate_password_hash(data["password"])

        if "qualification" in data:
            user.qualification = data["qualification"]

        # ---- DOB FIX ----
        if "dob" in data:
            try:
                user.dob = datetime.strptime(data["dob"], "%d-%m-%Y").date()
            except ValueError:
                return {"message": "DOB must be in DD-MM-YYYY format"}, 400

        db.session.commit()

        return {
            "message": "Profile updated successfully",
            "user": user.to_json()
        }, 200


# -------------------- ADMIN: VIEW ALL USERS --------------------
# -------------------- ADMIN: VIEW ALL USERS --------------------
class AdminUsersAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]

        if role != "admin":
            return {"message": "Admin access required"}, 403

        # Filter to only show users with role "user" if you want to hide admins from the list
        users = User.query.filter_by(role="user").all()
        
        # We return the list directly to match your frontend's await res.json() logic
        return [u.to_json() for u in users], 200
