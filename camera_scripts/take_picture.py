from picamera import PiCamera, Color
from time import sleep
import datetime as dt


# click is a special function.  When you go to
# <the Pi's address>/take_picture/<this script's name>,
# it'll run.
def click():
    camera = PiCamera()
    camera.resolution = (600, 600)
    camera.annotate_background = Color('pink')
    camera.annotate_foreground = Color('blue')
    camera.annotate_text_size = 30
    date_str = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # camera.annotate_text = ' ' * 31
    camera.annotate_text += "gabe visits!" + date_str
    camera.start_preview()
    camera.image_effect = 'posterise'
    # choices include none, negative, solarize, sketch, denoise,
    # emboss, oilpaint, hatch, gpen, pastel, watercolor, film, blur,
    # saturation, colorswap, washedout, posterise, colorpoint, cartoon
    sleep(2)
    camera.capture('/home/pi/images/img_%s.jpg' % date_str)
    camera.stop_preview()
    camera.close()
    return 'You took a photo!'
