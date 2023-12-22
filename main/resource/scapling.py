from flask_restful import Resource
from flask import request, render_template, make_response
# from flask_jwt_extended import jwt_required

from main.logic.scapling import ScaplingService, ScaplingResponse
from main.models.scapling import ScaplingModel
from main.schemas.scapling import ScaplingSchema

NAME_ALREADY_EXISTS = "An scapling with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the scapling."
ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted."
ERROR_MAKING_FILE = "An error occurred while writing data to files"

scapling_schema = ScaplingSchema()
scapling_list_schema = ScaplingSchema(many=True)


class RewriteData:
    @classmethod
    def write_to_report(cls):
        try:
            ScaplingService.write_data()
            ScaplingService.write_data_by_pair()
        except Exception as e:
            return {"message": ERROR_MAKING_FILE}, e, 500


class ScaplingTransaction(Resource):
    @classmethod
    def post(cls):
        scapling_json = request.get_json()
        data = ScaplingResponse.get_scapling_data(scapling_json)
        scapling = scapling_schema.load(data)
        try:
            scapling.save_to_db()
            RewriteData.write_to_report()
        except Exception as e:
            return {"message": ERROR_INSERTING}, e, 500

        return scapling_schema.dump(scapling), 201


class Scapling(Resource):
    @classmethod
    def get(cls, _id: int):
        scapling = ScaplingModel.find_by_id(_id)
        if scapling:
            return scapling_schema.dump(scapling), 200

        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    # @jwt_required
    def delete(cls, _id: str):
        scapling = ScaplingModel.find_by_id(_id)
        if scapling:
            scapling.delete_from_db()
            RewriteData.write_to_report()
            return {"message": ITEM_DELETED}, 200

        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    def put(cls, _id: str):
        scapling_json = request.get_json()
        scapling = ScaplingModel.find_by_id(_id)

        if scapling:
            scapling.profit_r = scapling_json["newProfitR"]
            scapling.comments = scapling_json["newComment"]
            scapling.pair = scapling_json["newPair"]

            scapling.save_to_db()
            RewriteData.write_to_report()
            return scapling_schema.dump(scapling)

        return {"message": ITEM_NOT_FOUND}, 404


class ScaplingList(Resource):
    @classmethod
    def get(cls):
        return {"scapling": scapling_list_schema.dump(ScaplingModel.find_all())}, 200


class ScaplingPage(Resource):
    @classmethod
    def get(cls):
        return make_response(render_template('scapling.html'))


class ScaplingPairListByMonth(Resource):
    @classmethod
    def get(cls, year: int, month: int, pair: str):
        return scapling_list_schema.dump(ScaplingModel.get_transaction_by_pair(year=year, month=month, pair=pair))

    @classmethod
    def delete(cls, year: int, month: int, pair: str):
        scapling_list = ScaplingModel.get_transaction_by_pair(
            year=year, month=month, pair=pair)
        if scapling_list:
            for scapling in scapling_list:
                scapling.delete_from_db()
            RewriteData.write_to_report()
            return {"message": ITEM_DELETED}, 200
        return {"message": ITEM_NOT_FOUND}, 404


class ScaplingListByMonth(Resource):
    @classmethod
    def get(cls, year: int, month: int):
        pairs = ScaplingModel.get_distinct_pairs_by_month(
            year=year, month=month)
        return [pair[0] for pair in pairs]

    @classmethod
    def delete(cls, year: int, month: int):
        scapling_list = ScaplingModel.get_transaction_by_month(
            year=year, month=month)
        if scapling_list:
            for scapling in scapling_list:
                scapling.delete_from_db()
            RewriteData.write_to_report()
            return {"message": ITEM_DELETED}, 200
        return {"message": ITEM_NOT_FOUND}, 404

# end of file
