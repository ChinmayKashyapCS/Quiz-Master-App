from env.applications.models import db, Subject
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt
from flask_restful import Resource
from flask import request, current_app
from flask_caching import Cache

from env.extensions import cache



class SubjectAPI(Resource):

    # -------------------- GET SUBJECTS (CACHED) --------------------
    @jwt_required()
    @cache.cached(timeout=300, key_prefix="all_subjects")
    def get(self):
        """
        Admin/User can view all subjects.
        Cached to reduce database load.
        """
        subjects = Subject.query.all()
        return {
            "subjects": [s.to_json() for s in subjects]
        }, 200


    # -------------------- CREATE SUBJECT (ADMIN ONLY) --------------------
    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]

        if role != "admin":
            return {"message": "Admin access required"}, 403

        data = request.get_json() or {}
        name = data.get("name")
        description = data.get("description")

        if not name or not description:
            return {"message": "Name and description are required"}, 400

        if Subject.query.filter_by(name=name.strip()).first():
            return {"message": "Subject already exists"}, 409

        subject = Subject(
            name=name.strip(),
            description=description.strip(),
            created_by=user_id
        )

        db.session.add(subject)
        db.session.commit()

        # 🔴 IMPORTANT: clear cache after data change
        cache.clear()

        return {
            "message": "Subject created successfully",
            "subject": subject.to_json()
        }, 201


    # -------------------- UPDATE SUBJECT (ADMIN ONLY) --------------------
    @jwt_required()
    def patch(self, subject_id):
        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]

        if role != "admin":
            return {"message": "Admin access required"}, 403

        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message": "Subject not found"}, 404

        data = request.get_json() or {}

        if "name" in data:
            if not data["name"].strip():
                return {"message": "Invalid subject name"}, 400
            subject.name = data["name"].strip()

        if "description" in data:
            subject.description = data["description"].strip()

        db.session.commit()

        # 🔴 Clear cache so updated data is reflected
        cache.clear()

        return {
            "message": "Subject updated successfully",
            "subject": subject.to_json()
        }, 200


    # -------------------- DELETE SUBJECT (ADMIN ONLY) --------------------
    @jwt_required()
    def delete(self, subject_id):
        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]

        if role != "admin":
            return {"message": "Admin access required"}, 403

        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message": "Subject not found"}, 404

        db.session.delete(subject)
        db.session.commit()

        # 🔴 Clear cache after deletion
        cache.clear()

        return {"message": "Subject deleted successfully"}, 200
