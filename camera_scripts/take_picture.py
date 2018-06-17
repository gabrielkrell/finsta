from helpful_tools import shielded_camera

from picamera import Color
from time import sleep
import datetime as dt


def click():
    """Take a picture!

    You can customize this function to do whatever you want to the picture.
    Run it from the terminal with
        python3 this_script.py
    """
    with shielded_camera() as camera:
        camera.annotate_background = Color('pink')
        camera.annotate_foreground = Color('blue')
        camera.annotate_text_size = 30
        date_str = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.annotate_text = "Took a picture at "
        camera.annotate_text += date_str
        camera.image_effect = 'none'
        # choices include none, negative, solarize, sketch, denoise,
        # emboss, oilpaint, hatch, gpen, pastel, watercolor, film, blur,
        # saturation, colorswap, washedout, posterise, colorpoint, cartoon

        sleep(2)  # wait for the camera to be ready
        camera.capture('img_%s.jpg' % date_str)
        print('You took a photo!')


if __name__ == "__main__":
    # when run from the command line, run the custom click().
    # You shouldn't change this code when making your own script.
    click()
