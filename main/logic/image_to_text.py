import requests

from main.logic.from_dropbox import DropBox
from datetime import datetime
import re

KEY = []


class DataFromImage:
    """
    This class is used to retrieve text from image.
    The information is based on pre-defined needs of users.
    """

    @staticmethod
    def _get_datetime_str(date_time):
        if "'" in date_time:
            date_time_str = date_time.replace("'", "")
            return date_time_str
        elif '"' in f"""{date_time}""":
            date_time_str = date_time.replace('"', '')
            return date_time_str
        else:
            return date_time

    @classmethod
    def get_datetime(cls, message: str):
        pattern = r"""\S\d\s[a-zA-Z]+\s('|"?)\d+\s\d+(:)\d+"""
        tem = re.search(pattern, message)
        try:
            date_time_str = str(tem.group(0))
        except AttributeError as e:
            return e
        date_time_str = cls._get_datetime_str(date_time_str)
        date_time = datetime.strptime(date_time_str, '%d %b %y %H:%M')
        return date_time

    @classmethod
    def get_pair(cls, message: str):
        pattern = r"chart(|.+)(.|\n)+Publish(.+)?(\n(.+)?){3}"
        shorten_message = re.search(pattern, message)
        pattern_2 = r"\n[A-Z]{2}([A-Z]|\d|\S)(|\S)([A-Z]+|\d+|\n)"
        result = re.search(pattern_2, shorten_message.group(0))

        return result.group(0).strip()

    @classmethod
    def get_ratio(cls, message: str):
        pattern_profit_r = r'R.+R.+R.+:.+'
        r = re.search(pattern_profit_r, message)
        try:
            rr = re.search(r'([0-9]*[.])?[0-9]+', r.group(0))
        except AttributeError as e:
            return e
        return float(rr.group(0))

    @classmethod
    def get_position(cls, message: str):
        pattern_buy = r'Target((.|\n)*)Ratio:.+'
        # pattern_sell = r'Stop((.|\n)*)Target.+'
        buy = re.search(pattern_buy, message)
        # transaction_position = ''
        if buy:
            transaction_position = 'Buy'
        else:
            transaction_position = 'Sell'
        return transaction_position


class ImageToText:
    """
    This class is used to return data by calling an API orcly image-to-text.
    """

    # image has to be accessed online.
    @staticmethod
    def __image_to_text__(image_url):
        # number of keys can send the request via api

        for i in range(len(KEY)):
            url = "https://ocrly-image-to-text.p.rapidapi.com/"
            querystring = {"imageurl": f'{image_url}',
                           "filename": "sample.jpg"}
            headers = {
                'x-rapidapi-key': KEY[i],
                'x-rapidapi-host': "ocrly-image-to-text.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)
            if response.status_code > 200:
                continue
            else:
                return response.text

    @classmethod
    def get_data(cls, strategy_name):
        image_url = DropBox.get_image_url(strategy_name)
        message = cls.__image_to_text__(image_url)
        print(message)
        return (DataFromImage.get_datetime(message),
                DataFromImage.get_ratio(message),
                DataFromImage.get_position(message),
                DataFromImage.get_pair(message))

    # end of file
