# from main.services.logic.from_db import get_data_from_db
# from services.logic.show_data import create_report, open_report_file
#
# if __name__ == '__main__':
#     from models.create_connection import create_connection
#     database_url = '.data/transaction.db'
#     conn = create_connection(database_url)
#     data = {
#         'link15Min': 'this is 15min link',
#         'link1Hour': 'this is 1hour link',
#         'comment': 'this is the comment',
#         'profitR': 1
#     }
#     # store_data_db(data)
#     print(get_data_from_db(conn))
import os

from views import create_database, conn
database_url = '.data/transaction.db'

print(os.path.exists(database_url))
create_database(conn)

if not os.path.exists(database_url):
    create_database(conn)
    print('')


print("aaaaaa")
