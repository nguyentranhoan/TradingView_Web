import os

# COMMON CLASSES


class ExcelFormat:
    @staticmethod
    def decorate_sheet(worksheet_name, merge_start, merge_stop, value, cell_format, row_day):
        worksheet_name.set_column('E:F', 35)
        worksheet_name.set_column('H:H', 30)
        if merge_start == merge_stop:
            worksheet_name.write(f'K{merge_start}', value, cell_format)
        else:
            worksheet_name.merge_range(f'A{merge_start}:A{merge_stop}',
                                       f'{row_day[0]}',
                                       cell_format)
            worksheet_name.merge_range(f'K{merge_start}:K{merge_stop}',
                                       f'=SUM(G{merge_start}:G{merge_stop})',
                                       cell_format)

    @staticmethod
    def decorate_sheet_scapling(worksheet_name, merge_start, merge_stop, value, cell_format, row_day):

        worksheet_name.set_column('E:E', 35)
        worksheet_name.set_column('G:G', 30)
        if merge_start == merge_stop:
            worksheet_name.write(f'J{merge_start}', value, cell_format)
        else:
            worksheet_name.merge_range(f'A{merge_start}:A{merge_stop}',
                                       f'{row_day[0]}',
                                       cell_format)
            worksheet_name.merge_range(f'J{merge_start}:J{merge_stop}',
                                       f'=SUM(F{merge_start}:F{merge_stop})',
                                       cell_format)

    @staticmethod
    def decorate_sheet_strategy_4links(worksheet_name, merge_start, merge_stop, value, cell_format, row_day):
        worksheet_name.set_column('E:I', 35)
        worksheet_name.set_column('K:K', 30)
        if merge_start == merge_stop:
            worksheet_name.write(f'N{merge_start}', value, cell_format)
        else:
            worksheet_name.merge_range(f'A{merge_start}:A{merge_stop}',
                                       f'{row_day[0]}',
                                       cell_format)
            worksheet_name.merge_range(f'N{merge_start}:N{merge_stop}',
                                       f'=SUM(J{merge_start}:J{merge_stop})',
                                       cell_format)

    @staticmethod
    def format_sheet(workbook_name):
        cell_format = workbook_name.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'})
        cell_format.set_text_wrap()
        return cell_format


class CommentExtraction:
    @staticmethod
    def get_comment(comments):
        try:
            priority = int(comments[0])
            comment = comments[3:]
        except ValueError:
            comment = comments
            priority = 0
        except IndexError:
            comment = comments
            priority = 0
        return comment, priority

    @staticmethod
    def alter_comment(comment):
        try:
            if comment[0] == "-" or comment[0] == "=":
                comment = "'" + comment
        except IndexError:
            pass
        comment = comment.replace("'", "''")
        comment = comment.replace('"', '""')
        return comment


class ProfitRatio:
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


def create_folders_if_not_exist():
    strategies = ['scapling', 'momentum', 'harmonic',
                  'daily_ici', 'weekly_ici', 'weekly_mw']
    by_pair_folders = ["main/.data/bypair/" +
                       strategy for strategy in strategies]
    folder_path = ["main/.data/" + strategy for strategy in strategies]
    folder_paths = folder_path + by_pair_folders
    for folder_path in folder_paths:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        else:
            pass
# end of file
