from flask import Flask, render_template, url_for, copy_current_request_context
import random
import threading
import socket
from constant import UDP_IP_STATUS, UDP_PORT_STATUS
from flask_socketio import SocketIO
from threading import Thread, Event

sock_get_status = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock_get_status.bind((UDP_IP_STATUS, UDP_PORT_STATUS))

app = Flask(__name__)

socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()


def GET_STATUS():
    while True:
        msg_robot_status, addr = sock_get_status.recvfrom(10)
        if (addr[0] == UDP_IP_STATUS):
            print(msg_robot_status)
            status_list = [0, 1]
            status = random.choice(status_list)
            socketio.emit('newUdp', {'number': int(msg_robot_status), 'status': status}, namespace='/test')


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(GET_STATUS)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)

