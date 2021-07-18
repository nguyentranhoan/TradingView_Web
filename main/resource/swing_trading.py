from flask_restful import Resource
from flask import request, render_template, make_response
# from flask_jwt_extended import jwt_required

from main.logic.swing_trading import SwingTradingService, SwingTradingResponse
from main.models.swing_trading import SwingTradingModel
from main.schemas.swing_trading import SwingTradingSchema

NAME_ALREADY_EXISTS = "An swing_trading with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the swing_trading."
ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted."
ERROR_MAKING_FILE = "An error occurred while writing data to files"

swing_trading_schema = SwingTradingSchema()
swing_trading_list_schema = SwingTradingSchema(many=True)


class RewriteData:
    @classmethod
    def write_to_report(cls):
        try:
            SwingTradingService.write_data()
            SwingTradingService.write_data_by_pair()
        except:
            return {"message": ERROR_MAKING_FILE}, 500


class SwingTradingTransaction(Resource):
    @classmethod
    def post(cls):
        swing_trading_json = request.get_json()
        data = SwingTradingResponse.get_swing_trading_data(swing_trading_json)

        swing_trading = swing_trading_schema.load(data)

        try:
            swing_trading.save_to_db()
            RewriteData.write_to_report()
        except:
            return {"message": ERROR_INSERTING}, 500

        return swing_trading_schema.dump(swing_trading), 201


class SwingTrading(Resource):
    @classmethod
    def get(cls, _id: int):
        swing_trading = SwingTradingModel.find_by_id(_id)
        if swing_trading:
            return swing_trading_schema.dump(swing_trading), 200

        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    # @jwt_required
    def delete(cls, _id: str):
        swing_trading = SwingTradingModel.find_by_id(_id)
        if swing_trading:
            swing_trading.delete_from_db()
            RewriteData.write_to_report()
            return {"message": ITEM_DELETED}, 200

        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    def put(cls, _id: str):
        swing_trading_json = request.get_json()
        swing_trading = SwingTradingModel.find_by_id(_id)

        if swing_trading:
            swing_trading.profit_r = swing_trading_json["newProfitR"]
            swing_trading.comments = swing_trading_json["newComment"]

            swing_trading.save_to_db()
            RewriteData.write_to_report()
            return swing_trading_schema.dump(swing_trading)

        return {"message": ITEM_NOT_FOUND}, 404


class SwingTradingList(Resource):
    @classmethod
    def get(cls):
        return {"swing_trading": swing_trading_list_schema.dump(SwingTradingModel.find_all())}, 200


class SwingTradingPage(Resource):
    @classmethod
    def get(cls):
        return make_response(render_template('swing_trading.html'))


class SwingTradingPairListByMonth(Resource):
    @classmethod
    def get(cls, year: int, month: int, pair: str):
        return swing_trading_list_schema.dump(
            SwingTradingModel.get_transaction_by_pair(year=year, month=month, pair=pair))

    @classmethod
    def delete(cls, year: int, month: int, pair: str):
        swing_trading_list = SwingTradingModel.get_transaction_by_pair(year=year, month=month, pair=pair)
        if swing_trading_list:
            for swing_trading in swing_trading_list:
                swing_trading.delete_from_db()
            RewriteData.write_to_report()
            return {"message": ITEM_DELETED}, 200
        return {"message": ITEM_NOT_FOUND}, 404


class SwingTradingListByMonth(Resource):
    @classmethod
    def get(cls, year: int, month: int):
        pairs = SwingTradingModel.get_distinct_pairs_by_month(year=year, month=month)
        return [pair[0] for pair in pairs]

    @classmethod
    def delete(cls, year: int, month: int):
        swing_trading_list = SwingTradingModel.get_transaction_by_month(year=year, month=month)
        if swing_trading_list:
            for swing_trading in swing_trading_list:
                swing_trading.delete_from_db()
            RewriteData.write_to_report()
            return {"message": ITEM_DELETED}, 200
        return {"message": ITEM_NOT_FOUND}, 404

    # end of file
