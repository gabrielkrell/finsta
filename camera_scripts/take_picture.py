from picamera import PiCamera, Color
from time import sleep
import datetime as dt
import os


def get_full_image_name(filename):
    """Returns the path to a new image with the given filename.
       You shouldn't change this function when making your own script.
    """
    scripts_dir = os.path.dirname(os.path.realpath(__file__))
    finsta_dir = os.path.pardir(scripts_dir)
    return os.path.join(finsta_dir, 'static', 'images', filename)


def click():
    """Take a picture!

    You can customize this function to do whatever you want to the picture.
    Run it by going to http://your.pi's.address/take_picture/this.script's.name
    """
    camera = PiCamera()
    camera.resolution = (600, 600)
    camera.annotate_background = Color('pink')
    camera.annotate_foreground = Color('blue')
    camera.annotate_text_size = 30
    date_str = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # camera.annotate_text = ' ' * 31
    camera.annotate_text += date_str
    camera.start_preview()
    camera.image_effect = 'posterise'
    # choices include none, negative, solarize, sketch, denoise,
    # emboss, oilpaint, hatch, gpen, pastel, watercolor, film, blur,
    # saturation, colorswap, washedout, posterise, colorpoint, cartoon
    sleep(2)
    camera.capture(get_full_image_name('img_%s.jpg' % date_str))
    camera.stop_preview()
    camera.close()
    return 'You took a photo!'
