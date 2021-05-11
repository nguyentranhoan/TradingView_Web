import datetime
import re

from main.logic.image_to_text import image_to_text
from main.logic.from_dropbox import get_image_url


def get_datetime(message):
    pattern_time = r"\S\d\s[a-zA-Z]+\s('?)\d+\s\d+(:)\d+"
    tem = re.search(pattern_time, message)
    date_time_str = str(tem.group(0))
    date_time_str = date_time_str.replace("'", "")
    date_time = datetime.datetime.strptime(date_time_str, '%d %b %y %H:%M')
    return date_time


def get_pair(message):
    pattern_pair = r'[a-zA-Z]+:[a-zA-Z]+'
    pair = re.search(pattern_pair, message)
    symbol = pair.group(0)
    symbol = re.sub(r'[a-zA-Z]+(:)', '', symbol)
    return symbol


def get_ratio(message):
    pattern_profit_r = r'Ratio:.+'
    r = re.search(pattern_profit_r, message)
    # print(r)
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
    message = f"""{image_to_text(image_url)}"""
#     message = """
# nguyentranhoan published on Trading View.com, March 24, 2021 20:56:38 +07 FX:HUYHOAN, 15 1.37112 -0.00333 (-0.24%) 0:1.37132 H:1.37195 L: 1.37000 C: 1.37112
# British Pound / U.S. Dollar, 15, FXCM
# + 1 USD
# 1.38672 - 1.38657
# 1.38600
# 1.38500
# - 1.38435 + 1.38381
# 1.38364
# 1.38300
# + 1.38194
# + 1.38139
# 1.38100 - 1.38049 + 1.38034
# 1.38000
# - 1.37873 + 1.37857
# 1.37800
# 1.37700
# 1.37600
# 1.37500
# 1.37400
# 1.37300
# 1.37200
# 1.37112
# 03:24
# 1.37000
# 1 36900
# 20
# 22
# 08:00
# 12:00
# 18:00
# 23
# 06:00
# 12:00
# 18:00
# 06:00
# 12:00
# 18:00
# TradingView
# """
    # print(message)
    return get_pair(message)


def from_screenshot(strategy_name):
    image_url = get_image_url(strategy_name)
    message = image_to_text(image_url)
    print("message: ", message)
#     message = """
# Chrome
# File
# Edit
# View
# History
# Bookmarks
# People
# Tab
# Window
# Help
# <
# A
# O
# a
# 8
# Wed 24 Mar 19:08
# Ooo
# GBPUSD 1.37136
# -0.22% UI X
# +
# T Lộ trình cho Mọi n...
# T
# Lối đi riêng cho lậ...
# T Leo thang đặc qu...
# PDF 9-Bi-Quyet-Thuo
# o Introduction to Git...
# e! Top 100 Python In...
# »
# ill
# E → C tradingview.com/chart/ayow61Mm/
# Apps Defonic | A fabulo. Ps short science arti... SN Science News for... • CS50 CDN 9 Kafka tutorial #4 - 0 Hướng đi nào cho... = GBPUSD 150 00 Compare fx Indicators H Financials Templates Alert 10 Replay
# British Pound U.S. Dollar 15 FXCM K = 01.37113 H1.37148 L 1.37079 C1.37136 +0.00023 +0.02%) 1.37136 0.4 1.37140
# Target: 0.00276 (0.20%) 27.6, Amount: 1000 Vol 134K TIL
# o
# Unnamed
# C
# O
# Publish
# - 1 USD - 1.38672 + 1.38657
# o
# 1.38600
# 1.38500
# SE
# Closed P&L: 0.00276, Qty: 0
# Risk/Reward Ratio: 1.48
# - 1.38435
# 1.38381 + 1.38364
# 1.38300
# - 1.38194
# ** 099 o O cap @ @ @
# JIl ©
# Stop: 0.00187 (0.14%) 18.7, Amount: 1000
# + 1.38139
# 1 38100
# 1.38049 E 1.38034
# 1.38000
# ©
# - 1.37873 + 1.37857
# C
# 1.37800
# poco co
# 1.37700
# 1.37600
# od 3
# 1.37500
# 1.37400
# 1.37300
# 1.37200
# 1975
# Unlock the full power of TradingView Try any plan free for 30 days. We'll help you trade and invest better from the get-go.
# 1.37136 06:07
# CHD
# 30-day free trial
# 1.37000
# 1 36900
# 12:00
# 1 22 Mar 21 20:00
# 23
# 06:00
# 12:00
# 18:00
# 24
# 06:00
# 12:00
# 18:00
# 20 22 08:00 1M 3M 6m YTD 1Y5Y All
# 1D 5D
# 5
# 19:08:53 (UTC+7)
# %
# log
# auto
# Stock Screener -
# Text Notes
# Pine Editor
# Strategy Tester
# Trading Panel
# """
    # print(message)
    return get_datetime(message), \
           get_ratio(message), \
           get_position(message)


def get_transaction_data(strategy_name, data):
    transaction_datetime, transaction_ratio, transaction_position = from_screenshot(strategy_name)
    print(data)
    if int(data['profitR']) == -1:
        transaction_ratio = -1
    elif int(data["profitR"]) == 0:
        transaction_ratio = 0
    else:
        transaction_ratio = transaction_ratio
        # attention please alter data['link']
    transaction_pair = from_trading_view(image_url=data['link15Min'])
    time = f"{transaction_datetime.hour}:{transaction_datetime.minute}"
    transaction_data = {'DATE': transaction_datetime.date(),
                        'YEAR': transaction_datetime.year,
                        'MONTH': transaction_datetime.month,
                        'DAY': transaction_datetime.day,
                        'TIME': time,
                        'PAIR': transaction_pair,
                        'POSITION': transaction_position,
                        '1HR CHART': data['link1Hour'],
                        '15MIN CHART': data['link15Min'],
                        'PROFIT R': transaction_ratio,
                        'COMMENTS': data['comment']}
    print(transaction_data)
    return transaction_data
