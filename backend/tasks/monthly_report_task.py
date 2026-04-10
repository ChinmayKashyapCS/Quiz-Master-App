from celery import shared_task
from env.applications.models import db, User, Quiz, Score
from datetime import datetime, timedelta
import os
from flask import Flask

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt

from env.utils.email_service import send_email_with_pdf


REPORT_DIR = "reports"
GRAPH_DIR = "reports/graphs"

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(GRAPH_DIR, exist_ok=True)


from celery_config import celery

@celery.task(name="tasks.monthly_report_task.monthly_activity_report")
def monthly_activity_report():

    app = create_local_app()   

    with app.app_context():    

        print("[MONTHLY REPORT STARTED]")

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


            quiz_ids = [s.quiz_id for s in scores]
            score_values = [s.score for s in scores]

            graph_path = os.path.join(GRAPH_DIR, f"user_{user.id}_graph.png")

            if score_values:
                plt.figure()
                plt.plot(quiz_ids, score_values, marker='o')
                plt.title("Quiz Performance")
                plt.xlabel("Quiz ID")
                plt.ylabel("Score")
                plt.grid()

                plt.savefig(graph_path)
                plt.close()
            else:
                graph_path = None

            pdf_filename = f"user_{user.id}_monthly_report.pdf"
            pdf_path = os.path.join(REPORT_DIR, pdf_filename)

            doc = SimpleDocTemplate(pdf_path)
            styles = getSampleStyleSheet()

            elements = []

            
            elements.append(Paragraph("Quiz Master Monthly Report", styles['Title']))
            elements.append(Spacer(1, 10))

            
            elements.append(Paragraph(f"Name: {user.full_name}", styles['Normal']))
            elements.append(Paragraph(f"Email: {user.email}", styles['Normal']))
            elements.append(Paragraph(f"Month: {first_day_last_month.strftime('%B %Y')}", styles['Normal']))
            elements.append(Spacer(1, 10))

           
            elements.append(Paragraph("Summary:", styles['Heading2']))
            elements.append(Paragraph(f"Quizzes Taken: {quizzes_taken}", styles['Normal']))
            elements.append(Paragraph(f"Total Score: {total_score}", styles['Normal']))
            elements.append(Paragraph(f"Average Score: {avg_score}", styles['Normal']))
            elements.append(Spacer(1, 10))

           
            table_data = [["Quiz ID", "Score", "Date"]]

            for s in scores:
                table_data.append([
                    str(s.quiz_id),
                    str(s.score),
                    s.attempted_at.strftime("%Y-%m-%d")
                ])

            table = Table(table_data)
            elements.append(table)
            elements.append(Spacer(1, 20))

            # Add Graph Image (if exists)
            if graph_path and os.path.exists(graph_path):
                from reportlab.platypus import Image
                elements.append(Paragraph("Performance Graph:", styles['Heading2']))
                elements.append(Image(graph_path, width=400, height=200))

           
            doc.build(elements)

           
            print(f"[PDF GENERATED] → {pdf_path}")

            
            try:
                send_email_with_pdf(
                    user.email,
                    "Monthly Quiz Report ",
                    f"Hello {user.full_name},\n\n"
                    f"Your monthly performance report is attached.\n\n"
                    f"Keep improving!",
                    pdf_path
                )
                print(f"[PDF EMAIL SENT] → {user.email}")

            except Exception as e:
                print(f"[EMAIL ERROR] → {user.email} → {e}")

            reports_generated.append(user.email)

        return {
            "status": "completed",
            "reports_generated": reports_generated,
            "month": first_day_last_month.strftime("%B %Y")
        }
def create_local_app():
    app = Flask(__name__)

    app.config.update(
        SQLALCHEMY_DATABASE_URI="sqlite:///database.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)
    return app