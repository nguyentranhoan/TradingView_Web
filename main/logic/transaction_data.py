import csv

from main.logic.data_from_img import from_screenshot, from_trading_view


def get_transaction_data(data):
    transaction_datetime, transaction_ratio, transaction_position = from_screenshot()
    print(data)
    if int(data['profitR']) == -1:
        transaction_ratio = -1
    elif int(data["profitR"]) == 0:
        transaction_ratio = 0
    else:
        transaction_ratio = transaction_ratio
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


def store_data(data):
    with open("../.data/transaction.csv", 'w') as f:
        transaction_data = get_transaction_data(data)
        w = csv.writer(f)
        for key, value in transaction_data.items():
            w.writerow([key, value])
        f.close()


# if __name__ == '__main__':
#     data = {
#         'link15Min': 'this is 15min link',
#         'link1Hour': 'this is 1hour link',
#         'comment': 'this is the comment',
#         'profitR': 1
#     }
#     get_transaction_data(data)
