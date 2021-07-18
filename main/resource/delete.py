from flask import render_template, make_response
from flask_restful import Resource


class DeletionPage(Resource):
    @classmethod
    def get(cls):
        return make_response(render_template('delete.html'))

    # end of file
