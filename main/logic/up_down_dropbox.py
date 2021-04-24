from __future__ import print_function

import dropbox
from dropbox import files


def from_dropbox():
    access_token = '70JPeRBX8PcAAAAAAAAAAQ_xIdqzwa9G3w2Wt7Ub0CzwU4rk7e1rIxvPWVPM7Om0'
    dbx = dropbox.Dropbox(access_token)
    return dbx


def upload_image(dbx):
    # dbx = from_dropbox()
    file_from = 'main/static/images/screenshot.png'  # local file path
    file_to = '/TradingViewStorage/screenshot.png'      # dropbox path
    f = open(file_from, 'rb')
    dbx.files_upload(f.read(), file_to, mode=files.WriteMode.overwrite)


def get_image_url():
    dbx = from_dropbox()
    upload_image(dbx)
    tem = dbx.files_get_temporary_link('/TradingViewStorage/screenshot.png')
    return tem.link


# if __name__ == '__main__':
#     print(get_image_url())
