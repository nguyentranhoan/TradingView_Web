import datetime
import re

from main.logic.image_to_text import image_to_text
from main.logic.from_dropbox import get_image_url


def get_datetime(message):
    pattern_time = r"""\S\d\s[a-zA-Z]+\s('|"?)\d+\s\d+(:)\d+"""
    tem = re.search(pattern_time, message)
    date_time_str = str(tem.group(0))
    date_time_str = get_datetime_str(date_time_str)
    date_time = datetime.datetime.strptime(date_time_str, '%d %b %y %H:%M')
    return date_time


def get_pair(message):
    pattern_pair = r'[a-zA-Z]+:[a-zA-Z]+'
    pair = re.search(pattern_pair, message)
    symbol = pair.group(0)
    symbol = re.sub(r'[a-zA-Z]+(:)', '', symbol)
    return symbol


def get_ratio(message):
    pattern_profit_r = r'R.+R.+R.+:.+'
    r = re.search(pattern_profit_r, message)
    rr = re.search(r'\d+(.?)\d+', r.group(0))
    return float(rr.group(0))


def get_position(message):
    pattern_buy = r'Target((.|\n)*)Ratio:.+'
    # pattern_sell = r'Stop((.|\n)*)Target.+'
    buy = re.search(pattern_buy, message)
    transaction_position = ''
    if buy is not None:
        transaction_position = 'Buy'
    if buy is None:
        transaction_position = 'Sell'
    return transaction_position


def from_trading_view(image_url):
    # message = f"""{image_to_text(image_url)}"""
    message = """FX:GPBUSD"""
    return get_pair(message)


def from_screenshot(strategy_name):
    # image_url = get_image_url(strategy_name)
    # message = image_to_text(image_url)
    # print(message)
    message = """GBPUSD
15m
+ Compare
fr Indicators
l Financials
M Templates Q Alert
14 Replay
O Unnamed
Publish<br />
British Pound / U.S. Dollar · 15 · FXCM K<br />
01.41015 H1.41119 L1.40995 C1.41075 +0.00060 (+0.04%)<br />
1. USDO
T
1.41077 0.0 1.41077
www
1.41700
Vol 3.086K
1.41600
1.41500
T<br />
Target: 0.00275 (0.19%) 27.5, Amount: 1577.73<br />
-1.41416
1.41316
1.41200<br />
Closed P&L: 0.00275, Qty: 210084<br />
Risk/Reward Ratio: 2.31
- 1.41141
1 41100
1.41075
06:44
-1.41022<br />
Stop: 0.00119 (0.08%) 11.9, Amount: 750<br />
1.40900
1.40800
1.40700
1.40600
1.40500
1.40400
1.40300<br />
Unlock the full power of TradingView<br />
1.40200<br />
Try any plan free for 30 days. We'll help you<br />
trade and invest better from the get-go.<br />
1.40100
30-day free trial
1.40000
1:00
06:00
09:00
12:00
11 May "21 13:30 15:00
18:00
21:00
12
03:00
06:00
09:00
12:00<br />
1D 5D 1M 3M 6M YTD 1Y 5Y All<br />
21:23:16 (UTC+7)
% log auto
Stock Screener
Text Notes
Pine Editor
Strategy Tester
Trading Panel
"""
    return get_datetime(message), \
           get_ratio(message), \
           get_position(message)


def get_chosen_ratio(data, transaction_ratio):
    if int(data['profitR']) == -1:
        value = -1
        return value
    elif int(data["profitR"]) == 0:
        value = 0
        return value
    else:
        value = transaction_ratio
        return value


def transaction_model(strategy_name, data):
    transaction_datetime, transaction_ratio, transaction_position = from_screenshot(strategy_name)
    chosen_transaction_ratio = get_chosen_ratio(data, transaction_ratio)
    time = f"{transaction_datetime.hour}:{transaction_datetime.minute}"
    if strategy_name == "momentum":
        transaction_pair = from_trading_view(image_url=data['link15Mins'])
        transaction_data = {'DATE': transaction_datetime.date(),
                            'YEAR': transaction_datetime.year,
                            'MONTH': transaction_datetime.month,
                            'DAY': transaction_datetime.day,
                            'TIME': time,
                            'PAIR': transaction_pair,
                            'POSITION': transaction_position,
                            '1HR CHART': data['link1Hour'],
                            '15MIN CHART': data['link15Mins'],
                            'PROFIT R': chosen_transaction_ratio,
                            'COMMENTS': data['comment']}
        return transaction_data
    elif strategy_name == "harmonic":
        transaction_pair = from_trading_view(image_url=data['link1Hour'])
        transaction_data = {'DATE': transaction_datetime.date(),
                            'YEAR': transaction_datetime.year,
                            'MONTH': transaction_datetime.month,
                            'DAY': transaction_datetime.day,
                            'TIME': time,
                            'PAIR': transaction_pair,
                            'POSITION': transaction_position,
                            '1HR CHART': data['link1Hour'],
                            '1DAY CHART': data['link1Day'],
                            'PROFIT R': chosen_transaction_ratio,
                            'COMMENTS': data['comment']}
        return transaction_data
    elif strategy_name == 'swing_trading':
        transaction_pair = from_trading_view(image_url=data['link4Hours'])
        transaction_data = {'DATE': transaction_datetime.date(),
                            'YEAR': transaction_datetime.year,
                            'MONTH': transaction_datetime.month,
                            'DAY': transaction_datetime.day,
                            'TIME': time,
                            'PAIR': transaction_pair,
                            'POSITION': transaction_position,
                            '4HR CHART': data['link4Hours'],
                            'PRE 4HOUR CHART': data['linkPre4Hours'],
                            '1DAY CHART': data['link1Day'],
                            '1WEEK CHART': data['link1Week'],
                            '1MONTH CHART': data['link1Month'],
                            'PROFIT R': chosen_transaction_ratio,
                            'COMMENTS': data['comment']}
        return transaction_data


def get_transaction_data(strategy_name, data):
    transaction_data = transaction_model(strategy_name, data)
    return transaction_data


def get_datetime_str(date_time):
    if "'" in date_time:
        date_time_str = date_time.replace("'", "")
        return date_time_str
    elif '"' in f"""{date_time}""":
        date_time_str = date_time.replace('"', '')
        return date_time_str
    else:
        return date_time
