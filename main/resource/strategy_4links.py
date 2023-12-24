from flask_restful import Resource
from flask import request, render_template, make_response
# from flask_jwt_extended import jwt_required

from main.logic.strategy_4links import Strategy4LinksService, Strategy4LinksResponse
from main.models.strategy_4links import Strategy4LinksModel
from main.schemas.strategy_4links import Strategy4LinksSchema

NAME_ALREADY_EXISTS = "An strategy_4links with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the strategy_4links."
ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted."
ERROR_MAKING_FILE = "An error occurred while writing data to files"

strategy_4links_schema = Strategy4LinksSchema()
strategy_4links_list_schema = Strategy4LinksSchema(many=True)


class RewriteData:
    @classmethod
    def write_to_report(cls, strategy: str):
        try:
            Strategy4LinksService.write_data(strategy)
            Strategy4LinksService.write_data_by_pair(strategy)
        except Exception as e:
            return {"message": ERROR_MAKING_FILE}, e, 500


class Strategy4LinksTransaction(Resource):
    @classmethod
    def post(cls, strategy: str):
        strategy_4links_json = request.get_json()
        data = Strategy4LinksResponse.get_strategy_4links_data(strategy, 
            strategy_4links_json)
        strategy_4links = strategy_4links_schema.load(data)
        try:
            strategy_4links.save_to_db()
            RewriteData.write_to_report(strategy)
            pass
        except Exception as e:
            return {"message": ERROR_INSERTING}, e, 500

        return strategy_4links_schema.dump(strategy_4links), 201


class Strategy4Links(Resource):
    @classmethod
    def get(cls, strategy: str, _id: int):
        strategy_4links = Strategy4LinksModel.find_by_id(_id, strategy)
        if strategy_4links:
            return strategy_4links_schema.dump(strategy_4links), 200

        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    # @jwt_required
    def delete(cls, strategy: str, _id: str):
        strategy_4links = Strategy4LinksModel.find_by_id(_id, strategy)
        if strategy_4links:
            strategy_4links.delete_from_db()
            RewriteData.write_to_report(strategy)
            return {"message": ITEM_DELETED}, 200

        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    def put(cls, strategy: str, _id: str):
        strategy_4links_json = request.get_json()
        strategy_4links = Strategy4LinksModel.find_by_id(_id, strategy)

        if strategy_4links:
            strategy_4links.profit_r = strategy_4links_json["newProfitR"]
            strategy_4links.comments = strategy_4links_json["newComment"]
            strategy_4links.pair = strategy_4links_json["newPair"]

            strategy_4links.save_to_db()
            RewriteData.write_to_report(strategy)
            return strategy_4links_schema.dump(strategy_4links)

        return {"message": ITEM_NOT_FOUND}, 404


class Strategy4LinksList(Resource):
    @classmethod
    def get(cls, strategy: str):
        return {"strategy_4links": strategy_4links_list_schema.dump(Strategy4LinksModel.find_all(strategy=strategy))}, 200


class Strategy4LinksPage(Resource):
    @classmethod
    def get(cls):
        return make_response(render_template('strategy_4links.html'))


class Strategy4LinksPairListByMonth(Resource):
    @classmethod
    def get(cls, strategy: str, year: int, month: int, pair: str):
        return strategy_4links_list_schema.dump(
            Strategy4LinksModel.get_transaction_by_pair(strategy=strategy, year=year, month=month, pair=pair))

    @classmethod
    def delete(cls, strategy: str, year: int, month: int, pair: str):
        strategy_4links_list = Strategy4LinksModel.get_transaction_by_pair(
            strategy=strategy, year=year, month=month, pair=pair)
        if strategy_4links_list:
            for strategy_4links in strategy_4links_list:
                strategy_4links.delete_from_db()
            RewriteData.write_to_report(strategy)
            return {"message": ITEM_DELETED}, 200
        return {"message": ITEM_NOT_FOUND}, 404


class Strategy4LinksListByMonth(Resource):
    @classmethod
    def get(cls, strategy: str, year: int, month: int):
        pairs = Strategy4LinksModel.get_distinct_pairs_by_month(
            strategy=strategy, year=year, month=month)
        return [pair[0] for pair in pairs]

    @classmethod
    def delete(cls, strategy: str, year: int, month: int):
        strategy_4links_list = Strategy4LinksModel.get_transaction_by_month(
            strategy=strategy, year=year, month=month)
        if strategy_4links_list:
            for strategy_4links in strategy_4links_list:
                strategy_4links.delete_from_db()
            RewriteData.write_to_report(strategy)
            return {"message": ITEM_DELETED}, 200
        return {"message": ITEM_NOT_FOUND}, 404

    # end of file
