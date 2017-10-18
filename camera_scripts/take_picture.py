from picamera import PiCamera, Color, PiCameraMMALError
from time import sleep
import datetime as dt
import os


def get_full_image_name(filename):
    """Returns the path to a new image with the given filename.
       You shouldn't change this function when making your own script.
    """
    scripts_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(
        scripts_dir, os.path.pardir, 'static', 'images', filename)


def start_camera():
    """Starts up the camera, retrying if it's currently in use.
       You shouldn't change this function when making your own script.
    """
    while True:
        try:
            return PiCamera(resolution=(600, 600))
            break
        except PiCameraMMALError:
            print('Someone else is using the camera. Retrying...')
            sleep(1)


def click():
    """Take a picture!

    You can customize this function to do whatever you want to the picture.
    Run it from the terminal with
        python3 this_script.py
    """
    try:
        camera = start_camera()
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
        camera.capture(get_full_image_name('img_%s.jpg' % date_str))
        print('You took a photo!')
    finally:
        # even if picture fails, make sure the next person can use the camera
        camera.close()


if __name__ == "__main__":
    # when run from the command line, run the custom click().
    # You shouldn't change this code when making your own script.
    click()
