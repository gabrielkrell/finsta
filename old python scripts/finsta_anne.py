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
    camera.annotate_background = Color ('Orange')
    camera.annotate_foreground = Color ('Blue')
    camera.annotate_text_size = 40
    date_str = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # camera.annotate_text = ' ' * 31
    camera.annotate_text += “Dude! It's " + date_str
    camera.start_preview()
    camera.image_effect = ‘negative’
    #sleep(5)
    camera.capture('/home/pi/images/img_%s.jpg' % date_str)
    camera.stop_preview()
    return 'Success!'
    

@app.route('/images/<path:path>')
def show_image(path):
    return send_from_directory('images', path)

@app.route("/")
def finsta():
    html = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta http-equiv="refresh" content="30">
    <title>Anne WAS HERE</title>
    <style type="text/css" media="screen">
  * {192
    margin: 0px 0px 0px 0px;
    padding: 0px 0px 0px 0px;
  }

  body, html {
    padding: 3px 3px 3px 3px;

    background-color: white;

    font-family: Helvetica, Verdana, sans-serif;
    font-color: red;
    font-size: 40 pt;
    text-align: center;
  }

    </style>
  </head>
  <body>
 
<h1> Anne Was <a href="http://www.fusestudio.net"> Here </a> March 15, 2017 </h1>
<ul>
'''
    
    location = os.path.dirname(os.path.abspath(__file__)) + '/images/'
    images = sorted_image_list(location)
    for image in reversed(images):
        print(image)
        html += '  <li><img src="/images/' + os.path.basename(image) + '"></li>' + "\n"

    html += '''
</ul>
</body>
</html>
'''
    return html

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
