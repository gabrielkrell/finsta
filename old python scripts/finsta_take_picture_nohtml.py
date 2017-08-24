from picamera import PiCamera, Color
from time import sleep
import datetime as dt

from flask import Flask, request, send_from_directory
import os

app = Flask(__name__, static_url_path='')


def sorted_image_list(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))

@app.route('/click')
def click():
    camera = PiCamera()
    camera.resolution = (600, 600)
    camera.annotate_background = Color ('pink')
    camera.annotate_foreground = Color ('blue')
    camera.annotate_text_size = 30
    date_str = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # camera.annotate_text = ' ' * 31
    camera.annotate_text += "FUSE Team wz here " + date_str
    camera.start_preview()
    camera.image_effect = 'saturation'
    sleep(2)
    camera.capture('/home/pi/images/img_%s.jpg' % date_str)
    camera.stop_preview()
    camera.close()
    return 'Success!'
    

@app.route('/images/<path:path>')
def show_image(path):
    return send_from_directory('images', path)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
