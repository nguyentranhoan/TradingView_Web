import requests

from main.logic.data_from_img import from_screenshot
from main.logic.from_dropbox import get_image_url
#
# img = get_image_url('Screenshot')
from_screenshot('harmonic')
# print(img)
# url = "https://microsoft-computer-vision3.p.rapidapi.com/ocr"
#
# querystring = {"detectOrientation": "false", "language": "en"}
#
# payload = "{\n\"url\": \"https://content.dropboxapi.com/apitl/1/AxJWva8pcEkpO5QnY9mXyyCewNCXVimGbAEzeB1160Fyx7y_Up9rk4QiDyfAhcyq_UL8lVPbWRAt45_rO8ShNjJFi0OUR4RLBzJN9VRt7n6yyCZ9_Wmx3qhC8-PeZS_nF5UlD61xXqYVLOFCxTBHI7pHH0HYAYlMFWvl9psvcDda9h-mgTRSY9Fqek9LZUxFbs6xgHs6-P8yDXaAsons5tqiY12H7LVoE2Al-3SjlbSyXEOKtlpC3G-VOSO7y-pWYVDj6LYrzSSpI_beaw23tCZ-4oUJJ0WCnDlxOs368xd74EY4WTKgBJs-HD4gT9H695V-aYdZE9ZAYQtpod2pttxbUBTaS7Met4nFHtUeM-EwnGx4YGpYs_F_lKCoOFhytVznk0Bk1Jm8azopLV_Xua-J\"\n}"
# headers = {
#     'content-type': "application/json",
#     'x-rapidapi-key': "cc9d56c945mshdec870cd8fe1c7ap1b1d5ejsne92957cff589",
#     'x-rapidapi-host': "microsoft-computer-vision3.p.rapidapi.com"
# }
#
# response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
#
# print(response.text)
