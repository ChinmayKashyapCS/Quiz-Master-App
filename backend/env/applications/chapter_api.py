from env.applications.models import db, Subject, Chapter
from flask_jwt_extended import jwt_required, get_jwt_identity,get_jwt
from flask_restful import Resource
from flask import request, current_app
from flask_caching import Cache
from env.extensions import cache





class ChapterAPI(Resource):

    # -------------------- GET CHAPTERS --------------------
    @jwt_required()
    @cache.cached(
        timeout=300,
        key_prefix=lambda: (
            f"chapters_subject_{request.view_args.get('subject_id')}"
            if request.view_args and request.view_args.get("subject_id")
            else "all_chapters"
        )
    )
    def get(self, subject_id=None):
        """
        GET /api/chapters
        GET /api/chapters/subject/<subject_id>
        """

        if subject_id:
            subject = Subject.query.get(subject_id)
            if not subject:
                return {"message": "Subject not found"}, 404

            chapters = Chapter.query.filter_by(subject_id=subject_id).all()
        else:
            chapters = Chapter.query.all()

        return {"chapters": [c.to_json() for c in chapters]}, 200


    # -------------------- CREATE CHAPTER (ADMIN ONLY) --------------------
    @jwt_required()
    def post(self):
        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]

        if role != "admin":
            return {"message": "Admin access required"}, 403

        data = request.get_json() or {}

        subject_id = data.get("subject_id")
        name = data.get("name")
        description = data.get("description")
        difficulty = data.get("difficulty")

        if not subject_id or not name or difficulty is None:
            return {"message": "Missing required fields"}, 400

        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message": "Subject not found"}, 404

        chapter = Chapter(
            subject_id=subject_id,
            name=name.strip(),
            description=description.strip() if description else None,
            difficulty=int(difficulty)
        )

        db.session.add(chapter)
        db.session.commit()

        # 🔴 IMPORTANT: Clear cache after data change
        cache.clear()

        return {
            "message": "Chapter created successfully",
            "chapter": chapter.to_json()
        }, 201


    # -------------------- UPDATE CHAPTER (ADMIN ONLY) --------------------
    @jwt_required()
    def patch(self, chapter_id):
        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]

        if role != "admin":
            return {"message": "Admin access required"}, 403

        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message": "Chapter not found"}, 404

        data = request.get_json() or {}

        if "name" in data:
            chapter.name = data["name"].strip()

        if "description" in data:
            chapter.description = data["description"].strip()

        if "difficulty" in data:
            chapter.difficulty = int(data["difficulty"])

        db.session.commit()

        # 🔴 Clear cache so updated data is reflected
        cache.clear()

        return {
            "message": "Chapter updated successfully",
            "chapter": chapter.to_json()
        }, 200


    # -------------------- DELETE CHAPTER (ADMIN ONLY) --------------------
    @jwt_required()
    def delete(self, chapter_id):
        user_id = int(get_jwt_identity())
        role = get_jwt()["role"]

        if role != "admin":
            return {"message": "Admin access required"}, 403

        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message": "Chapter not found"}, 404

        db.session.delete(chapter)
        db.session.commit()

        # 🔴 Clear cache after deletion
        cache.clear()

        return {"message": "Chapter deleted successfully"}, 200
