from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
import os

REPORT_DIR = "reports"


class DownloadReportAPI(Resource):

    @jwt_required()
    def get(self):

        user_id = int(get_jwt_identity())

        user_files = []

        for root, dirs, files in os.walk(REPORT_DIR):
            for file in files:
                if f"user_{user_id}_" in file:
                    user_files.append(file)

        return {
            "files": user_files
        }, 200