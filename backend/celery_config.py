from celery import Celery
from celery.schedules import crontab
celery = Celery(
    "quiz_master",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.imports = (
    "tasks.csv_tasks",
    "tasks.daily_reminder_task",
    "tasks.monthly_report_task",
)

def init_celery(app):

    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = ContextTask



celery.conf.beat_schedule = {

    "daily-reminder": {
        "task": "tasks.daily_reminder_task.daily_reminder_job",
        "schedule": crontab(minute="*/1"),
    },

    "monthly-report": {
        "task": "tasks.monthly_report_task.monthly_activity_report",
        "schedule": crontab(minute="*/1"),
    },
}