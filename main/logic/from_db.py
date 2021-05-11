from main.logic.data_from_img import get_transaction_data


def get_data_from_db(conn, table_name):
    cur = conn.cursor()
    years = cur.execute(f"SELECT DISTINCT year FROM {table_name} GROUP BY year ORDER BY year ASC").fetchall()
    yearly_list = []
    for year in years:
        monthly_list = []
        yearly_data = {'year': year[0], 'months': monthly_list}
        months = cur.execute(
            f"SELECT DISTINCT month FROM {table_name} WHERE year=? GROUP BY month ORDER BY month ASC",
            year).fetchall()
        for month in months:
            daily_list = []
            monthly_data = {'month': month[0], 'days': daily_list}
            monthly_list.append(monthly_data)
            days = cur.execute(
                f"SELECT DISTINCT day FROM {table_name} WHERE month=? GROUP BY day ORDER BY day ASC",
                month).fetchall()
            for day in days:
                transaction_list = []
                daily_data = {'day': day[0], 'transactions': transaction_list}
                daily_list.append(daily_data)
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
                                           f"FROM {table_name} WHERE year=? AND month=? AND day=?",
                                           (year[0], month[0], day[0])).fetchall()
                for data in transactions:
                    print(data)
                    transaction_data = {"INDEX": data[0],
                                        'TIME': data[5],
                                        'PAIR': data[6],
                                        'POSITION': data[7],
                                        '1HR CHART': data[8],
                                        '15MIN CHART': data[9],
                                        'PROFIT R': data[10],
                                        'COMMENTS': data[11]
                                        }
                    transaction_list.append(transaction_data)
        yearly_list.append(yearly_data)
    return yearly_list


def transaction_by_id(conn, table_name, transaction_id):
    cur = conn.cursor()
    transaction = cur.execute(f"SELECT rowid, date, year, month, day, time, "
                              f"pair, position, profit_r, comments "
                              f"FROM {table_name} WHERE rowid={transaction_id}").fetchone()
    return transaction


def update_transaction_by_id(conn, table_name, transaction_id, profit_r, comments):
    comment = alter_comment(comments)
    conn.cursor().execute(
        f"UPDATE {table_name} SET profit_r={profit_r}, comments='{comment}' WHERE rowid={transaction_id};")
    conn.commit()


def delete_transaction_by_id(conn, table_name, transaction_id):
    conn.cursor().execute(f"DELETE FROM {table_name} WHERE rowid={transaction_id};")
    conn.commit()


def store_data_db(conn, table_name, data):
    transaction_data = get_transaction_data(table_name, data)
    print(data)
    cur = conn.cursor()
    comments = f"{transaction_data['COMMENTS']}"
    comment = alter_comment(comments)
    transaction = check_existed_transaction(cur, table_name, transaction_data)
    if transaction is not None:
        update_query = update_data(table_name, transaction_data,
                                   transaction, comment)
        cur.execute(update_query)
    else:
        insert_query = insert_data(table_name, transaction_data, comments)
        cur.execute(insert_query)
    conn.commit()


def alter_comment(comment):
    for i in comment:
        if i == '=' or i == '-':
            comment = "'" + comment
            break
    comment = comment.replace("'", "''")
    comment = comment.replace('"', '""')
    return comment


def check_existed_transaction(cur, table_name, transaction_data):
    transaction = cur.execute(
        f"""SELECT rowid FROM {table_name} 
            WHERE date={transaction_data['DATE']} 
                AND pair='{transaction_data['PAIR']}' 
                AND time='{transaction_data['TIME']}'
                AND position='{transaction_data['POSITION']}'""").fetchone()
    return transaction


def update_data(table_name, transaction_data, transaction, comments):
    query = f"""UPDATE {table_name} SET
                    comments='{comments}',
                    position='{transaction_data['POSITION']}',
                    profit_r={transaction_data['PROFIT R']}
                WHERE rowid={transaction[0]}'"""
    return query


def insert_data(table_name, transaction_data, comments):
    if table_name == "":
        query = f"""INSERT INTO {table_name} VALUES (
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
        return query
    elif table_name == "":
        query = f"""INSERT INTO {table_name} VALUES (
                        {transaction_data['DATE']},
                        {transaction_data['YEAR']},
                        {transaction_data['MONTH']},
                        {transaction_data['DAY']},
                        '{transaction_data['TIME']}',
                        '{transaction_data['PAIR']}',
                        '{transaction_data['POSITION']}',
                        '{transaction_data['1HR CHART']}',
                        '{transaction_data['1DAY CHART']}',
                        {transaction_data['PROFIT R']},
                        '{comments}');"""
        return query
    else:
        query = f"""INSERT INTO {table_name} VALUES (
                        {transaction_data['DATE']},
                        {transaction_data['YEAR']},
                        {transaction_data['MONTH']},
                        {transaction_data['DAY']},
                        '{transaction_data['TIME']}',
                        '{transaction_data['PAIR']}',
                        '{transaction_data['POSITION']}',
                        '{transaction_data['4HR CHART']}',
                        '{transaction_data['PRE 4HOUR CHART']}',
                        '{transaction_data['1DAY CHART']}',
                        '{transaction_data['1WEEK CHART']}',
                        '{transaction_data['1MONTH CHART']}',
                        {transaction_data['PROFIT R']},
                        '{comments}');"""
        return query
