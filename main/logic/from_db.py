from main.logic.transaction_data import get_transaction_data


def get_data_from_db(conn):
    cur = conn.cursor()
    years = cur.execute("SELECT DISTINCT year FROM tradingview_data GROUP BY year ORDER BY year ASC").fetchall()
    yearly_list = []
    for year in years:
        monthly_list = []
        yearly_data = {'year': year[0], 'months': monthly_list}
        for month in cur.execute(
                "SELECT DISTINCT month FROM tradingview_data WHERE year=? GROUP BY month ORDER BY month ASC",
                year).fetchall():
            daily_list = []
            monthly_data = {'month': month[0], 'days': daily_list}
            monthly_list.append(monthly_data)
            for day in cur.execute(
                    "SELECT DISTINCT day FROM tradingview_data WHERE month=? GROUP BY day ORDER BY day ASC",
                    month).fetchall():
                transaction_list = []
                daily_data = {'day': day[0], 'transactions': transaction_list}
                daily_list.append(daily_data)
                for data in cur.execute("SELECT * FROM tradingview_data WHERE day=?", day).fetchall():
                    transaction_data = {'TIME': data[4],
                                        'PAIR': data[5],
                                        'POSITION': data[6],
                                        '1HR CHART': data[7],
                                        '15MIN CHART': data[8],
                                        'PROFIT R': data[9],
                                        'COMMENTS': data[10]
                                        }
                    transaction_list.append(transaction_data)
        yearly_list.append(yearly_data)
    return yearly_list


def store_data_db(conn, data):
    # if not os.path.exists('../../.data/transaction.db'):
    #     create_database()
    #     store_data_db(conn, data)
    # else:
    transaction_data = get_transaction_data(data)
    print(data)
    cur = conn.cursor()
    comments = f"{transaction_data['COMMENTS']}"
    for i in comments:
        if i == '=' or i == '-':
            comments = "'" + comments
            break
    comments = comments.replace("'", "''")
    comments = comments.replace('"', '""')
    transaction = cur.execute(
        f"""SELECT * FROM tradingview_data 
            WHERE date={transaction_data['DATE']} 
                AND pair='{transaction_data['PAIR']}' 
                AND time='{transaction_data['TIME']}'
                AND position='{transaction_data['POSITION']}'""").fetchone()
    if transaction is not None:
        cur.execute(
            f"""UPDATE tradingview_data SET
                    comments='{comments}',
                    position='{transaction_data['POSITION']}',
                    profit_r={transaction_data['PROFIT R']}
                WHERE date={transaction_data['DATE']} 
                    AND pair='{transaction_data['PAIR']}' 
                    AND time='{transaction_data['TIME']}'
                    AND position='{transaction_data['POSITION']}'""")

    else:
        query = f"""INSERT INTO tradingview_data VALUES (
                        {transaction_data['DATE']},
                        {transaction_data['YEAR']},
                        {transaction_data['MONTH']},
                        {transaction_data['DAY']},
                        '{transaction_data['TIME']}',
                        '{transaction_data['PAIR']}',
                        '{transaction_data['POSITION']}',
                        '{transaction_data['1HR CHART']}',
                        '{transaction_data['15MIN CHART']}',
                        {transaction_data['PROFIT R']},
                        '{comments}');"""
        cur.execute(query)
    conn.commit()
    # conn.close()

