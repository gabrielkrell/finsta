from flask import Flask, request, send_from_directory
import os

app = Flask(__name__, static_url_path='')


def sorted_image_list(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))

@app.route('/images/<path:path>')
def show_image(path):
    return send_from_directory('images', path)

@app.route('/logos/<path:path>')
def show_underpants(path):
    return send_from_directory('logos', path)

@app.route("/")
def finsta():
    html = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta http-equiv="refresh" content="30">
    <title>Studio Finstagram</title>
    <link href="https://fonts.googleapis.com/css?family=Rancho" rel="stylesheet">
    <style type="text/css" media="screen">
  * {192
    margin: 0px 0px 0px 0px;
    padding: 0px 0px 0px 0px;
  }

  body, h1 {
    padding: 15px;
    background-color: white;
    font-family: 'Rancho', Helvetica, Verdana, sans-serif;
    color: gray;
    font-size: 1.5em;
    text-align: center;
  }

ul {
    list-style-type: none;
    margin: 1em;
}

img {
     border-width: thin;
     border-style: solid;
     border-color: gray;
     margin: 40px;
     padding: 30px;         
}

.logo {
     padding: 2px;
     border: none;
     height: 40px;
     margin: 0px;
     padding: 0px;
}
   
</style>
  </head>
  <body>
<img class="logo" src="/logos/FUSER.png">
<h1> Studio Finsta </a> </h1>
<hr style="margin:0; padding:0; background-color: #F7D25F; border: 0; height:1px;" />
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
    app.run(debug=True, host='0.0.0.0')
