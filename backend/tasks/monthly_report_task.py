from celery import shared_task
from env.applications.models import db, User, Quiz, Score
from datetime import datetime, timedelta
import os

REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)


@shared_task(bind=True)
def monthly_activity_report(self):
    """
    Generates monthly activity report for each user (HTML).
    Runs on 1st of every month.
    """

    today = datetime.utcnow()
    first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
    last_day_last_month = today.replace(day=1) - timedelta(days=1)

    users = User.query.filter_by(role="user").all()
    reports_generated = []

    for user in users:
        scores = (
            Score.query
            .filter(
                Score.user_id == user.id,
                Score.attempted_at >= first_day_last_month,
                Score.attempted_at <= last_day_last_month
            )
            .all()
        )

        quizzes_taken = len(scores)
        total_score = sum(s.score for s in scores)
        avg_score = round(total_score / quizzes_taken, 2) if quizzes_taken else 0

        # Basic ranking logic
        all_scores = Score.query.filter(
            Score.attempted_at >= first_day_last_month,
            Score.attempted_at <= last_day_last_month
        ).all()

        user_totals = {}
        for s in all_scores:
            user_totals.setdefault(s.user_id, 0)
            user_totals[s.user_id] += s.score

        sorted_users = sorted(
            user_totals.items(),
            key=lambda x: x[1],
            reverse=True
        )

        rank = next(
            (idx + 1 for idx, (uid, _) in enumerate(sorted_users) if uid == user.id),
            None
        )

        # ---------------- HTML REPORT ----------------
        html_content = f"""
        <html>
        <head>
            <title>Monthly Activity Report</title>
            <style>
                body {{ font-family: Arial; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #333; padding: 8px; text-align: center; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h2>Monthly Activity Report</h2>
            <p><strong>Name:</strong> {user.full_name}</p>
            <p><strong>Email:</strong> {user.email}</p>
            <p><strong>Month:</strong> {first_day_last_month.strftime('%B %Y')}</p>

            <h3>Summary</h3>
            <ul>
                <li>Quizzes Taken: {quizzes_taken}</li>
                <li>Total Score: {total_score}</li>
                <li>Average Score: {avg_score}</li>
                <li>Rank: {rank if rank else 'N/A'}</li>
            </ul>

            <h3>Quiz Details</h3>
            <table>
                <tr>
                    <th>Quiz ID</th>
                    <th>Score</th>
                    <th>Date</th>
                </tr>
        """

        for s in scores:
            html_content += f"""
                <tr>
                    <td>{s.quiz_id}</td>
                    <td>{s.score}</td>
                    <td>{s.attempted_at.strftime('%Y-%m-%d')}</td>
                </tr>
            """

        html_content += """
            </table>
        </body>
        </html>
        """

        filename = f"user_{user.id}_monthly_report.html"
        filepath = os.path.join(REPORT_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Simulated email send (acceptable for demo)
        print(f"[MONTHLY REPORT] Sent report to {user.email} → {filepath}")

        reports_generated.append(user.email)

    return {
        "status": "completed",
        "reports_generated": reports_generated,
        "month": first_day_last_month.strftime("%B %Y")
    }
