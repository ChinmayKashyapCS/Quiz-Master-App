from celery_config import celery
import csv, os
from datetime import datetime

from env.applications.models import db, User, Score, Quiz
from env.utils.email_service import send_email_with_attachment


from flask import Flask


EXPORT_DIR = os.path.join(os.getcwd(), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)


def create_local_app():
    app = Flask(__name__)

    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///database.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)
    return app


@celery.task(name="tasks.csv_tasks.export_user_scores_csv")
def export_user_scores_csv(user_id):

    print(f"[CSV TASK STARTED] {user_id}")

    app = create_local_app()   # 🔥 CREATE APP HERE

    with app.app_context():

        user = User.query.get(user_id)
        scores = Score.query.filter_by(user_id=user_id).all()

        filename = f"user_{user_id}_{int(datetime.utcnow().timestamp())}.csv"
        filepath = os.path.join(EXPORT_DIR, filename)

        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)

            writer.writerow([
                "quiz_id", "chapter_id", "date_of_quiz",
                "score", "remarks", "attempted_at"
            ])

            for s in scores:
                quiz = Quiz.query.get(s.quiz_id)

                writer.writerow([
                    s.quiz_id,
                    quiz.chapter_id if quiz else None,
                    quiz.date_of_quiz.isoformat() if quiz else None,
                    s.score,
                    quiz.remarks if quiz else None,
                    s.attempted_at.isoformat()
                ])

        send_email_with_attachment(
            user.email,
            "Score Card",
            "Your CSV is attached",
            filepath
        )

        print("[EMAIL SENT]")
        return filepath


@celery.task(name="tasks.csv_tasks.export_admin_performance_csv")
def export_admin_performance_csv():

    app = create_local_app()   # 🔥 SAME FIX

    with app.app_context():

        filename = f"admin_report_{int(datetime.utcnow().timestamp())}.csv"
        filepath = os.path.join(EXPORT_DIR, filename)

        users = User.query.filter_by(role="user").all()

        with open(filepath, "w", newline="") as f:

            writer = csv.writer(f)

            writer.writerow([
                "user_id", "name", "email",
                "quizzes_taken", "total_score", "average_score"
            ])

            for user in users:

                scores = Score.query.filter_by(user_id=user.id).all()

                count = len(scores)
                total = sum(s.score for s in scores)
                avg = round(total / count, 2) if count else 0

                writer.writerow([
                    user.id,
                    user.full_name,
                    user.email,
                    count,
                    total,
                    avg
                ])

        print("[ADMIN CSV CREATED]")
        return filepath