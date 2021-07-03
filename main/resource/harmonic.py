from flask_restful import Resource
from flask import request, render_template, make_response
from flask_jwt_extended import jwt_required

from main.logic.transaction import Transaction
from main.logic.harmonic import HarmonicService
from main.models.harmonic import HarmonicModel
from main.schemas.harmonic import HarmonicSchema


NAME_ALREADY_EXISTS = "An harmonic with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the harmonic."
ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted."
ERROR_MAKING_FILE = "An error occurred while writing data to files"

harmonic_schema = HarmonicSchema()
harmonic_list_schema = HarmonicSchema(many=True)


class HarmonicTransaction(Resource):
    @classmethod
    def post(cls):
        harmonic_json = request.get_json()
        data = Transaction.get_harmonic_data(harmonic_json)

        harmonic = harmonic_schema.load(data)

        try:
            harmonic.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500
        try:
            HarmonicService.write_data()
            HarmonicService.write_data_by_pair()
        except:
            return {"message": ERROR_MAKING_FILE}, 500

        return harmonic_schema.dump(harmonic), 201


class Harmonic(Resource):
    @classmethod
    def get(cls, _id: int):
        harmonic = HarmonicModel.find_by_id(_id)
        if harmonic:
            return harmonic_schema.dump(harmonic), 200

        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    # @jwt_required
    def delete(cls, _id: str):
        harmonic = HarmonicModel.find_by_id(_id)
        if harmonic:
            harmonic.delete_from_db()
            return {"message": ITEM_DELETED}, 200

        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    def put(cls, _id: str):
        harmonic_json = request.get_json()
        harmonic = HarmonicModel.find_by_id(_id)

        if harmonic:
            harmonic.profit_r = harmonic_json["newProfitR"]
            harmonic.comments = harmonic_json["newComment"]

            harmonic.save_to_db()
            return harmonic_schema.dump(harmonic)

        return {"message": ITEM_NOT_FOUND}, 404


class HarmonicList(Resource):
    @classmethod
    def get(cls):
        return {"harmonic": harmonic_list_schema.dump(HarmonicModel.find_all())}, 200


class HarmonicPage(Resource):
    @classmethod
    def get(cls):
        return make_response(render_template('harmonic.html'))

    # end of file
