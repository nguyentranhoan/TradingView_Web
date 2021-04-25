import sqlite3
from sqlite3 import Error


def create_connection(database_url):
    """ create a database connection to the SQLite database
        specified by db_file
    :param database_url:
    :param db_file: database file
    :return: Connection object or None
    """
    # database = get_config()
    conn = None
    try:
        conn = sqlite3.connect(database_url, check_same_thread=False)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_database(conn):
    sql_create_tradingview_table = """ CREATE TABLE IF NOT EXISTS tradingview_data (
                                        date DATE,
                                        year INTEGER,
                                        month INTEGER,
                                        day INTEGER, 
                                        time CHAR(50), 
                                        pair TEXT, 
                                        position TEXT, 
                                        one_hr_chart TEXT, 
                                        fifteen_min_chart TEXT, 
                                        profit_r FLOAT, 
                                        comments TEXT); """

    # create a database connection
    # database_url = '../.data/transaction.db'
    # conn = create_connection(database_url)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_tradingview_table)
    else:
        print("Error! cannot create the database connection.")


# if __name__ == '__main__':
#     conn = create_connection()
#     print(conn)