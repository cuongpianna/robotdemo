from flask import Flask, render_template, url_for, copy_current_request_context
import random
import threading
import socket
from constant import UDP_IP_STATUS, UDP_PORT_STATUS, IP_SERVER
from flask_socketio import SocketIO
from threading import Thread, Event
import requests

sock_get_status = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock_get_status.bind((UDP_IP_STATUS, UDP_PORT_STATUS))

app = Flask(__name__)

socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()


def check_status():
    try:
        rq = requests.get(IP_SERVER)
        if rq.status_code == 200:
            return True
        else:
            return False
    except:
        return False


def GET_STATUS():
    while True:
        msg_robot_status, addr = sock_get_status.recvfrom(10)
        if addr[0] == UDP_IP_STATUS:
            if check_status():
                status = 1
            else:
                status = 0
            socketio.emit('newUdp', {'number': int(msg_robot_status), 'status': status}, namespace='/test')


@app.route('/')
def index():
    status = check_status()
    if status:
        classes = 'active'
    else:
        classes = 'deactive'
    return render_template('index.html', classes = classes)


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    print('Client connected')

    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(GET_STATUS)


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
