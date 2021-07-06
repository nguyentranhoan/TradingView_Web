import os

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api
from marshmallow import ValidationError

from main.db import db
from main.ma import ma
from main.resource.harmonic import Harmonic, HarmonicPage, HarmonicTransaction
from main.resource.momentum import Momentum, MomentumPage, MomentumTransaction
from main.resource.report import ReportCreation
from main.resource.swing_trading import SwingTrading, SwingTradingPage, SwingTradingTransaction
from main.resource.transaction_screenshot import TransactionScreenshot
from main.resource.update import UpdatePage
from main.resource.welcome import WelcomePage
#from main.resource.migrate_data import MigrateData, WriteData

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]  # allow blacklisting for access and refresh tokens
app.secret_key = os.environ.get(
    "APP_SECRET_KEY"
)  # could do app.config['JWT_SECRET_KEY'] if we prefer
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)

api.add_resource(WelcomePage, "/")
api.add_resource(UpdatePage, "/update")
api.add_resource(MomentumPage, "/momentum")
api.add_resource(Momentum, "/momentum/<int:_id>")  # search, update, delete
api.add_resource(MomentumTransaction, "/momentum/submit")  # add new
api.add_resource(HarmonicPage, "/harmonic")
api.add_resource(Harmonic, "/harmonic/<int:_id>")
api.add_resource(HarmonicTransaction, "/harmonic/submit")
api.add_resource(SwingTradingPage, "/swing_trading")
api.add_resource(SwingTrading, "/swing_trading/<int:_id>")
api.add_resource(SwingTradingTransaction, "/swing_trading/submit")
api.add_resource(TransactionScreenshot, "/screenshot/<string:strategy_name>")
api.add_resource(ReportCreation, '/report')
#api.add_resource(MigrateData, '/migrate')
#api.add_resource(WriteData, '/write_data')

db.init_app(app)

if __name__ == "__main__":

    ma.init_app(app)
    app.run(port=5000, debug=True)

    # end of file
