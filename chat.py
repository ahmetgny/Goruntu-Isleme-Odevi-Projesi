from flask import Flask, Response
# Flask is a web framework, it lets you develop web applications and we use flask to use our program in browser.

import cv2
# Provides a common infrastructure for computer vision applications

import os
import subprocess
# We use subprocess to connect ana.py to ceviri.py
import time

app = Flask(__name__)
camera = cv2.VideoCapture(0)


def frameGeneration():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video')  # combines the frames from the upper function
def video():
    return Response(frameGeneration(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/capture')  # takes an image from the video stream, sends to translation code
def capture():
    success, frame = camera.read()

    if success:
        desktopPath = "/Users/ahmeteminguney/Desktop/"
        photoPath = os.path.join(desktopPath, "TARA.png")
        cv2.imwrite(photoPath, frame)

        time.sleep(1)

        subprocess.Popen(["python", "ceviri.py"])


if __name__ == "__main__":
    app.run(debug=True, port=5001)