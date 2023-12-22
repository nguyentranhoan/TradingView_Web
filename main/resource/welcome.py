from flask import render_template, make_response
from flask_restful import Resource
from main.logic.utils import create_folders_if_not_exist


class WelcomePage(Resource):
    @classmethod
    def get(cls):
        create_folders_if_not_exist()
        return make_response(render_template('index.html'))

    # end of file
