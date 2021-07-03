# Transaction.py

from flask_restful.representations import json

from main.logic.image_to_text import ImageToText
from main.response.harmonic import Harmonic
from main.response.momentum import Momentum
from main.response.swing_trading import SwingTrading


class Transaction:

    @staticmethod
    def alter_comment(comment):
        for i in comment:
            if i == '=' or i == '-':
                comment = "'" + comment
                break
        comment = comment.replace("'", "''")
        comment = comment.replace('"', '""')
        return comment

    @staticmethod
    def get_chosen_ratio(data, transaction_ratio):
        if int(data['profitR']) == -1:
            value = -1
            return value
        elif int(data["profitR"]) == 0:
            value = 0
            return value
        else:
            value = transaction_ratio
            return value

    @classmethod
    def get_momentum_data(cls, data: json):
        transaction_datetime, transaction_ratio, transaction_position, transaction_pair = ImageToText.get_data(
            'momentum')
        chosen_data_ratio = cls.get_chosen_ratio(data, transaction_ratio)
        time = f"{transaction_datetime.hour}:{transaction_datetime.minute}"
        comment = cls.alter_comment(data['comment'])
        data = Momentum(datetime=f"{transaction_datetime}",
                        year=transaction_datetime.year,
                        month=transaction_datetime.month,
                        day=transaction_datetime.day,
                        time=time,
                        pair=transaction_pair,
                        position=transaction_position,
                        fifteen_min_chart=data['link15Mins'],
                        one_hr_chart=data['link1Hour'],
                        profit_r=chosen_data_ratio,
                        comments=comment)

        keys = ['datetime', 'year',
                'month', 'day',
                'time', 'pair',
                'position', 'fifteen_min_chart',
                'one_hr_chart', 'profit_r',
                'comments']

        values = [data.datetime, data.year,
                  data.month, data.day,
                  data.time, data.pair,
                  data.position, data.fifteen_min_chart,
                  data.one_hr_chart, data.profit_r,
                  data.comments]

        return dict(zip(keys, values))

    @classmethod
    def get_harmonic_data(cls, data: json):
        transaction_datetime, transaction_ratio, transaction_position, transaction_pair = ImageToText.get_data(
            'harmonic')
        chosen_data_ratio = cls.get_chosen_ratio(data, transaction_ratio)
        time = f"{transaction_datetime.hour}:{transaction_datetime.minute}"
        comment = cls.alter_comment(data['comment'])
        data = Harmonic(datetime=f"{transaction_datetime}",
                        year=transaction_datetime.year,
                        month=transaction_datetime.month,
                        day=transaction_datetime.day,
                        time=time,
                        pair=transaction_pair,
                        position=transaction_position,
                        one_hr_chart=data['link1Hour'],
                        one_day_chart=data['link1Day'],
                        profit_r=chosen_data_ratio,
                        comments=comment)

        keys = ['datetime', 'year',
                'month', 'day',
                'time', 'pair',
                'position', 'one_hr_chart',
                'one_day_chart', 'profit_r',
                'comments']

        values = [data.datetime, data.year,
                  data.month, data.day,
                  data.time, data.pair,
                  data.position, data.one_hr_chart,
                  data.one_day_chart, data.profit_r,
                  data.comments]

        return dict(zip(keys, values))

    @classmethod
    def get_swing_trading_data(cls, data: json):
        transaction_datetime, transaction_ratio, transaction_position, transaction_pair = ImageToText.get_data(
            'swing_trading')
        chosen_data_ratio = cls.get_chosen_ratio(data, transaction_ratio)
        time = f"{transaction_datetime.hour}:{transaction_datetime.minute}"
        comment = cls.alter_comment(data['comment'])
        data = SwingTrading(datetime=f"{transaction_datetime}",
                            year=transaction_datetime.year,
                            month=transaction_datetime.month,
                            day=transaction_datetime.day,
                            time=time,
                            pair=transaction_pair,
                            position=transaction_position,
                            four_hr_chart=data['link4Hours'],
                            pre_four_hr_chart=data['linkPre4Hours'],
                            one_day_chart=data['link1Day'],
                            one_week_chart=data['link1Week'],
                            one_month_chart=data['link1Month'],
                            profit_r=chosen_data_ratio,
                            comments=comment)

        keys = ['datetime', 'year',
                'month', 'day',
                'time', 'pair',
                'position', 'four_hr_chart',
                'pre_four_hr_chart', 'one_day_chart',
                'one_week_chart', 'one_month_chart',
                'profit_r', 'comments']

        values = [data.datetime, data.year,
                  data.month, data.day,
                  data.time, data.pair,
                  data.position, data.four_hr_chart,
                  data.pre_four_hr_chart, data.one_day_chart,
                  data.one_week_chart, data.one_month_chart,
                  data.profit_r, data.comments]

        return dict(zip(keys, values))

    # end of file
