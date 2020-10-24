import threading
import socket
from constant import UDP_IP_STATUS
from websocket import create_connection, WebSocket
import ssl
import base64

UDP_IP = '127.0.0.1'
PORT2 = 12347
ws_url = 'wss://172.20.10.2:9000/agency/downloadMedia'
ROBOT_CODE = 'R32124'

# ========================================================================================


def GET_STATUS():
    while True:
        socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        socket_udp.bind((UDP_IP, PORT2))
        msg_robot_status, addr = socket_udp.recvfrom(1024)
        if (addr[0] == UDP_IP_STATUS):
            print(msg_robot_status)
            ws = WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
            ws.connect(ws_url)
            ws.send(base64.b64encode(bytes(msg_robot_status.decode('utf-8') + '#' + ROBOT_CODE, "utf-8")))
            ws.close()
        socket_udp.close()


if __name__ == '__main__':
    threading.Thread(target=GET_STATUS).start()