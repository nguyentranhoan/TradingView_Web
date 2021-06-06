from flask import render_template, request, jsonify, abort
from main import app

from main.logic.strategy import submit_strategy, open_report_file, update_report_after_alter_data
from main.logic.from_db import transaction_by_id, update_transaction_by_id, delete_transaction_by_id

from main.logic.screenshot import preview_screenshot, take_a_screenshot
from main.logic.create_connection import create_connection, create_database

database_url = 'main/.data/transaction.db'
conn = create_connection(database_url)
create_database(conn)


# this should be the welcome page the index page


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/update', methods=['GET'])
def update():
    return render_template('update.html')


@app.route('/momentum', methods=['GET'])
def momentum():
    return render_template('momentum.html')


@app.route('/harmonic', methods=['GET'])
def harmonic():
    return render_template('harmonic.html')


@app.route('/swing_trading', methods=['GET'])
def swing_trading():
    return render_template('swing_trading.html')


@app.route('/submit/<strategy_name>', methods=['POST'])
def submit(strategy_name):
    data = request.get_json()
    submit_strategy(conn, strategy_name, data)
    return 'done'


@app.route('/preview/<strategy_name>', methods=['GET'])
def preview(strategy_name):
    preview_screenshot(strategy_name)
    return 'ok'


@app.route('/report', methods=['GET'])
def report():
    open_report_file()
    return 'ok'


@app.route('/screenshot/<strategy_name>', methods=['POST'])
def screenshot(strategy_name):
    data = request.get_json()
    screen_no = int(data['screenNo'])
    if screen_no is None:
        abort(404, "screen num is out of index")
    take_a_screenshot(screen_no, strategy_name)
    return 'ok'


@app.route('/search/<strategy_name>/<transaction_id>', methods=["GET"])
def get_transaction_id(strategy_name, transaction_id):
    transaction = transaction_by_id(conn, strategy_name, transaction_id)
    if transaction is None:
        abort(404, "Transaction not found, please check again or call your brother")
    data = {"dateTime": f"{transaction[2]}/{transaction[3]}/{transaction[4]} - {transaction[5]}",
            "position": f"{transaction[7]}",
            "pair": f"{transaction[6]}",
            "profitR": transaction[8],
            "comment": f"{transaction[9]}"}
    return jsonify(data)


@app.route("/update", methods=["POST"])
def update_transaction():
    data = request.get_json()
    update_transaction_by_id(conn, data["strategyName"], int(data["transactionID"]), data["newProfitR"],
                             data["newComment"])
    update_report_after_alter_data(conn, data["strategyName"])
    return "ok"


@app.route("/delete", methods=["POST"])
def delete_transaction():
    data = request.get_json()
    delete_transaction_by_id(conn, data["strategyName"], int(data["transactionID"]))
    update_report_after_alter_data(conn, data["strategyName"])
    return "ok"
