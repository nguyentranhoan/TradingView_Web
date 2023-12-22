# ReportCreation Resource
import os
import shutil
import platform
from flask_restful import Resource
from main import ROOT_FOLDER, ROOT_REPORT_FOLDER, ROOT_FOLDER_WINDOWS


class ReportCreation(Resource):
    @classmethod
    def get(cls):
        try:
            shutil.copytree(ROOT_FOLDER, ROOT_REPORT_FOLDER,
                            dirs_exist_ok=True)
            if platform.system() != "Windows":
                os.system(f"open {ROOT_REPORT_FOLDER[:-1]}")
            else:
                os.system(f"start {ROOT_FOLDER_WINDOWS}")
        except Exception as e:
            return {"message": "Error copy file to report folder"}, e, 500

        return {"message": "Report files created successfully"}, 200

    # end of file
