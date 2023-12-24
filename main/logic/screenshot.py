import mss
from PIL import Image
from main import LOCAL_IMAGE_ROOT_PATH


class FromScreenshot:

    @classmethod
    def take_a_screenshot(cls, strategy_name, screen_num):
        output_filename = LOCAL_IMAGE_ROOT_PATH + f'/{strategy_name}.png'
        with mss.mss() as mss_instance:
            monitor = mss_instance.monitors[screen_num]
            screenshot = mss_instance.grab(monitor)
            # Convert to PIL.Image
            img = Image.frombytes("RGB", screenshot.size,
                                  screenshot.bgra, "raw", "BGRX")
            img.save(output_filename, "PNG")  # Save the image

    @classmethod
    def preview_screenshot(cls, strategy_name):
        output_filename = LOCAL_IMAGE_ROOT_PATH + f'/{strategy_name}.png'
        im = Image.open(output_filename)
        im.show()

    # end of file
