import os
import shutil

import xlsxwriter

from main.logic.strategy import get_strategy_data_from_db


def write_data_to_excel(conn, table_name):
    yearly_list = get_strategy_data_from_db(conn, table_name)

    for i in range(len(yearly_list)):
        wbn = f".data/[{yearly_list[i]['year']}]" + "[HuyNguyen]-TradingView" + ".xlsx"
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
            worksheet_name.set_column('E:F', 35)
            worksheet_name.set_column('H:H', 30)
            row_names = ['DAY',
                         'PAIR',
                         'TIME',
                         'POSITION',
                         '1HR CHART',
                         '15MIN CHART',
                         'PROFIT R',
                         'COMMENTS',
                         'ID',
                         'SUM']
            worksheet_name.write_row(0, 0, row_names, cell_format)
            for k in range(len(yearly_list[i]["months"][j]["days"])):
                row_day = [yearly_list[i]["months"][j]["days"][k]["day"], ]
                worksheet_name.write_row(row_num + 1, 0, row_day, cell_format)
                s = 0
                for h in range(len(yearly_list[i]["months"][j]["days"][k]["transactions"])):
                    s += yearly_list[i]["months"][j]["days"][k]["transactions"][h]['PROFIT R']
                    merge_start = row_num + 2 - h
                    merge_stop = row_num + 1 - h + len(yearly_list[i]["months"][j]["days"][k]["transactions"])
                    data = [
                            yearly_list[i]["months"][j]["days"][k]["transactions"][h]['PAIR'],
                            yearly_list[i]["months"][j]["days"][k]["transactions"][h]['TIME'],
                            yearly_list[i]["months"][j]["days"][k]["transactions"][h]['POSITION'],
                            yearly_list[i]["months"][j]["days"][k]["transactions"][h]['1HR CHART'],
                            yearly_list[i]["months"][j]["days"][k]["transactions"][h]['15MIN CHART'],
                            yearly_list[i]["months"][j]["days"][k]["transactions"][h]['PROFIT R'],
                            yearly_list[i]["months"][j]["days"][k]["transactions"][h]['COMMENTS'],
                            yearly_list[i]["months"][j]["days"][k]["transactions"][h]['INDEX']
                            ]
                    row_num += 1
                    worksheet_name.write_row(row_num, 1, data, cell_format)
                if merge_start == merge_stop:
                    worksheet_name.write(f'J{merge_start}', s, cell_format)
                else:
                    worksheet_name.merge_range(f'A{merge_start}:A{merge_stop}',
                                               f'{row_day[0]}',
                                               cell_format)
                    worksheet_name.merge_range(f'J{merge_start}:J{merge_stop}',
                                               f'=SUM(G{merge_start}:G{merge_stop})',
                                               cell_format)
        workbook_name.close()
        print('done')


def open_report_file(file_path):
    os.system(f"open {file_path}")


def create_report(src, dst):
    shutil.copy(src, dst)

#
# if __name__ == "__main__":
#     create_report()
#     open_report_file()
