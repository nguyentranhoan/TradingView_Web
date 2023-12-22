from main.ma import ma
from main.models.scapling import ScaplingModel


class ScaplingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ScaplingModel
        # load_only = ("store",)
        dump_only = ("id",)
        # include_fk = True
        load_instance = True
