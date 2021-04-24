from flask import render_template, request
import datetime

from main.logic.from_db import store_data_db
from main import app

from main.logic.screenshot import preview_screenshot, take_a_screenshot
from main.logic.show_data import write_data_to_excel, create_report, open_report_file
from main.logic.create_connection import create_connection, create_database

database_url = 'main/.data/transaction.db'
conn = create_connection(database_url)
create_database(conn)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(data)
    store_data_db(conn=conn, data=data)
    write_data_to_excel(conn=conn)
    # src, dst for create report
    src = f"main/.data/[{datetime.datetime.now().year}][HuyNguyen]-TradingView.xlsx"
    dst = f'main/report/'
    create_report(src=src, dst=dst)
    return 'done'


@app.route('/preview', methods=['GET'])
def preview():
    preview_screenshot()
    return 'ok'


@app.route('/report', methods=['GET'])
def report():
    file_path = "main/report/[2021][HuyNguyen]-TradingView.xlsx"
    open_report_file(file_path)
    return 'ok'


@app.route('/screenshot', methods=['POST'])
def screenshot():
    data = request.get_json()
    screen_no = int(data['screenNo'])
    take_a_screenshot(screen_no)
    print(screen_no)
    return 'ok'


# if __name__ == '__main__':
#     app.run(port=4444,
#             debug=True)


