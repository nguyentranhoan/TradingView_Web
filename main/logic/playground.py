if __name__ == "__main__":
    from logic.create_connection import create_connection
    from show_data import write_data_to_excel
    from from_db import get_data_from_db
    database_url = '../../.data/transaction.db'
    conn = create_connection(database_url)
    year_list = get_data_from_db(conn)
    write_data_to_excel(year_list)
    # create_report()
    # open_report_file()
    # .data/transaction.db
