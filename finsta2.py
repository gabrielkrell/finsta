from flask import Flask, request, send_from_directory, render_template
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


@app.route('/take_picture/<filename>')
def take_pic(filename):
    import subprocess
    subprocess.call(filename)
    # execute script with filename


@app.route("/")
def finsta():
    location = os.path.dirname(os.path.abspath(__file__)) + '/images/'
    images = sorted_image_list(location)
    image_html = ""
    for image in reversed(images):
        image_html += '  <li><img src="/images/' + os.path.basename(image) + '"></li>' + "\n"
    return render_template('finsta.html', image_html=image_html)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
