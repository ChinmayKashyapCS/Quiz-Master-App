from celery import shared_task
from env.applications.models import db, User, Quiz, Score
from datetime import datetime, timedelta

@shared_task(bind=True)
def daily_reminder_job(self):
    # LOCAL IMPORT: This prevents the circular import error
    from app import app 

    with app.app_context():
        today = datetime.utcnow()
        seven_days_ago = today - timedelta(days=7)

        # Logic remains exactly the same
        users = User.query.filter_by(role="user").all()

        reminders_sent = []

        for user in users:
            scores = Score.query.filter_by(user_id=user.id).all()

            if not scores:
                reminders_sent.append(user.email)
                print(f"[REMINDER] {user.email} → No attempts yet!")
                continue

            last_attempt = max(s.attempted_at for s in scores)
            if last_attempt < seven_days_ago:
                reminders_sent.append(user.email)
                print(f"[REMINDER] {user.email} → Inactive for 7 days!")

        new_quizzes = Quiz.query.filter(
            Quiz.created_at >= today.replace(hour=0, minute=0, second=0)
        ).all()

        if new_quizzes:
            for user in users:
                print(f"[REMINDER] {user.email} → New quizzes available!")

        return {
            "status": "completed",
            "users_notified": reminders_sent,
            "new_quizzes": len(new_quizzes)
        }