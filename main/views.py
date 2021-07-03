# from flask import render_template, request, jsonify, abort
#
# from main import app
# from main.logic.screenshot import FromScreenshot
# from main.logic.strategy import open_report_file
#
#
# # this should be the welcome page the index page
# @app.route('/', methods=['GET'])
# def index():
#     return render_template('index.html')
#
#
# @app.route('/update', methods=['GET'])
# def update():
#     return render_template('update.html')
#
#
# @app.route('/momentum', methods=['GET'])
# def momentum():
#     return render_template('momentum.html')
#
#
# @app.route('/harmonic', methods=['GET'])
# def harmonic():
#     return render_template('harmonic.html')
#
#
# @app.route('/swing_trading', methods=['GET'])
# def swing_trading():
#     return render_template('swing_trading.html')
#
#
# @app.route('/preview/<strategy_name>', methods=['GET'])
# def preview(strategy_name):
#     FromScreenshot(strategy_name).preview_screenshot()
#     return {"message": "This is the {} screenshot".format(strategy_name)}, 200
#
#
# @app.route('/report', methods=['GET'])
# def report():
#     open_report_file()
#     return 'ok'
#
#
# @app.route('/screenshot/<strategy_name>', methods=['POST'])
# def screenshot(strategy_name):
#     data = request.get_json()
#     screen_no = int(data['screenNo'])
#     if screen_no is None:
#         return {"message": "screen num is out of index"}, 502
#     FromScreenshot(strategy_name).take_a_screenshot(screen_no)
#     return {"message": "{} screenshot taken successfully".format(strategy_name)}, 200
#
#
# @app.route('/search/<strategy_name>/<transaction_id>', methods=["GET"])
# def get_transaction_id(strategy_name, transaction_id):
#     transaction = transaction_by_id(conn, strategy_name, transaction_id)
#     if transaction is None:
#         abort(404, "Transaction not found, please check again or call your brother")
#     data = {"dateTime": f"{transaction[2]}/{transaction[3]}/{transaction[4]} - {transaction[5]}",
#             "position": f"{transaction[7]}",
#             "pair": f"{transaction[6]}",
#             "profitR": transaction[8],
#             "comment": f"{transaction[9]}"}
#     return jsonify(data)
