from main.logic.image_to_text import image_to_text
from main.logic.strategy import get_strategy_data_from_db_by_pair, query_transaction_by_pair, \
    extract_transaction_data_by_pair, create_report, write_data_by_pair, write_data
from main.views import conn
import re


def get_ratio(message):
    pattern_profit_r = r'R.+R.+R.+:.+'
    r = re.search(pattern_profit_r, message)
    rr = re.search(r'\d+(.?)\d+', r.group(0))
    return float(rr.group(0))


def add2digits(a, b):
    try:
        s = a + b
    except TypeError as e:
        return e
    return s


def test():
    a = 'k'
    b = 5
    try:
        tem = add2digits(a, b)
    except Exception as e:
        return False
    return tem


if __name__ == '__main__':
    # # print(get_strategy_data_from_db_by_pair(conn, 'momentum'))
    # data = query_transaction_by_pair(conn.cursor(), 'momentum', 2017, 9, 'USDBTC')
    # for i in data:
    #     print(extract_transaction_data_by_pair('momentum', i))
    # print(get_strategy_data_from_db_by_pair(conn, 'momentum'))
    write_data(conn, 'swing_trading')
    write_data_by_pair(conn, 'swing_trading')
    create_report('swing_trading')
    # pairs = conn.cursor().execute(
    #         f"SELECT DISTINCT pair FROM momentum WHERE year=2021 GROUP BY pair ORDER BY month ASC").fetchall()
    # for pair in pairs:
    #     print(pair)
