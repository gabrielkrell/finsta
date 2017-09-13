from flask import Flask, send_from_directory, render_template, url_for, redirect
import socket
import os
import sys
from importlib import import_module

app = Flask(__name__, static_url_path='')


# from stack overflow: https://stackoverflow.com/a/4500607/
def sorted_files(path):
    """Get all files in a directory, sorted by modify date (desc).
    Arguments:
        path {str} -- The path to a directory.
    Returns:
        list(str) -- A list of files, sorted by modification time.
    """
    def modification_time(f):
        return os.stat(os.path.join(path, f)).st_mtime
    return sorted(os.listdir(path), key=modification_time, reverse=True)


@app.route('/')
def show_homepage():
    return render_template('homepage.html', hostname=socket.gethostname())


@app.route('/shell')
def redirect_to_shellinabox():
    """Dummy method for /shell

    Apache will grab requests to /shell, so this should not run unless Finsta
    is being run with the Flask debugger thing.  In that case, we'll send the
    user back to the index (it should really show an error page).
    """
    return redirect(url_for('show_homepage'))


@app.route('/images/<path:path>')
def show_image(path):
    return send_from_directory('images', path)


@app.route('/logos/<path:path>')
def show_logo(path):
    return send_from_directory('logos', path)


@app.route('/take_picture/<filename>')
def take_pic(filename):
    qualified_name = 'camera_scripts.{0}'.format(filename)
    if qualified_name in sys.modules:
        del sys.modules[qualified_name]
    student_script = import_module(qualified_name)
    try:
        student_script.click()
    except Exception:
        return "oops (this will show the stack trace later)"
    finally:
        return "Ran the {0}.py script successfully.".format(filename)


# todo: fix when no images directory
@app.route("/finsta")
def show_finsta_feed():
    location = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'images')
    images = sorted_files(location)
    image_paths = ['/images/' + os.path.basename(image) for image in images]
    print(image_paths)
    return render_template('finsta.html', images=image_paths)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
