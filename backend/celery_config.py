from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "quiz_master",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=[
        "tasks.csv_tasks",
        "tasks.daily_reminder_task",
        "tasks.monthly_report_task",
    ],
)

celery.conf.update(
    broker_url="redis://localhost:6379/0",
    result_backend="redis://localhost:6379/0",

    broker_transport="redis",      # 🔒 FORCE REDIS
    broker_connection_retry_on_startup=True,

    accept_content=["json"],
    task_serializer="json",
    result_serializer="json",

    worker_hijack_root_logger=False,
)


celery.conf.beat_schedule = {
    "daily-reminder-job": {
        "task": "tasks.daily_reminder_task.daily_reminder_job",
        "schedule": crontab(hour=18, minute=0),
    },
    "monthly-activity-report": {
        "task": "tasks.monthly_report_task.monthly_activity_report",
        "schedule": crontab(day_of_month=1, hour=9, minute=0),
    },
}
