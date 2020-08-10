from flask import Flask, render_template
import socket
from constant import UDP_IP_STATUS, UDP_PORT_STATUS, IP_SERVER, ROBOT_CODE, IP_SEND_ROBOT, PORT_SEND_ROBOT, \
    VIDEO_CALL_URL, LOCAL_WS_FROM, SERVER_WS_FROM, IS_PRODUCT
from flask_socketio import SocketIO
from threading import Thread, Event
import requests
from websocket import create_connection
import base64

app = Flask(__name__)

socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()


def check_status():
    try:
        rq = requests.get(IP_SERVER, verify=False)
        if rq.status_code == 200:
            return True
        else:
            return False
    except:
        return False


def GET_STATUS():
    while True:
        sock_get_status = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock_get_status.bind((UDP_IP_STATUS, UDP_PORT_STATUS))
        msg_robot, addr = sock_get_status.recvfrom(35)
        if addr[0] == UDP_IP_STATUS:
            if check_status():
                status = 1
            else:
                status = 0
            msg_robot_status = msg_robot.decode('utf-8')
            msg_robot_status = msg_robot_status[1:]
            msg_robot_status = msg_robot_status.split('#')[2]
            socketio.emit('newUdp', {'number': str(msg_robot_status), 'status': status})
        sock_get_status.close()

        # ws = create_connection("ws://localhost:49411/downloadMedia")
        # ws.send(base64.b64encode(bytes(msg_robot.decode('utf-8') + '#' + '127.0.0.1:7000', "utf-8")))
        # print("Sent")
        # print("Receiving...")
        # result = ws.recv()
        # print("Received '%s'" % result)
        # ws.close()


def CHECK_CONNECTION():
    status = check_status()
    number = 1 if status else 0
    socketio.emit('tt', {'connection': number, 'udp': 0}, broadcast=True)


@app.route('/')
def index():
    status = True
    robot_code = ROBOT_CODE
    if IS_PRODUCT:
        ws_from = SERVER_WS_FROM
    else:
        ws_from = LOCAL_WS_FROM
    if status:
        classes = 'active'
    else:
        classes = 'deactive'
    return render_template('index.html', classes=classes, robot_code=robot_code, video_call_url=VIDEO_CALL_URL,
                           ws_from=ws_from)


@socketio.on('connect')
def test_connect():
    global thread
    print('Client connected')

    if not thread.isAlive():
        print("Starting Thread")
    thread = socketio.start_background_task(GET_STATUS)


@socketio.on('connection2')
def check_connect():
    print('Check connection!!!!!!')
    thread = socketio.start_background_task(CHECK_CONNECTION)


@socketio.on('disconnect')
def test_check_disconnect():
    print('Client disconnected!!!!!!!')


@socketio.on('leave')
def leave(message):
    value = message['value']
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(value.encode(), (IP_SEND_ROBOT, PORT_SEND_ROBOT))
    except:
        sock.close()
    finally:
        sock.close()


if __name__ == '__main__':
    socketio.run(app, port=7000)
