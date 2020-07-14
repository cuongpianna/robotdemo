from flask import Flask, render_template, url_for, copy_current_request_context
import socket
from constant import UDP_IP_STATUS, PORT2, IP_SERVER
from flask_socketio import SocketIO
from threading import Thread, Event
import requests
from websocket import create_connection
from websocket import WebSocket
import base64
import ssl

__status =-1
sock_get_status = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock_get_status.bind((UDP_IP_STATUS, PORT2))

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

            # sock_net = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            # sock_net.sendto(bytes(msg_robot.decode('utf-8'), "utf-8"), ('127.0.0.1', 1111))
            # sock_net.close()

            # ws = create_connection("ws://localhost:49411/downloadMedia")
            ws = WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
            ws.connect('wss://178.128.26.135/agency/downloadMedia')
            ws.send(base64.b64encode(bytes(msg_robot.decode('utf-8') + '#' + '127.0.0.1:7000', "utf-8")))
            print("Sent")
            print("Receiving...")
            result = ws.recv()
            print("Received '%s'" % result)
            ws.close()


def CHECK_CONNECTION():
    status = check_status()
    number = 1 if status else 0
    socketio.emit('tt', {'connection': number, 'udp': 0}, broadcast=True)


@app.route('/')
def index():
    status = True
    if status:
        classes = 'active'
    else:
        classes = 'deactive'
    return render_template('index.html', classes = classes)


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
    global __status
    print(__status)
    thread = socketio.start_background_task(CHECK_CONNECTION)
@socketio.on('status')
def check_connect(sta):
    global __status
    __status =sta

@socketio.on('disconnect')
def test_check_disconnect():
    print('Client disconnected!!!!!!!')
    global __status
    __status =-1


if __name__ == '__main__':
    socketio.run(app, port=7000)
