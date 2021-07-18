from flask_restful import Resource
from flask import request, render_template, make_response
# from flask_jwt_extended import jwt_required

from main.logic.momentum import MomentumService, MomentumResponse
from main.models.momentum import MomentumModel
from main.schemas.momentum import MomentumSchema

NAME_ALREADY_EXISTS = "An momentum with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the momentum."
ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted."
ERROR_MAKING_FILE = "An error occurred while writing data to files"

momentum_schema = MomentumSchema()
momentum_list_schema = MomentumSchema(many=True)


class RewriteData:
    @classmethod
    def write_to_report(cls):
        try:
            MomentumService.write_data()
            MomentumService.write_data_by_pair()
        except:
            return {"message": ERROR_MAKING_FILE}, 500


class MomentumTransaction(Resource):
    @classmethod
    def post(cls):
        momentum_json = request.get_json()
        data = MomentumResponse.get_momentum_data(momentum_json)
        momentum = momentum_schema.load(data)

        try:
            momentum.save_to_db()
            RewriteData.write_to_report()
        except:
            return {"message": ERROR_INSERTING}, 500

        return momentum_schema.dump(momentum), 201


class Momentum(Resource):
    @classmethod
    def get(cls, _id: int):
        momentum = MomentumModel.find_by_id(_id)
        if momentum:
            return momentum_schema.dump(momentum), 200

        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    # @jwt_required
    def delete(cls, _id: str):
        momentum = MomentumModel.find_by_id(_id)
        if momentum:
            momentum.delete_from_db()
            RewriteData.write_to_report()
            return {"message": ITEM_DELETED}, 200

        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    def put(cls, _id: str):
        momentum_json = request.get_json()
        momentum = MomentumModel.find_by_id(_id)

        if momentum:
            momentum.profit_r = momentum_json["newProfitR"]
            momentum.comments = momentum_json["newComment"]

            momentum.save_to_db()
            RewriteData.write_to_report()
            return momentum_schema.dump(momentum)

        return {"message": ITEM_NOT_FOUND}, 404


class MomentumList(Resource):
    @classmethod
    def get(cls):
        return {"momentum": momentum_list_schema.dump(MomentumModel.find_all())}, 200


class MomentumPage(Resource):
    @classmethod
    def get(cls):
        return make_response(render_template('momentum.html'))


class MomentumPairListByMonth(Resource):
    @classmethod
    def get(cls, year: int, month: int, pair: str):
        return momentum_list_schema.dump(MomentumModel.get_transaction_by_pair(year=year, month=month, pair=pair))

    @classmethod
    def delete(cls, year: int, month: int, pair: str):
        momentum_list = MomentumModel.get_transaction_by_pair(year=year, month=month, pair=pair)
        if momentum_list:
            for momentum in momentum_list:
                momentum.delete_from_db()
            RewriteData.write_to_report()
            return {"message": ITEM_DELETED}, 200
        return {"message": ITEM_NOT_FOUND}, 404


class MomentumListByMonth(Resource):
    @classmethod
    def get(cls, year: int, month: int):
        pairs = MomentumModel.get_distinct_pairs_by_month(year=year, month=month)
        return [pair[0] for pair in pairs]

    @classmethod
    def delete(cls, year: int, month: int):
        momentum_list = MomentumModel.get_transaction_by_month(year=year, month=month)
        if momentum_list:
            for momentum in momentum_list:
                momentum.delete_from_db()
            RewriteData.write_to_report()
            return {"message": ITEM_DELETED}, 200
        return {"message": ITEM_NOT_FOUND}, 404

# end of file
