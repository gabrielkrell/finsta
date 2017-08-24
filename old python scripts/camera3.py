from picamera import PiCamera, Color
from time import sleep
import datetime as dt
 
camera = PiCamera()
 
camera.resolution = (600, 600)
camera.annotate_background = Color ('Red')
camera.annotate_foreground = Color ('White')
camera.annotate_text_size = 40
date_str = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# camera.annotate_text = ' ' * 31
camera.annotate_text += "Hi! It's " + date_str
camera.start_preview()
camera.image_effect = 'negative'
sleep(5)
camera.capture('/home/pi/images/img_%s.jpg' % date_str)
camera.stop_preview()
