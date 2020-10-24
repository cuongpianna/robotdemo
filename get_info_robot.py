import threading
import socket
from constant import UDP_IP_STATUS, ROBOT_CODE, WEBSOCKET_MEDIA, PORT_STATUS_ROBOT
from websocket import WebSocket
import base64
import ssl


def GET_STATUS():
    ws_url = WEBSOCKET_MEDIA

    while True:
        try:
            socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            socket_udp.bind((UDP_IP_STATUS, PORT_STATUS_ROBOT))
            msg_robot_status, addr = socket_udp.recvfrom(1024)
            if (addr[0] == UDP_IP_STATUS):
                print(msg_robot_status)
                ws = WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
                ws.connect(ws_url)
                ws.send(base64.b64encode(bytes(msg_robot_status.decode('utf-8') + '#' + ROBOT_CODE, "utf-8")))
                ws.close()
            socket_udp.close()
        except:
            print('ssss')
            pass


if __name__ == '__main__':
    threading.Thread(target=GET_STATUS).start()
