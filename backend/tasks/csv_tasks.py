import csv
import os
from datetime import datetime

from celery_config import celery
from env.applications.models import Score, Quiz, User

EXPORT_DIR = os.path.join(os.getcwd(), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)


@celery.task(name="tasks.csv_tasks.export_user_scores_csv")
def export_user_scores_csv(user_id):
    filename = f"user_{user_id}_{int(datetime.utcnow().timestamp())}.csv"
    filepath = os.path.join(EXPORT_DIR, filename)

    scores = Score.query.filter_by(user_id=user_id).all()

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["quiz_id", "chapter_id", "score", "attempted_at"])
        for s in scores:
            quiz = Quiz.query.get(s.quiz_id)
            writer.writerow([
                s.quiz_id,
                quiz.chapter_id if quiz else None,
                s.score,
                s.attempted_at.isoformat()
            ])
    return filepath


@celery.task(name="tasks.csv_tasks.export_admin_performance_csv")
def export_admin_performance_csv():
    filename = f"admin_report_{int(datetime.utcnow().timestamp())}.csv"
    filepath = os.path.join(EXPORT_DIR, filename)

    users = User.query.filter_by(role="user").all()

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "name", "quizzes_taken", "average_score"])
        for user in users:
            scores = Score.query.filter_by(user_id=user.id).all()
            count = len(scores)
            avg = round(sum(s.score for s in scores) / count, 2) if count else 0
            writer.writerow([user.id, user.full_name, count, avg])

    return filepath
