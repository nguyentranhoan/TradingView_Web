import requests

from main.logic.from_dropbox import DropBox
from datetime import datetime
import re
import os
import io
from google.cloud import vision
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "main/credentials.json"

KEY = ['b9b5df32f8msh948aa3b15534102p1ad977jsn6e47a84b40d3',
       '7ae890b37fmshe9523cf53d7b361p187537jsn61635bf55d64',
       '5dff3c7d5emshcfb7ca7eadc6111p156ac1jsn1825d021d248',
       'fb2e945d1fmsh1a14cb50e5e9a55p17de56jsnb81aefa62e2a',
       '3a3f154ed4mshab2dac338951432p196979jsn5a87096e7a9f',
       'c63dbfd753msh55284ac72561390p1fa9ddjsn59510c9faf51',
       '248a3c7ad6msh5f147c1d696da48p1d9c47jsnbd815bbf6cc2',
       '8e3563101emsh67b1813e250e8e5p1f5069jsn2f94c8890bd2',
       'e7a7011470msh918b1b4000f9ac4p18fb8bjsn253c915a8ac7',
       'addbae0c4bmshd72190c8418d504p134020jsnf7fa8d67a7af',
       '0c4bdee0eamshcf230e88ab126a0p1697bejsnffad01d3c6c7',
       '05559aab0amsh4c15eac0ff2f4d2p1ef3dfjsn1af89c0cdb48',
       '544764be9fmsh752065920e265a5p16ea8bjsn5ed7bb2693d7',
       'fe8419972fmsh52bbabe303e2d90p12a194jsn33bfd568025a',
       '0b14d9cdfemsh33fd4da7551016cp1b8b90jsn5be9eb1eda7a',
       "cd64c648b4msh8a6d48365b0374bp105766jsne7a29e5dfcb4",
       "0230adc154mshfbc439f7ddde556p17394fjsn0d3957abf5bb",
       "15c0cdeb68msh84cfd07b34f37f2p1e62c5jsn5d996c57049f",
       "b0ab8bf78bmshe29b4cc002d61b8p1f75e3jsnf7891e706414",
       "a90c0d3cc6mshd6b13374e81ca6dp10eee5jsnb3da9d892f76",
       "7a07324785mshd7629a8c8efe4f4p19062ajsn4a1826f8e863",
       "6627d1e7admshc18328b7979defdp16b966jsn4251afccb2be",
       "bdd6d36efamshd8646144399328dp18c730jsnc5719af5f850",
       "d85a671a1amshb80d6d19bb58cbdp119cd8jsnca4c8dc4e36d",
       "fdc37b4e6cmsh441f7cb1ecb529ep19d62bjsnc0789ed68ae7"]


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
        pattern_2 = r"\n(. |)[A-Z]{2}([A-Z]|\d|\S)(|\S)([A-Z]+|\d+|\n)"
        expected = re.search(pattern_2, shorten_message.group(0))
        result = expected.group(0).strip()
        if " " in result:
            result = result[2:]
        return result.strip()

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

    @staticmethod
    def detect_text(path):
        message = ""
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = client.text_detection(image=image)
        # print("\n######\n", response, "\n#######\n")
        texts = response.text_annotations
        # print(texts, "\n#####\n")
        for text in texts:
            # print('\n"{}"'.format(text.description))
            message += "\n" + text.description

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
        return message


    @classmethod
    def get_data(cls, strategy_name):
        # image_url = DropBox.get_image_url(strategy_name)
        img_path = "main/static/images/" + strategy_name + ".png"
        message = cls.detect_text(img_path)
        print(message)
        return (DataFromImage.get_datetime(message),
                DataFromImage.get_ratio(message),
                DataFromImage.get_position(message),
                DataFromImage.get_pair(message))

    # end of file
