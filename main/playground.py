import sqlite3
from sqlite3 import Error
from datetime import datetime
from main.response.momentum import Momentum
from main.response.harmonic import Harmonic
from main.response.swing_trading import SwingTrading


def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param database_url:
    :param db_file: database file
    :return: Connection object or None
    """
    # database = get_config()
    conn = None
    try:
        conn = sqlite3.connect('/Users/macintoshhd/Desktop/Hoan/TradingView_Web/main/test.db')
        return conn
    except Error as e:
        print(e)

    return conn


if __name__ == '__main__':
    now = datetime.now()
    conn = create_connection()
    cur = conn.cursor()
    index = 800
    for i in range(20):
        index += i
        data = SwingTrading(datetime=f"{now}",
                            year=now.year-i,
                            month=now.month,
                            day=now.day+i,
                            time=f"{now.time()}",
                            pair="PAIR2",
                            position="Sell",
                            four_hr_chart="link 1",
                            pre_four_hr_chart="link 2",
                            one_day_chart="link 3",
                            one_week_chart="link 4",
                            one_month_chart="link 5",
                            profit_r=3,
                            comments="this is my comment")
        momentum_query = f"INSERT INTO momentum VALUES ({index}, '{data.datetime}',{data.year}, {data.month}, {data.day},'{data.time}', '{data.pair}', '{data.position}', '{data.four_hr_chart}', '{data.pre_four_hr_chart}',{data.profit_r}, '{data.comments}');"
        cur.execute(momentum_query)
        harmonic_query = f"INSERT INTO harmonic VALUES ({index}, '{data.datetime}',{data.year}, {data.month}, {data.day},'{data.time}','{data.pair}', '{data.position}','{data.four_hr_chart}', '{data.pre_four_hr_chart}',{data.profit_r},'{data.comments}');"
        cur.execute(harmonic_query)
        st_query = f"INSERT INTO swing_trading VALUES ({index}, '{data.datetime}', {data.year},{data.month}, {data.day},'{data.time}','{data.pair}', '{data.position}','{data.four_hr_chart}', '{data.pre_four_hr_chart}','{data.one_day_chart}','{data.one_week_chart}', '{data.one_month_chart}',{data.profit_r},'{data.comments}');"
        cur.execute(st_query)

        conn.commit()

    conn.close()
