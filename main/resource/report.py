# ReportCreation Resource
import os
import shutil

from flask_restful import Resource
from main import ROOT_FOLDER, ROOT_REPORT_FOLDER, ROOT_FOLDER_WINDOWS


class ReportCreation(Resource):
    @classmethod
    def get(cls):
        try:
            shutil.copytree(ROOT_FOLDER, ROOT_REPORT_FOLDER, dirs_exist_ok=True)
            os.system(f"start {ROOT_FOLDER_WINDOWS}")
        except:
            return {"message": "Error copy file to report folder"}, 500

        return {"message": "Report files created successfully"}, 200

    # end of file
