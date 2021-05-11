import datetime

from main.logic.strategy import get_strategy_data_from_db, write_data, create_report
from main.logic.show_data import write_data_to_excel
from main.logic.create_connection import create_connection, create_database
from main.logic.from_db import get_data_from_db, transaction_by_id

if __name__ == '__main__':
    database_url = '.data/transaction.db'
    conn = create_connection(database_url)
    cur = conn.cursor()
    create_database(conn)
    now = datetime.datetime.now()

    # for i in range(5):
    #     transaction_data = {"DATE": now.date(),
    #                         "YEAR": now.year-i,
    #                         "MONTH": now.month+i,
    #                         "DAY": now.day+i,
    #                         "TIME": now.time(),
    #                         "PAIR": "USDBTC",
    #                         "POSITION": "buy",
    #                         "1HR CHART": "LINK 4 HOURS",
    #                         "15MIN CHART": "LINK PRE 4 HOURS",
    #                         "PROFIT R": 1+i,
    #                         "COMMENT": "strategy 2 comment"}
    #
    #     cur.execute(f"""INSERT INTO swing_trading VALUES (
    #                     {transaction_data['DATE']},
    #                     {transaction_data['YEAR']},
    #                     {transaction_data['MONTH']},
    #                     {transaction_data['DAY']},
    #                     '{transaction_data['TIME']}',
    #                     '{transaction_data['PAIR']}',
    #                     '{transaction_data['POSITION']}',
    #                     '{transaction_data['1HR CHART']}',
    #                     '{transaction_data['15MIN CHART']}',
    #                     '{transaction_data['1HR CHART']}',
    #                     '{transaction_data['15MIN CHART']}',
    #                     '{transaction_data['1HR CHART']}',
    #                     {transaction_data['PROFIT R']},
    #                     '{transaction_data["COMMENT"]}')""")
    # conn.commit()

    # # write_data_to_excel(conn)
    # # cur.execute("ALTER TABLE tradingview_data RENAME TO momentum")
    # # conn.commit()
    # # write_data_to_excel(conn, 'momentum')
    # tem = get_strategy_data_from_db(conn, 'harmonic')
    # print(tem)
    # tem = cur.execute("select rowid from swing_trading").fetchall()
    # for data in tem:
    #     cur.execute(f"delete from swing_trading where rowid={data[0]}")
    # conn.commit()
    # create_report('swing_trading')
    strategy_name = "swing_trading"
    write_data(conn, strategy_name)
    for data in cur.execute(f"select rowid, year, month, day, profit_r from {strategy_name}").fetchall():
        print(data)
