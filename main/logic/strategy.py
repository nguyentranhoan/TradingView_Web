import os
import shutil

import xlsxwriter

from main.logic.from_db import store_data_db


def submit_strategy(conn, strategy_name, data):
    store_data_db(conn, strategy_name, data)
    write_data(conn, strategy_name)
    create_report(strategy_name)


def update_report_after_alter_data(conn, strategy_name):
    write_data(conn, strategy_name)
    create_report(strategy_name)


def write_data(conn, strategy_name):
    yearly_list = get_strategy_data_from_db(conn=conn, strategy_name=strategy_name)
    print(yearly_list)
    for i in range(len(yearly_list)):
        wbn = f"main/.data/{strategy_name}/[{yearly_list[i]['year']}]" + "[HuyNguyen]-TradingView" + ".xlsx"
        workbook_name = xlsxwriter.Workbook(filename=wbn)
        cell_format = workbook_name.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'})
        for j in range(len(yearly_list[i]["months"])):
            row_num = 0
            merge_start = 0
            merge_stop = 0
            wsn = f'{yearly_list[i]["months"][j]["month"]}'
            worksheet_name = workbook_name.add_worksheet(name=wsn)
            # call get_row function
            row_names = get_row(strategy_name)
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
                    data = map_data_to_row(strategy_name, yearly_list, i, j, k, h)
                    row_num += 1
                    worksheet_name.write_row(row_num, 1, data, cell_format)
                # add setting for some rows
                make_sum_row(strategy_name, worksheet_name, merge_start,
                             merge_stop, value, cell_format, row_day)
        workbook_name.close()
        print('done')


def open_report_file():
    os.system(f"open 'main/report'")


def create_report(strategy_name):
    src = f"main/.data/{strategy_name}/"
    dst = f'main/report/{strategy_name}/'
    for filename in os.listdir(src):
        shutil.copy(src + filename, dst)
    # create report by pair
    src_by_pair = f"main/.data/byPair/{strategy_name}/"
    dst_by_pair = f'main/report/byPair/{strategy_name}/'
    for filename in os.listdir(src_by_pair):
        shutil.copy(src_by_pair + filename, dst_by_pair)


def get_row(strategy_name):
    if strategy_name == "momentum":
        row_names = ['DAY', 'PAIR', 'TIME', 'POSITION',
                     '1HR CHART', '15MIN CHART', 'PROFIT R',
                     'COMMENTS', 'ID', 'SUM']
        return row_names
    elif strategy_name == "harmonic":
        row_names = ['DAY', 'PAIR', 'TIME', 'POSITION',
                     '1HR CHART', '1DAY CHART', 'PROFIT R',
                     'COMMENTS', 'ID', 'SUM']
        return row_names
    else:
        row_names = ['DAY', 'PAIR', 'TIME', 'POSITION',
                     '4HOUR CHART', 'PRE 4HOUR CHART',
                     '1DAY CHART', '1WEEK CHART', '1MONTH CHART',
                     'PROFIT R', 'COMMENTS', 'ID', 'SUM']
        return row_names


def get_row_by_pair(strategy_name):
    if strategy_name == "momentum":
        row_names = ['MONTH', 'DAY', 'TIME', 'POSITION',
                     '1HR CHART', '15MIN CHART', 'PROFIT R',
                     'COMMENTS', 'ID', 'SUM']
        return row_names
    elif strategy_name == "harmonic":
        row_names = ['MONTH', 'DAY', 'TIME', 'POSITION',
                     '1HR CHART', '1DAY CHART', 'PROFIT R',
                     'COMMENTS', 'ID', 'SUM']
        return row_names
    else:
        row_names = ['MONTH', 'DAY', 'TIME', 'POSITION',
                     '4HOUR CHART', 'PRE 4HOUR CHART',
                     '1DAY CHART', '1WEEK CHART', '1MONTH CHART',
                     'PROFIT R', 'COMMENTS', 'ID', 'SUM']
        return row_names


def map_data_to_row(strategy_name, yearly_list, i, j, k, h):
    if strategy_name == "momentum":
        data = [yearly_list[i]["months"][j]["days"][k]["transactions"][h]['PAIR'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['TIME'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['POSITION'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['1HR CHART'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['15MIN CHART'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['PROFIT R'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['COMMENTS'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['INDEX']]
        return data
    elif strategy_name == "harmonic":
        data = [yearly_list[i]["months"][j]["days"][k]["transactions"][h]['PAIR'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['TIME'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['POSITION'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['1HR CHART'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['1DAY CHART'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['PROFIT R'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['COMMENTS'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['INDEX']]
        return data
    else:
        data = [yearly_list[i]["months"][j]["days"][k]["transactions"][h]['PAIR'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['TIME'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['POSITION'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['4HR CHART'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['PRE 4DAY CHART'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['1DAY CHART'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['1WEEK CHART'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['1MONTH CHART'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['PROFIT R'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['COMMENTS'],
                yearly_list[i]["months"][j]["days"][k]["transactions"][h]['INDEX']]
        return data


def map_data_to_row_by_pair(strategy_name, yearly_list, i, j, k, h):
    if strategy_name == "momentum":
        data = [yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['DAY'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['TIME'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['POSITION'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['1HR CHART'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['15MIN CHART'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['PROFIT R'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['COMMENTS'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['INDEX']]
        return data
    elif strategy_name == "harmonic":
        data = [yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['DAY'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['TIME'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['POSITION'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['1HR CHART'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['1DAY CHART'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['PROFIT R'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['COMMENTS'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['INDEX']]
        return data
    else:
        data = [yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['DAY'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['TIME'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['POSITION'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['4HR CHART'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['PRE 4DAY CHART'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['1DAY CHART'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['1WEEK CHART'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['1MONTH CHART'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['PROFIT R'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['COMMENTS'],
                yearly_list[i]["pairs"][j]["months"][k]["transactions"][h]['INDEX']]
        return data


def make_sum_row(strategy_name, worksheet_name, merge_start,
                 merge_stop, value, cell_format, row_day):
    if strategy_name == "swing_trading":
        # set column width
        worksheet_name.set_column('E:I', 35)
        worksheet_name.set_column('K:K', 30)
        if merge_start == merge_stop:
            worksheet_name.write(f'M{merge_start}', value, cell_format)
        else:
            worksheet_name.merge_range(f'A{merge_start}:A{merge_stop}',
                                       f'{row_day[0]}',
                                       cell_format)
            worksheet_name.merge_range(f'M{merge_start}:M{merge_stop}',
                                       f'=SUM(J{merge_start}:J{merge_stop})',
                                       cell_format)
    else:
        # set column width
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


def query_transaction(cur, strategy_name, year, month, day):
    if strategy_name == "momentum":
        transactions = cur.execute("SELECT "
                                   "rowid, "
                                   "date, "
                                   "year, "
                                   "month, "
                                   "day, "
                                   "time, "
                                   "pair, "
                                   "position, "
                                   "one_hr_chart, "
                                   "fifteen_min_chart, "
                                   "profit_r, "
                                   "comments "
                                   f"FROM {strategy_name} WHERE year=? AND month=? AND day=? ORDER BY time",
                                   (year, month, day)).fetchall()
        return transactions
    elif strategy_name == "harmonic":
        transactions = cur.execute("SELECT "
                                   "rowid, "
                                   "date, "
                                   "year, "
                                   "month, "
                                   "day, "
                                   "time, "
                                   "pair, "
                                   "position, "
                                   "one_hr_chart, "
                                   "one_day_chart, "
                                   "profit_r, "
                                   "comments "
                                   f"FROM {strategy_name} WHERE year=? AND month=? AND day=? ORDER BY time",
                                   (year, month, day)).fetchall()
        return transactions
    else:
        transactions = cur.execute("SELECT "
                                   "rowid, "
                                   "date, "
                                   "year, "
                                   "month, "
                                   "day, "
                                   "time, "
                                   "pair, "
                                   "position, "
                                   "four_hr_chart, "
                                   "pre_four_hr_chart, "
                                   "one_day_chart, "
                                   "one_week_chart, "
                                   "one_month_chart, "
                                   "profit_r, "
                                   "comments "
                                   f"FROM {strategy_name} WHERE year=? AND month=? AND day=?"
                                   f"ORDER BY day ASC, time",
                                   (year, month, day)).fetchall()
        return transactions


def extract_transaction_data(strategy_name, data):
    if strategy_name == "momentum":
        transaction_data = {"INDEX": data[0],
                            'TIME': data[5],
                            'PAIR': data[6],
                            'POSITION': data[7],
                            '1HR CHART': data[8],
                            '15MIN CHART': data[9],
                            'PROFIT R': data[10],
                            'COMMENTS': data[11]
                            }
        return transaction_data
    elif strategy_name == "harmonic":
        transaction_data = {"INDEX": data[0],
                            'TIME': data[5],
                            'PAIR': data[6],
                            'POSITION': data[7],
                            '1HR CHART': data[8],
                            '1DAY CHART': data[9],
                            'PROFIT R': data[10],
                            'COMMENTS': data[11]
                            }
        return transaction_data
    else:
        transaction_data = {"INDEX": data[0],
                            'TIME': data[5],
                            'PAIR': data[6],
                            'POSITION': data[7],
                            '4HR CHART': data[8],
                            'PRE 4DAY CHART': data[9],
                            '1DAY CHART': data[10],
                            '1WEEK CHART': data[11],
                            '1MONTH CHART': data[12],
                            'PROFIT R': data[13],
                            'COMMENTS': data[14]
                            }
        return transaction_data


def get_strategy_data_from_db(conn, strategy_name):
    cur = conn.cursor()
    years = cur.execute(f"SELECT DISTINCT year FROM {strategy_name} GROUP BY year ORDER BY year ASC").fetchall()
    yearly_list = []
    for year in years:
        monthly_list = []
        yearly_data = {'year': year[0], 'months': monthly_list}
        months = cur.execute(
            f"SELECT DISTINCT month FROM {strategy_name} WHERE year=? GROUP BY month ORDER BY month ASC",
            year).fetchall()
        for month in months:
            daily_list = []
            monthly_data = {'month': month[0], 'days': daily_list}
            monthly_list.append(monthly_data)
            days = cur.execute(
                f"SELECT DISTINCT day FROM {strategy_name} WHERE year=? AND month=? GROUP BY day ORDER BY day ASC",
                (year[0], month[0])).fetchall()
            for day in days:
                transaction_list = []
                daily_data = {'day': day[0], 'transactions': transaction_list}
                daily_list.append(daily_data)
                transactions = query_transaction(cur, strategy_name, year[0], month[0], day[0])
                for data in transactions:
                    transaction_data = extract_transaction_data(strategy_name, data)
                    transaction_list.append(transaction_data)
        yearly_list.append(yearly_data)
    return yearly_list


def query_transaction_by_pair(cur, strategy_name, year, month, pair):
    if strategy_name == "momentum":
        transactions = cur.execute("SELECT "
                                   "rowid, "
                                   "date, "
                                   "year, "
                                   "month, "
                                   "day, "
                                   "time, "
                                   "pair, "
                                   "position, "
                                   "one_hr_chart, "
                                   "fifteen_min_chart, "
                                   "profit_r, "
                                   "comments "
                                   f"FROM {strategy_name} WHERE year=? AND month=? AND pair=? ORDER BY time",
                                   (year, month, pair)).fetchall()
        return transactions
    elif strategy_name == "harmonic":
        transactions = cur.execute("SELECT "
                                   "rowid, "
                                   "date, "
                                   "year, "
                                   "month, "
                                   "day, "
                                   "time, "
                                   "pair, "
                                   "position, "
                                   "one_hr_chart, "
                                   "one_day_chart, "
                                   "profit_r, "
                                   "comments "
                                   f"FROM {strategy_name} WHERE year=? AND month=? AND pair=? ORDER BY time",
                                   (year, month, pair)).fetchall()
        return transactions
    else:
        transactions = cur.execute("SELECT "
                                   "rowid, "
                                   "date, "
                                   "year, "
                                   "month, "
                                   "day, "
                                   "time, "
                                   "pair, "
                                   "position, "
                                   "four_hr_chart, "
                                   "pre_four_hr_chart, "
                                   "one_day_chart, "
                                   "one_week_chart, "
                                   "one_month_chart, "
                                   "profit_r, "
                                   "comments "
                                   f"FROM {strategy_name} WHERE year=? AND month=? AND pair=? ORDER BY day, time",
                                   (year, month, pair)).fetchall()
        return transactions


def extract_transaction_data_by_pair(strategy_name, data):
    if strategy_name == "momentum":
        transaction_data = {"INDEX": data[0],
                            'TIME': data[5],
                            'DAY': data[4],
                            'POSITION': data[7],
                            '1HR CHART': data[8],
                            '15MIN CHART': data[9],
                            'PROFIT R': data[10],
                            'COMMENTS': data[11]
                            }
        return transaction_data
    elif strategy_name == "harmonic":
        transaction_data = {"INDEX": data[0],
                            'TIME': data[5],
                            'DAY': data[4],
                            'POSITION': data[7],
                            '1HR CHART': data[8],
                            '1DAY CHART': data[9],
                            'PROFIT R': data[10],
                            'COMMENTS': data[11]
                            }
        return transaction_data
    else:
        transaction_data = {"INDEX": data[0],
                            'TIME': data[5],
                            'DAY': data[4],
                            'POSITION': data[7],
                            '4HR CHART': data[8],
                            'PRE 4DAY CHART': data[9],
                            '1DAY CHART': data[10],
                            '1WEEK CHART': data[11],
                            '1MONTH CHART': data[12],
                            'PROFIT R': data[13],
                            'COMMENTS': data[14]
                            }
        return transaction_data


def get_strategy_data_from_db_by_pair(conn, strategy_name):
    cur = conn.cursor()
    years = cur.execute(f"SELECT DISTINCT year FROM {strategy_name} GROUP BY year ORDER BY year ASC").fetchall()
    yearly_list = []
    for year in years:
        pair_list = []
        yearly_data = {'year': year[0], 'pairs': pair_list}
        pairs = cur.execute(
            f"SELECT DISTINCT pair FROM {strategy_name} WHERE year=? GROUP BY pair ORDER BY pair ASC",
            year).fetchall()
        for pair in pairs:
            monthly_list = []
            pair_data = {'pair': pair[0], 'months': monthly_list}
            pair_list.append(pair_data)
            months = cur.execute(
                f"SELECT DISTINCT month FROM {strategy_name} WHERE year=? AND pair=? GROUP BY month ORDER BY month ASC",
                (year[0], pair[0])).fetchall()
            for month in months:
                transaction_list = []
                monthly_data = {'month': month[0], 'transactions': transaction_list}
                monthly_list.append(monthly_data)
                transactions = query_transaction_by_pair(cur, strategy_name, year[0], month[0], pair[0])
                print("transactions:", transactions)
                for data in transactions:
                    transaction_data = extract_transaction_data_by_pair(strategy_name, data)
                    transaction_list.append(transaction_data)
        yearly_list.append(yearly_data)
    return yearly_list


def write_data_by_pair(conn, strategy_name):
    yearly_list = get_strategy_data_from_db_by_pair(conn=conn, strategy_name=strategy_name)
    print(yearly_list)
    for i in range(len(yearly_list)):
        wbn = f"main/.data/byPair/{strategy_name}/[{yearly_list[i]['year']}]" + "[HuyNguyen]-TradingView" + ".xlsx"
        workbook_name = xlsxwriter.Workbook(filename=wbn)
        cell_format = workbook_name.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'})
        for j in range(len(yearly_list[i]["pairs"])):
            row_num = 0
            merge_start = 0
            merge_stop = 0
            wsn = f'{yearly_list[i]["pairs"][j]["pair"]}'
            worksheet_name = workbook_name.add_worksheet(name=wsn)
            # call get_row function
            row_names = get_row_by_pair(strategy_name)
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
                    data = map_data_to_row_by_pair(strategy_name, yearly_list, i, j, k, h)
                    row_num += 1
                    worksheet_name.write_row(row_num, 1, data, cell_format)
                # add setting for some rows
                make_sum_row(strategy_name, worksheet_name, merge_start,
                             merge_stop, value, cell_format, row_day)
        workbook_name.close()
        print('done')
