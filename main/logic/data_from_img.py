import datetime
import re

from main.logic.image_to_text import image_to_text
from main.logic.from_dropbox import get_image_url


def get_datetime(message):
    pattern_time = r"""\S\d\s[a-zA-Z]+\s('|"?)\d+\s\d+(:)\d+"""
    tem = re.search(pattern_time, message)
    try:
        date_time_str = str(tem.group(0))
    except AttributeError as e:
        return e
    date_time_str = get_datetime_str(date_time_str)
    date_time = datetime.datetime.strptime(date_time_str, '%d %b %y %H:%M')
    return date_time


def get_pair(message):
    pattern_pair = r'[a-zA-Z]+:[a-zA-Z]+'
    pair = re.search(pattern_pair, message)
    try:
        symbol = pair.group(0)
    except AttributeError as e:
        return e
    symbol = re.sub(r'[a-zA-Z]+(:)', '', symbol)
    return symbol


def get_ratio(message):
    pattern_profit_r = r'R.+R.+R.+:.+'
    r = re.search(pattern_profit_r, message)
    try:
        rr = re.search(r'\d+(.?)(\d{0,5}?)', r.group(0))
    except AttributeError as e:
        return e
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
    message = f"""{image_to_text(image_url)}"""
    return get_pair(message)


def from_screenshot(strategy_name):
    image_url = get_image_url(strategy_name)
    message = image_to_text(image_url)
    print(message)
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
