from flask import Flask, render_template
import socket
from constant import UDP_IP_STATUS, UDP_PORT_STATUS, IP_SERVER
from flask_socketio import SocketIO
from flask_socketio import emit
from threading import Thread, Event
import requests
from tcping import Ping

__status =-1
sock_get_status = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock_get_status.bind((UDP_IP_STATUS, UDP_PORT_STATUS))

app = Flask(__name__)

socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

thread = Thread()
thread_stop_event = Event()

index = 0
first = 0
second = 1

def check_status():
    global first
    try:
        rq = requests.get(IP_SERVER, verify=False)
        if rq.status_code == 200:
            return True
        else:
            return False
    except:
        return False


def check_status2():
    ping = Ping(IP_SERVER)
    try:
        p = ping.ping(3)
        return True
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
            socketio.emit('newUdp', {'number': int(msg_robot_status), 'status': status})


def CHECK_CONNECTION():
    status = check_status()
    number = 1 if status else 0
    socketio.emit('tt', {'connection': number}, broadcast=True)


@app.route('/')
def index():
    status = check_status()
    if status:
        classes = 'active'
    else:
        classes = 'deactive'

    try:
        sock_get_status.settimeout(1.0)
        msg_robot_status, addr = sock_get_status.recvfrom(1024)
        msg_robot_status = int(msg_robot_status)
    except:
        msg_robot_status = 0

    print('-------------')
    print(msg_robot_status)

    if msg_robot_status == 0:
        msg = 'Chế độ điều khiển bằng tay'
        led = 'LED Base_Station  OFF + LED Manual_Mode ON'
    elif msg_robot_status == 1:
        if status:
            msg = 'Chế độ điều khiển bằng tay'
            led = 'LED Base_Station  OFF + LED Manual_Mode ON'
        else:
            msg = 'Đang ở Chế độ điều khiển bằng tay nhưng không có kết nối đến server'
            led = 'LED Base_Station  OFF + LED Manual_Mode ON'
    elif msg_robot_status == 2:
        if status:
            msg = 'Chế độ điều khiển bằng tay'
            led = 'LED Base_Station ON + LED Manual_Mode ON'
        else:
            msg = 'Đang ở Chế độ điều khiển bằng tay nhưng không có kết nối đến server'
            led = 'LED Base_Station ON + LED Manual_Mode ON'
    elif msg_robot_status == 3:
        if status:
            msg = 'Chế độ điều khiển tự động'
            led = 'LED Base_Station ON + LED Auto_Mode ON'
        else:
            msg = 'Đang ở Chế độ điều khiển tự động nhưng không có kết nối đến server'
            led = 'LED Base_Station ON + LED Auto_Mode ON'
    elif msg_robot_status == 4:
        if status:
            msg = 'Chế độ tự động bấm vạch từ'
            led = 'LED Base_Station ON + LED Auto_Following_Line_Mode ON'
        else:
            msg = 'Đang ở Chế độ tự động bấm vạch từ nhưng không có kết nối đến server'
            led = 'LED Base_Station ON + LED Auto_Following_Line_Mode ON'
    return render_template('index.html', classes = classes, msg=msg, led=led)


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
    global __status
    __status =-1


if __name__ == '__main__':
    socketio.run(app)
