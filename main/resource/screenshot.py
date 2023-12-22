import mss
from PIL import Image
from flask import request
from flask_restful import Resource

ROOT_FOLDER = "main/static/images/"


class TransactionScreenshot(Resource):
    """
    This class is used to take the wanted transaction screenshot.
    The image can be review by calling get() method.
    """
    @classmethod
    def get(cls, strategy_name: str):
        output_filename = ROOT_FOLDER + f'{strategy_name}.png'

        try:
            im = Image.open(output_filename)
        except FileNotFoundError:
            return {"message": FileNotFoundError}, 500
        im.show()

        return {"message": "image shown successfully"}, 200

    @classmethod
    def post(cls, strategy_name: str):
        data_json = request.get_json()

        screen_num = int(data_json['screen_num'])

        output_filename = ROOT_FOLDER + f'{strategy_name}.png'
        with mss.mss() as mss_instance:
            try:
                monitor = mss_instance.monitors[screen_num]
            except IndexError:
                return {"message": "screen number is out of range"}, IndexError, 500
            screenshot = mss_instance.grab(monitor)
            # Convert to PIL.Image
            img = Image.frombytes("RGB", screenshot.size,
                                  screenshot.bgra, "raw", "BGRX")
            try:
                img.save(output_filename, "PNG")  # Save the image
            except FileNotFoundError:
                return {"message": FileExistsError}, 500

        return {"message": "image taken successfully"}, 200

    # end of file
