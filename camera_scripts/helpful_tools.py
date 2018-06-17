"""
This file contains tools to make your camera scripts easier. The example runs
code from this file.  You shouldn't need to edit this or make your own copy,
but it might be fun to look around.
"""
from picamera import PiCamera, PiCameraMMALError
from time import sleep
import os
from contextlib import contextmanager


def make_image_path(filename):
    """Returns the complete path to a new image with the given filename.
    """
    scripts_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(
        scripts_dir, os.path.pardir, 'static', 'images', filename)


@contextmanager
def shielded_camera():
    """Handle PiCamera opening/closing, retry logic and make capture() nicer.

    Open a PiCamera in our standard resolution, retrying if it's in use.  Patch
    capture() to take a file name instead of a complete path. After use, clean
    up with camera.close().
    :returns: a PiCamera instance
    :rtype: PiCamera
    """
    fail_count = 0
    while True:
        try:
            camera = PiCamera(resolution=(600, 600))
            camera._capture = camera._capture

            def capture_by_filename(self, filename):
                """Monkey-patch PiCamera's capture() to take a filename instead
                of a path.
                """
                self._capture(make_image_path(filename))
            camera.capture = capture_by_filename
            try:
                yield camera
            finally:
                camera.close()
            break
        except PiCameraMMALError:
            fail_count += 1
            print('Someone else is using the camera. Retrying... ({})'.format(
                fail_count))
            if fail_count == 5:  # Show this message only once
                print("Press Ctrl+C to cancel.")
            sleep(1)


if __name__ == "__main__":
    print("This script doesn't do anything by itself.  Try take_picture.py instead.")
