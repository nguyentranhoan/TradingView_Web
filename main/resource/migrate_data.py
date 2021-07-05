from flask_restful import Resource
import pandas as pd
from datetime import datetime

from main.logic.momentum import MomentumService
from main.schemas.momentum import MomentumSchema
from main.response.momentum import Momentum

momentum_schema = MomentumSchema()


class MigrateData(Resource):
    @classmethod
    def get(cls):
        df = pd.read_csv('main/.data/momentum.csv')
        keys = ['datetime', 'year',
                'month', 'day',
                'time', 'pair',
                'position', 'fifteen_min_chart',
                'one_hr_chart', 'profit_r',
                'comments']
        for i in range(len(df)):
            _str = f"{df['day'][i]} {df['month'][i]} {df['year'][i]} {df['time'][i]}"
            desired_datetime = datetime.strptime(_str, '%d %m %Y %H:%M')
            data = Momentum(datetime=f"{desired_datetime}",
                            year=desired_datetime.year,
                            month=desired_datetime.month,
                            day=desired_datetime.day,
                            time=f"{desired_datetime.time()}",
                            pair=df['pair'][i],
                            position=df["position"][i],
                            fifteen_min_chart=df['fifteen_min_chart'][i],
                            one_hr_chart=df['one_hr_chart'][i],
                            profit_r=df['profit_r'][i],
                            comments=f"{df['comments'][i]}")

            values = [data.datetime, data.year,
                      data.month, data.day,
                      data.time, data.pair,
                      data.position, data.fifteen_min_chart,
                      data.one_hr_chart, data.profit_r,
                      data.comments]

            momentum = momentum_schema.load(dict(zip(keys, values)))

            try:
                momentum.save_to_db()
            except:
                return {"message": "ERROR_INSERTING"}, 500


class WriteData(Resource):
    @classmethod
    def get(cls):
        try:
            MomentumService.write_data()
            MomentumService.write_data_by_pair()
        except:
            return {"message": "ERROR_MAKING_FILE"}, 500