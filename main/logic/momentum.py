# MomentumService file

import xlsxwriter

from main import (USER_FILE_NAME,
                  ROOT_FOLDER,
                  ROOT_FOLDER_BY_PAIR)
from main.models.momentum import MomentumModel

STRATEGY_NAME = "momentum/"


class MomentumService:

    @staticmethod
    def decorate_sheet(worksheet_name, merge_start, merge_stop, value, cell_format, row_day):
        worksheet_name.set_column('E:F', 35)
        worksheet_name.set_column('H:H', 30)
        if merge_start == merge_stop:
            worksheet_name.write(f'J{merge_start}', value, cell_format)
        else:
            worksheet_name.merge_range(f'A{merge_start}:A{merge_stop}',
                                       f'{row_day[0]}',
                                       cell_format)
            worksheet_name.merge_range(f'J{merge_start}:J{merge_stop}',
                                       f'=SUM(G{merge_start}:G{merge_stop})',
                                       cell_format)

    @staticmethod
    def format_sheet(workbook_name):
        cell_format = workbook_name.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'})
        return cell_format

    @classmethod
    def write_data(cls):
        yearly_list = cls.get_transaction_by_day()
        print(yearly_list)
        for i in range(len(yearly_list)):
            wbn = ROOT_FOLDER + STRATEGY_NAME + f"[{yearly_list[i]['year']}]" + USER_FILE_NAME
            workbook_name = xlsxwriter.Workbook(filename=wbn)
            cell_format = cls.format_sheet(workbook_name)
            for j in range(len(yearly_list[i]["months"])):
                row_num = 0
                merge_start = 0
                merge_stop = 0
                wsn = f'{yearly_list[i]["months"][j]["month"]}'
                worksheet_name = workbook_name.add_worksheet(name=wsn)
                # call get_row function
                row_names = ['DAY', 'PAIR', 'TIME', 'POSITION',
                             '15MIN CHART', '1HR CHART', 'PROFIT R',
                             'COMMENTS', 'ID', 'SUM']
                worksheet_name.write_row(0, 0, row_names, cell_format)
                for k in range(len(yearly_list[i]["months"][j]["days"])):
                    row_day = [yearly_list[i]["months"][j]["days"][k]["day"], ]
                    worksheet_name.write_row(row_num + 1, 0, row_day, cell_format)
                    value = 0
                    for h in range(len(yearly_list[i]["months"][j]["days"][k]["transactions"])):
                        value += yearly_list[i]["months"][j]["days"][k]["transactions"][h]['PROFIT R']
                        merge_start = row_num + 2 - h
                        merge_stop = row_num + 1 - h + len(yearly_list[i]["months"][j]["days"][k]["transactions"])
                        # function call
                        data = [yearly_list[i]["months"][j]["days"][k]["transactions"][h]['PAIR'],
                                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['TIME'],
                                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['POSITION'],
                                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['15MIN CHART'],
                                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['1HR CHART'],
                                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['PROFIT R'],
                                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['COMMENTS'],
                                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['INDEX']]
                        row_num += 1
                        worksheet_name.write_row(row_num, 1, data, cell_format)
                    # add setting for some rows
                    cls.decorate_sheet(worksheet_name, merge_start,
                                       merge_stop, value, cell_format, row_day)
            workbook_name.close()
            print('done')

    @classmethod
    def write_data_by_pair(cls):
        yearly_list = cls.get_transaction_by_pair()
        print(yearly_list)
        for i in range(len(yearly_list)):
            wbn = ROOT_FOLDER_BY_PAIR + STRATEGY_NAME + f"[{yearly_list[i]['year']}]" + USER_FILE_NAME
            workbook_name = xlsxwriter.Workbook(filename=wbn)
            cell_format = cls.format_sheet(workbook_name)
            for j in range(len(yearly_list[i]["pairs"])):
                row_num = 0
                merge_start = 0
                merge_stop = 0
                wsn = f'{yearly_list[i]["pairs"][j]["pair"]}'
                worksheet_name = workbook_name.add_worksheet(name=wsn)
                # call get_row function
                row_names = ['MONTH', 'DAY', 'TIME', 'POSITION',
                             '15MIN CHART', '1HR CHART', 'PROFIT R',
                             'COMMENTS', 'ID', 'SUM']
                worksheet_name.write_row(0, 0, row_names, cell_format)
                for k in range(len(yearly_list[i]["pairs"][j]["months"])):
                    row_day = [yearly_list[i]["pairs"][j]["months"][k]["month"], ]
                    worksheet_name.write_row(row_num + 1, 0, row_day, cell_format)
                    value = 0
                    for h in range(len(yearly_list[i]["pairs"][j]["months"][k]["transactions"])):
                        value += yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['PROFIT R']
                        merge_start = row_num + 2 - h
                        merge_stop = row_num + 1 - h + len(yearly_list[i]["pairs"][j]["months"][k]["transactions"])
                        # function call
                        data = [yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['DAY'],
                                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['TIME'],
                                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['POSITION'],
                                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['15MIN CHART'],
                                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['1HR CHART'],
                                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['PROFIT R'],
                                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['COMMENTS'],
                                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['INDEX']]
                        row_num += 1
                        worksheet_name.write_row(row_num, 1, data, cell_format)
                    # add setting for some rows
                    cls.decorate_sheet(worksheet_name, merge_start,
                                       merge_stop, value, cell_format, row_day)
            workbook_name.close()
            print('done')

    @staticmethod
    def get_transaction_by_day():
        years = MomentumModel.get_distinct_years()
        yearly_list = []
        for year in years:
            monthly_list = []
            yearly_data = {'year': year[0], 'months': monthly_list}
            months = MomentumModel.get_distinct_months_by_year(year=year[0])
            for month in months:
                daily_list = []
                monthly_data = {'month': month[0], 'days': daily_list}
                monthly_list.append(monthly_data)
                days = MomentumModel.get_distinct_days_by_month(year=year[0], month=month[0])
                for day in days:
                    transaction_list = []
                    daily_data = {'day': day[0], 'transactions': transaction_list}
                    daily_list.append(daily_data)
                    transactions = MomentumModel.get_daily_transaction(year=year[0], month=month[0], day=day[0])
                    for data in transactions:
                        print(data)
                        transaction_data = {"INDEX": data.id,
                                            'TIME': data.time,
                                            'PAIR': data.pair,
                                            'POSITION': data.position,
                                            '15MIN CHART': data.fifteen_min_chart,
                                            '1HR CHART': data.one_hr_chart,
                                            'PROFIT R': data.profit_r,
                                            'COMMENTS': data.comments
                                            }
                        transaction_list.append(transaction_data)
            yearly_list.append(yearly_data)
        return yearly_list

    @staticmethod
    def get_transaction_by_pair():
        years = MomentumModel.get_distinct_years()
        yearly_list = []
        for year in years:
            pair_list = []
            yearly_data = {'year': year[0], 'pairs': pair_list}
            pairs = MomentumModel.get_distinct_pairs_by_year(year=year[0])
            for pair in pairs:
                monthly_list = []
                pair_data = {'pair': pair[0], 'months': monthly_list}
                pair_list.append(pair_data)
                months = MomentumModel.get_distinct_months_by_pair(year=year[0], pair=pair[0])
                for month in months:
                    transaction_list = []
                    monthly_data = {'month': month[0], 'transactions': transaction_list}
                    monthly_list.append(monthly_data)
                    transactions = MomentumModel.get_transaction_by_pair(year=year[0], month=month[0], pair=pair[0])
                    print("transactions:", transactions)
                    for data in transactions:
                        transaction_data = {"INDEX": data.id,
                                            'TIME': data.time,
                                            'DAY': data.day,
                                            'POSITION': data.position,
                                            '15MIN CHART': data.fifteen_min_chart,
                                            '1HR CHART': data.one_hr_chart,
                                            'PROFIT R': data.profit_r,
                                            'COMMENTS': data.comments
                                            }
                        transaction_list.append(transaction_data)
            yearly_list.append(yearly_data)
        return yearly_list

# def get_trans(data: MomentumModel, transaction_list: list):
#     transaction_data = {"INDEX": data.id,
#                         'TIME': data.time,
#                         'PAIR': data.pair,
#                         'POSITION': data.position,
#                         '1HR CHART': data.one_hr_chart,
#                         '15MIN CHART': data.fifteen_min_chart,
#                         'PROFIT R': data.profit_r,
#                         'COMMENTS': data.comments
#                         }
#     transaction_list.append(transaction_data)


# def get_mons(month: tuple, monthly_list: list, year: int, pair: str):
#     transaction_list = []
#     monthly_data = {'month': month[0], 'transactions': transaction_list}
#     monthly_list.append(monthly_data)
#     transactions = MomentumModel.get_transaction_by_pair(year=year, month=month[0], pair=pair[0])
#
#     return transaction_list, monthly_data, transactions
#
#
# def get_pa(pair: tuple, pair_list: list, year: int):
#     monthly_list = []
#     pair_data = {'pair': pair[0], 'months': monthly_list}
#     pair_list.append(pair_data)
#     months = MomentumModel.get_distinct_months_by_pair(year=year[0], pair=pair[0][0])
#
#     return monthly_list, pair_list, months
#
#
# def get_ye(year: tuple):
#     pair_list = []
#     yearly_data = {'year': year[0], 'pairs': pair_list}
#     pairs = MomentumModel.get_distinct_pairs_by_year(year=year[0][0])
#     return pair_list, yearly_data, pairs
#
#
# def test():
#     years = MomentumModel.get_distinct_years()
#     yearly_list = []
#     for year in years:
#         pair_list, yearly_data, pairs = get_ye(year)
#         for pair in pairs:
#             monthly_list, pair_list, months = get_pa(pair, pair_list, year[0])
#             for month in months:
#                 transaction_list, monthly_data, transactions = get_mons(month, monthly_list, year[0], pair[0])
#                 for data in transactions:
#                     transaction_data = {"INDEX": data.id,
#                                         'TIME': data.time,
#                                         'PAIR': data.pair,
#                                         'POSITION': data.position,
#                                         '1HR CHART': data.one_hr_chart,
#                                         '15MIN CHART': data.fifteen_min_chart,
#                                         'PROFIT R': data.profit_r,
#                                         'COMMENTS': data.comments
#                                         }
#                     transaction_list.append(transaction_data)
#         yearly_list.append(yearly_data)
#     return yearly_list

    # end of file
