from main.ma import ma
from main.models.momentum import MomentumModel


class MomentumSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MomentumModel
        # load_only = ("store",)
        dump_only = ("id",)
        # include_fk = True
        load_instance = True
