from flask import Flask, render_template
from constant import UDP_IP_STATUS, UDP_PORT_STATUS, IP_SERVER, DOWNLOAD_MEDIA, API_DOWNLOAD_MEDIA, ROBOT_CODE, \
    VIDEO_CALL_URL, MEDIA_SERVER_HOST, WEBSOCKET_MEDIA, WEBSOCKET_SEND_UDP, IP_SEND_ROBOT, PORT_SEND_ROBOT
from flask_socketio import SocketIO
from threading import Thread, Event
import requests
requests.packages.urllib3.disable_warnings()
import json
import wget
import socket
from websocket import WebSocket
import base64
import ssl


__status = -1

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
        msg_robot_status, addr = sock_get_status.recvfrom(10)
        if addr[0] == UDP_IP_STATUS:
            if check_status():
                status = 1
            else:
                status = 0
            socketio.emit('newUdp', {'number': int(msg_robot_status), 'status': status})
        sock_get_status.close()


def CHECK_CONNECTION():
    status = check_status()
    number = 1 if status else 0
    socketio.emit('tt', {'connection': number, 'udp': 0}, broadcast=True)


@app.route('/')
def index():
    status = check_status()
    robot_code = ROBOT_CODE
    ws_from = WEBSOCKET_SEND_UDP
    websocket_media = WEBSOCKET_MEDIA
    classes = 'active'
    return render_template('index.html', classes=classes, robot_code=robot_code, video_call_url=VIDEO_CALL_URL,
                           ws_from=ws_from, websocket_media=websocket_media)


@socketio.on('connect')
def test_connect():
    global thread
    print('Client connected')

    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(GET_STATUS)


@socketio.on('status')
def check_connect(sta):
    global __status
    __status = sta


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
    ws_url = WEBSOCKET_MEDIA
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
            print('DONWWLOAD ANH')
            url_image = MEDIA_SERVER_HOST.format(record["fileName"])
            wget.download(url_image, DOWNLOAD_MEDIA.format(record["fileName"]))
        ws = WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
        ws.connect(ws_url)
        ws.send(base64.b64encode(bytes('reload_' + ROBOT_CODE, "utf-8")))
        ws.close()


if __name__ == '__main__':
    socketio.run(app)
