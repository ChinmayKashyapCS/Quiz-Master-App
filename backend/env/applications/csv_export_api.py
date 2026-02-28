from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_restful import Resource
from kombu.exceptions import OperationalError
from tasks.csv_tasks import export_admin_performance_csv

from tasks.csv_tasks import (
    export_user_scores_csv,
    export_admin_performance_csv
)

class CSVExportAPI(Resource):

    @jwt_required()
    def post(self):
        try:
            task = export_user_scores_csv.delay(int(get_jwt_identity()))
            return {"message": "CSV export started", "task_id": task.id}, 202
        except OperationalError:
            return {"message": "CSV service unavailable"}, 503


class AdminCSVExportAPI(Resource):

    @jwt_required()
    def post(self):
        if get_jwt()["role"] != "admin":
            return {"message": "Admin access required"}, 403

        try:
            task = export_admin_performance_csv.delay()
            return {
                "message": "Admin CSV export started",
                "task_id": task.id
            }, 202

        except OperationalError:
            return {
                "message": "CSV service unavailable"
            }, 503