from main.ma import ma
from main.models.strategy_4links import Strategy4LinksModel


class Strategy4LinksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Strategy4LinksModel
        # load_only = ("store",)
        dump_only = ("id",)
        # include_fk = True
        load_instance = True
