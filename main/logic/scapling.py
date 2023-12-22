# ScaplingService file
import xlsxwriter
from flask_restful.representations import json

from main import USER_FILE_NAME, ROOT_FOLDER, ROOT_FOLDER_BY_PAIR
from main.logic.image_to_text import ImageToText
from main.logic.utils import ExcelFormat, CommentExtraction, ProfitRatio
from main.models.scapling import ScaplingModel
from main.response.scapling import Scapling

STRATEGY_NAME = "scapling/"


class ScaplingService:

    @classmethod
    def write_data(cls):
        yearly_list = cls.get_transaction_by_day()
        for i in range(len(yearly_list)):
            wbn = ROOT_FOLDER + STRATEGY_NAME + \
                f"[{yearly_list[i]['year']}]" + USER_FILE_NAME
            workbook_name = xlsxwriter.Workbook(filename=wbn)
            cell_format = ExcelFormat.format_sheet(workbook_name)
            for j in range(len(yearly_list[i]["months"])):

                row_num = 0
                merge_start = 0
                merge_stop = 0
                wsn = f'{yearly_list[i]["months"][j]["month"]}'
                worksheet_name = workbook_name.add_worksheet(name=wsn)
                # call get_row function
                row_names = ['DAY', 'PAIR', 'TIME', 'POSITION',
                             '15MIN CHART', 'PROFIT R',
                             'COMMENTS', "PRIORITY", 'ID', 'SUM']
                worksheet_name.write_row(0, 0, row_names, cell_format)
                for k in range(len(yearly_list[i]["months"][j]["days"])):

                    row_day = [yearly_list[i]["months"][j]["days"][k]["day"], ]
                    worksheet_name.write_row(
                        row_num + 1, 0, row_day, cell_format)
                    value = 0
                    for h in range(len(yearly_list[i]["months"][j]["days"][k]["transactions"])):

                        value += yearly_list[i]["months"][j]["days"][k]["transactions"][h]['PROFIT R']
                        merge_start = row_num + 2 - h
                        merge_stop = row_num + 1 - h + \
                            len(yearly_list[i]["months"][j]
                                ["days"][k]["transactions"])
                        # function call
                        comments = yearly_list[i]["months"][j]["days"][k]["transactions"][h]['COMMENTS']
                        comment, priority = CommentExtraction.get_comment(
                            comments)
                        comment = CommentExtraction.alter_comment(comment)
                        data = [yearly_list[i]["months"][j]["days"][k]["transactions"][h]['PAIR'],
                                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['TIME'],
                                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['POSITION'],
                                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['15MIN CHART'],
                                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['PROFIT R'],
                                # yearly_list[i]["months"][j]["days"][k]["transactions"][h]['COMMENTS'],
                                comment,
                                priority,
                                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['INDEX']]
                        row_num += 1
                        worksheet_name.write_row(row_num, 1, data, cell_format)
                    # add setting for some rows
                    ExcelFormat.decorate_sheet_scapling(worksheet_name, merge_start,
                                                        merge_stop, value, cell_format, row_day)
            workbook_name.close()

    @classmethod
    def write_data_by_pair(cls):
        yearly_list = cls.get_transaction_by_pair()
        for i in range(len(yearly_list)):
            wbn = ROOT_FOLDER_BY_PAIR + STRATEGY_NAME + \
                f"[{yearly_list[i]['year']}]" + USER_FILE_NAME
            workbook_name = xlsxwriter.Workbook(filename=wbn)
            cell_format = ExcelFormat.format_sheet(workbook_name)
            for j in range(len(yearly_list[i]["pairs"])):
                row_num = 0
                merge_start = 0
                merge_stop = 0
                wsn = f'{yearly_list[i]["pairs"][j]["pair"]}'
                worksheet_name = workbook_name.add_worksheet(name=wsn)
                # call get_row function
                row_names = ['MONTH', 'DAY', 'TIME', 'POSITION',
                             '15MIN CHART', 'PROFIT R',
                             'COMMENTS', "PRIORITY", 'ID', 'SUM']
                worksheet_name.write_row(0, 0, row_names, cell_format)
                for k in range(len(yearly_list[i]["pairs"][j]["months"])):
                    row_day = [yearly_list[i]["pairs"]
                               [j]["months"][k]["month"], ]
                    worksheet_name.write_row(
                        row_num + 1, 0, row_day, cell_format)
                    value = 0
                    for h in range(len(yearly_list[i]["pairs"][j]["months"][k]["transactions"])):
                        value += yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['PROFIT R']
                        merge_start = row_num + 2 - h
                        merge_stop = row_num + 1 - h + \
                            len(yearly_list[i]["pairs"][j]
                                ["months"][k]["transactions"])
                        # function call
                        comments = yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['COMMENTS']
                        comment, priority = CommentExtraction.get_comment(
                            comments)
                        comment = CommentExtraction.alter_comment(comment)
                        data = [yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['DAY'],
                                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['TIME'],
                                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['POSITION'],
                                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['15MIN CHART'],
                                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['PROFIT R'],
                                # yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['COMMENTS'],
                                comment,
                                priority,
                                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['INDEX']]
                        row_num += 1
                        worksheet_name.write_row(row_num, 1, data, cell_format)
                    # add setting for some rows
                    ExcelFormat.decorate_sheet_scapling(worksheet_name, merge_start,
                                                        merge_stop, value, cell_format, row_day)
            workbook_name.close()

    @staticmethod
    def get_transaction_by_day():
        years = ScaplingModel.get_distinct_years()
        yearly_list = []
        for year in years:
            monthly_list = []
            yearly_data = {'year': year[0], 'months': monthly_list}
            months = ScaplingModel.get_distinct_months_by_year(year=year[0])
            for month in months:
                daily_list = []
                monthly_data = {'month': month[0], 'days': daily_list}
                monthly_list.append(monthly_data)
                days = ScaplingModel.get_distinct_days_by_month(
                    year=year[0], month=month[0])
                for day in days:
                    transaction_list = []
                    daily_data = {'day': day[0],
                                  'transactions': transaction_list}
                    daily_list.append(daily_data)
                    transactions = ScaplingModel.get_daily_transaction(
                        year=year[0], month=month[0], day=day[0])
                    for data in transactions:
                        transaction_data = {"INDEX": data.id,
                                            'TIME': data.time,
                                            'PAIR': data.pair,
                                            'POSITION': data.position,
                                            '15MIN CHART': data.fifteen_min_chart,
                                            'PROFIT R': data.profit_r,
                                            'COMMENTS': data.comments
                                            }
                        transaction_list.append(transaction_data)
            yearly_list.append(yearly_data)
        return yearly_list

    @staticmethod
    def get_transaction_by_pair():
        years = ScaplingModel.get_distinct_years()
        yearly_list = []
        for year in years:
            pair_list = []
            yearly_data = {'year': year[0], 'pairs': pair_list}
            pairs = ScaplingModel.get_distinct_pairs_by_year(year=year[0])
            for pair in pairs:
                monthly_list = []
                pair_data = {'pair': pair[0], 'months': monthly_list}
                pair_list.append(pair_data)
                months = ScaplingModel.get_distinct_months_by_pair(
                    year=year[0], pair=pair[0])
                for month in months:
                    transaction_list = []
                    monthly_data = {
                        'month': month[0], 'transactions': transaction_list}
                    monthly_list.append(monthly_data)
                    transactions = ScaplingModel.get_transaction_by_pair(
                        year=year[0], month=month[0], pair=pair[0])
                    for data in transactions:
                        transaction_data = {"INDEX": data.id,
                                            'TIME': data.time,
                                            'DAY': data.day,
                                            'POSITION': data.position,
                                            '15MIN CHART': data.fifteen_min_chart,
                                            'PROFIT R': data.profit_r,
                                            'COMMENTS': data.comments
                                            }
                        transaction_list.append(transaction_data)
            yearly_list.append(yearly_data)
        return yearly_list


class ScaplingResponse:
    @classmethod
    def get_scapling_data(cls, data: json):
        transaction_datetime, transaction_ratio, transaction_position, transaction_pair = ImageToText.get_data(
            'scapling')
        chosen_data_ratio = ProfitRatio.get_chosen_ratio(
            data, transaction_ratio)
        time = f"{transaction_datetime.hour}:{transaction_datetime.minute}"
        data = Scapling(datetime=f"{transaction_datetime}",
                        year=transaction_datetime.year,
                        month=transaction_datetime.month,
                        day=transaction_datetime.day,
                        time=time,
                        pair=transaction_pair,
                        position=transaction_position,
                        fifteen_min_chart=data['link15Mins'],
                        profit_r=chosen_data_ratio,
                        comments=data['comment'])

        keys = ['datetime', 'year',
                'month', 'day',
                'time', 'pair',
                'position', 'fifteen_min_chart',
                'profit_r',
                'comments']

        values = [data.datetime, data.year,
                  data.month, data.day,
                  data.time, data.pair,
                  data.position, data.fifteen_min_chart,
                  data.profit_r,
                  data.comments]

        return dict(zip(keys, values))

# end of file
