# from_dropbox.py

from __future__ import print_function
import os
import dropbox
from dropbox import files
from main import LOCAL_IMAGE_ROOT_PATH

DROPBOX_TradingViewStorage_ROOT_PATH = "/TradingViewStorage"


class DropBox:
    """
    This class is used to retrieve an image's url from dropbox.
    The image is the screenshot of a transaction.
    """

    @staticmethod
    def __get_access():
        access_token = os.environ.get('DROPBOX_ACCESS_KEY')
        dbx = dropbox.Dropbox(access_token)
        return dbx

    @staticmethod
    def __upload_image(dbx, strategy_name):
        file_from = LOCAL_IMAGE_ROOT_PATH + \
            f'/{strategy_name}.png'  # local file path
        file_to = DROPBOX_TradingViewStorage_ROOT_PATH + \
            f'/{strategy_name}.png'  # dropbox path
        f = open(file_from, 'rb')
        dbx.files_upload(f.read(), file_to, mode=files.WriteMode.overwrite)

    @classmethod
    def get_image_url(cls, strategy_name):
        dbx = cls.__get_access()
        cls.__upload_image(dbx, strategy_name)
        tem = dbx.files_get_temporary_link(
            DROPBOX_TradingViewStorage_ROOT_PATH + f'/{strategy_name}.png')
        return tem.link

    # end of file
