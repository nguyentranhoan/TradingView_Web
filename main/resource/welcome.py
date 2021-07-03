from flask import render_template, make_response
from flask_restful import Resource


class WelcomePage(Resource):
    @classmethod
    def get(cls):
        return make_response(render_template('index.html'))

    # end of file
