from main.ma import ma

from main.models.harmonic import HarmonicModel


class HarmonicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HarmonicModel
        # load_only = ("store",)
        dump_only = ("id",)
        # include_fk = True
        load_instance = True
