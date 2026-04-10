from celery_config import celery
from env.applications.models import db, User, Quiz, Score
from datetime import datetime
from flask import Flask
import os

from env.utils.email_service import send_email

REMINDER_DIR = "reports/daily_reminders"
os.makedirs(REMINDER_DIR, exist_ok=True)


def create_local_app():
    app = Flask(__name__)
    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///database.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    db.init_app(app)
    return app


@celery.task(name="tasks.daily_reminder_task.daily_reminder_job")
def daily_reminder_job():

    app = create_local_app()

    with app.app_context():

        print("[DAILY REMINDER STARTED]")

        users = User.query.filter_by(role="user").all()
        quizzes = Quiz.query.all()

        today = datetime.utcnow()

        for user in users:

            scores = Score.query.filter_by(user_id=user.id).all()
            attempted_ids = [s.quiz_id for s in scores]

            unattempted = [q for q in quizzes if q.id not in attempted_ids]

            filename = f"user_{user.id}_{int(today.timestamp())}.txt"
            filepath = os.path.join(REMINDER_DIR, filename)

            with open(filepath, "w") as f:

                f.write(f"User: {user.full_name}\n")
                f.write(f"Date: {today}\n\n")

                if not unattempted:
                    f.write("All quizzes attempted\n")
                else:
                    f.write("Unattempted Quizzes:\n")

                    for q in unattempted:
                        f.write(f"- Quiz ID: {q.id}\n")

            print(f"[REMINDER FILE CREATED] → {filepath}")

            # 🔥 EMAIL ADDED
            try:
                send_email(
                    user.email,
                    "Daily Reminder ",
                    f"Hello {user.full_name},\n\n"
                    f"You have {len(unattempted)} unattempted quizzes.\n"
                    f"Please check the attached report or login to attempt them."
                )
                print(f"[EMAIL SENT] → {user.email}")
            except Exception as e:
                print(f"[EMAIL ERROR] → {user.email} → {e}")

        return {"status": "done"}