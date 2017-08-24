from picamera import PiCamera, Color
from time import sleep
import datetime as dt

camera = PiCamera()

camera.resolution = (600, 600)
camera.annotate_background = Color ('white')
camera.annotate_foreground = Color ('blue')
camera.annotate_text_size = 12
date_str = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
camera.annotate_text = "Hello world! Anne  was here " + date_str
camera.start_preview()
camera.image_effect = 'watercolor'
sleep(5)
camera.capture('/home/pi/images/img_%s.jpg')
camera.stop_preview()
