import mss
from PIL import Image


def take_a_screenshot(screen_num, strategy_name):
    output_filename = f'main/static/images/{strategy_name}.png'
    print(strategy_name)
    with mss.mss() as mss_instance:
        monitor = mss_instance.monitors[screen_num]
        screenshot = mss_instance.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")  # Convert to PIL.Image
        img.save(output_filename, "PNG")  # Save the image


def preview_screenshot(strategy_name):
    output_filename = f'main/static/images/{strategy_name}.png'
    im = Image.open(output_filename)
    im.show()

#
# if __name__ == '__main__':
#     take_a_screenshot(1)
#     preview_screenshot()
