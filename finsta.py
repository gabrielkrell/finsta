from flask import Flask, render_template, request, url_for, redirect
import socket
import os
import subprocess
from itertools import repeat, groupby, count
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_url_path='')
Bootstrap(app)


# from stack overflow: https://stackoverflow.com/a/4500607/
def sorted_files(path):
    """Get all files in a directory, sorted by modify date (desc).
    Arguments:
        path {str} -- The path to a directory.
    Returns:
        list(str) -- A list of filenames, sorted by modification time.
    """
    def modification_time(f):
        return os.stat(os.path.join(path, f)).st_mtime
    return sorted(os.listdir(path), key=modification_time, reverse=True)


def get_chunks(iterable, size):
    """
    Splits an iterable into "size"-sized chunks. Ex: [0,1,2,3] --> [0,1,2],[3]
    Thanks to Daniel Lepage: code.activestate.com/recipes/303279/#c7
    Arguments:
        iterable -- Iterable to be split up
        size(int) -- Max size of each chunk
    """
    c = count()
    for k, g in groupby(iterable, lambda x: next(c) // size):
        yield g


@app.route('/')
def show_homepage():
    try:
        location = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'static',
            'images')
        latest_image = os.path.join('images', sorted_files(location)[0])
    except FileNotFoundError as e:
        latest_image = ""
    return render_template('homepage.html',
                           hostname=socket.gethostname(),
                           latest_image=latest_image)


@app.route('/shell')
def redirect_to_shellinabox():
    """Dummy method for /shell

    Apache will grab requests to /shell, so this should not run unless Finsta
    is being run with the Flask debugger thing.  In that case, we'll send the
    user back to the index (it should really show an error page).
    """
    return redirect(url_for('show_error_page'))


@app.route("/finsta")
def show_finsta_feed():
    location = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'static',
        'images')
    try:
        images = sorted_files(location)
    except FileNotFoundError as e:
        # let the camera make the folder later.
        images = ()
    image_paths = map(os.path.join, repeat('images'), images)
    image_chunks = get_chunks(image_paths, 3)
    return render_template('finsta.html', images=image_chunks)


@app.route("/error")
def show_error_page():
    return render_template('error.html')


@app.route("/update_hostname")  # , methods=['POST'])
def update_hostname():
    body = request.get_json()
    return request.environ['REMOTE_ADDR']
    return request.headers['X-Forwarded-For']
    return request.access_route
    """example body:
    {
        'hostname': hostname
    }
    """
    subprocess.run(['sudo', '/usr/sbin/change_hostname.sh', body['hostname']])


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
