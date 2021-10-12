from flask import render_template, make_response
from flask_restful import Resource


class UpdatePage(Resource):
    @classmethod
    def get(cls):
        return make_response(render_template('update.html'))

    # end of file
