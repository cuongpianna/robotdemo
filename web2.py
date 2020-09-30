from flask import Flask, render_template
import socket
from constant import UDP_IP_STATUS, UDP_PORT_STATUS, IP_SERVER, ROBOT_CODE, IP_SEND_ROBOT, PORT_SEND_ROBOT, \
    VIDEO_CALL_URL, WEBSOCKET_SEND_UDP, WEBSOCKET_MEDIA, API_DOWNLOAD_MEDIA, DOWNLOAD_MEDIA, \
    MEDIA_SERVER_HOST
from flask_socketio import SocketIO
from threading import Thread, Event
import requests
import json
import wget

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
        msg_robot, addr = sock_get_status.recvfrom(10)
        print(msg_robot)
        if addr[0] == UDP_IP_STATUS:
            if check_status():
                status = 1
            else:
                status = 0
            msg_robot_status = msg_robot.decode('utf-8')
            socketio.emit('newUdp', {'number': str(msg_robot_status), 'status': status})
        sock_get_status.close()


def CHECK_CONNECTION():
    status = check_status()
    number = 1 if status else 0
    socketio.emit('tt', {'connection': number, 'udp': 0}, broadcast=True)


@app.route('/')
def index():
    status = True
    robot_code = ROBOT_CODE
    ws_from = WEBSOCKET_SEND_UDP
    websocket_media = WEBSOCKET_MEDIA
    if status:
        classes = 'active'
    else:
        classes = 'deactive'
    return render_template('index.html', classes=classes, robot_code=robot_code, video_call_url=VIDEO_CALL_URL,
                           ws_from=ws_from, websocket_media=websocket_media)


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


@socketio.on('download')
def download(message):
    value = message['value']
    value = value.split('_')
    media_id = value[2]
    robot_id = value[3]
    res = requests.post(API_DOWNLOAD_MEDIA, json={
        'RobotId': robot_id,
        'MediaIds': [media_id]
    })
    res = json.loads(res.text)

    if res['records']:
        for record in res['records']:
            url_image = MEDIA_SERVER_HOST.format(record["fileName"])
            wget.download(url_image, DOWNLOAD_MEDIA.format(record["fileName"]))


if __name__ == '__main__':
    socketio.run(app, port=7000)
