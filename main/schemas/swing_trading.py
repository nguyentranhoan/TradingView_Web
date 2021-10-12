from main.ma import ma
from main.models.swing_trading import SwingTradingModel


class SwingTradingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SwingTradingModel
        # load_only = ("store",)
        dump_only = ("id",)
        # include_fk = True
        load_instance = True
