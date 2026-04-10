from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from werkzeug.security import generate_password_hash
from env.applications.models import db, User
from env.extensions import cache
from celery_config import init_celery
from flask_cors import CORS
from celery_config import celery
# APIs
from env.applications.authentication_api import (
    RegisterAPI, LoginAPI, EditAPI, AdminUsersAPI
)
from env.applications.report_api import DownloadReportAPI
from env.applications.subject_api import SubjectAPI
from env.applications.chapter_api import ChapterAPI
from env.applications.quiz_api import QuizAPI
from env.applications.question_api import QuestionAPI
from env.applications.quiz_attempt_api import QuizAttemptAPI
from env.applications.score_api import ScoreAPI
from env.applications.csv_export_api import CSVExportAPI, AdminCSVExportAPI
from env.applications.api import WelcomeAPI

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

app.config.update(
    SQLALCHEMY_DATABASE_URI="sqlite:///database.db",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    JWT_SECRET_KEY="super-secret",
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=1),

    CACHE_TYPE="redis",
    CACHE_REDIS_HOST="localhost",
    CACHE_REDIS_PORT=6379,
    CACHE_REDIS_DB=0,
    CACHE_DEFAULT_TIMEOUT=300,
)

db.init_app(app)
cache.init_app(app)
jwt = JWTManager(app)
api = Api(app)
init_celery(app)
jwt_blocklist = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload["jti"] in jwt_blocklist


def add_admin():
    if not User.query.filter_by(role="admin").first():
        admin = User(
            full_name="Admin",
            email="admin@gmail.com",
            password=generate_password_hash("1234"),
            role="admin",
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Quiz Master - V2"}), 200

api.add_resource(WelcomeAPI, "/api/welcome")
api.add_resource(RegisterAPI, "/api/register")
api.add_resource(LoginAPI, "/api/login")
api.add_resource(EditAPI, "/api/editprofile")
api.add_resource(AdminUsersAPI, "/api/admin/users")
api.add_resource(DownloadReportAPI, "/api/reports")
api.add_resource(SubjectAPI, "/api/subjects", "/api/subjects/<int:subject_id>")
api.add_resource(ChapterAPI, "/api/chapters","/api/chapters/<int:chapter_id>", "/api/chapters/subject/<int:subject_id>")
api.add_resource(
    QuizAPI,
    "/api/quizzes",
    "/api/quizzes/<int:quiz_id>",
    "/api/quizzes/chapter/<int:chapter_id>"
)
api.add_resource(
    QuestionAPI,
    "/api/questions",
    "/api/questions/<int:question_id>",
    "/api/questions/quiz/<int:quiz_id>"
)
api.add_resource(QuizAttemptAPI, "/api/quiz/attempt/<int:quiz_id>")
api.add_resource(ScoreAPI, "/api/scores")
api.add_resource(CSVExportAPI, "/api/export/csv")
api.add_resource(AdminCSVExportAPI, "/api/admin/export/csv")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        add_admin()

    app.run(host="0.0.0.0", port=5000, debug=True)