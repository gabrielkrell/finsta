import os
import socket
import subprocess
from itertools import count, groupby, repeat

from flask import (Flask, abort, jsonify, redirect, render_template, request,
                   url_for)

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
        abort(404)
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


@app.route("/latest_image")
def show_latest_image():
    try:
        location = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'static',
            'images')
        latest_image = os.path.join('images', sorted_files(location)[0])
        return redirect(latest_image)
    except FileNotFoundError:
        return "", 404


@app.route("/error")
def show_error_page():
    return render_template('error.html')


@app.route("/take_picture", methods=['POST'])
def take_picture():
    """Take a picture with default settings.

    To do: should we check that this command is coming from FUSE?
    """
    # note: a few months ago we ran into trouble running this stuff from Flask
    # due to some threading business.  Instead, we're going to run our
    # take_picture script directly.
    try:
        subprocess.run(
            ['python3', '/opt/finsta/camera_scripts/take_picture.py'],
            check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'returncode': e.returncode,
                        'stderr': str(e.stderr)}), 500
    else:
        return 'OK', 200


@app.route("/update_hostname", methods=['POST'])
def update_hostname():
    fuse_ip = socket.gethostbyname('rpis.fusestudio.net')
    request_ip = request.headers['X-Forwarded-For']
    if fuse_ip != request_ip:
        abort(403)  # only finsta-coordinator can change the pi's hostname

    hostname = request.get_json()['hostname']
    if not hostname:
        abort(400)  # can't change to a blank hostname or Bad Things happen

    try:
        subprocess.run(
            ['sudo', '/usr/sbin/change_hostname.sh', hostname],
            check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({'returncode': e.returncode}), 500
    else:
        return 'OK', 200


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
