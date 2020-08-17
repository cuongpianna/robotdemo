import threading
import socket
from constant import UDP_IP_STATUS
from websocket import create_connection, WebSocket
import ssl
import base64

UDP_IP = '127.0.0.1'
PORT2 = 12346
ws_url = 'wss://192.168.1.64:9000/agency/downloadMedia'
ROBOT_CODE = 'R32124'

# ========================================================================================


def GET_STATUS():
    while True:
        try:
            socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            socket_udp.bind((UDP_IP, PORT2))
            msg_robot_status, addr = socket_udp.recvfrom(1024)
            if (addr[0] == UDP_IP_STATUS):
                print(msg_robot_status)
                ws = WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
                ws.connect()
                ws.send(base64.b64encode(bytes(msg_robot_status.decode('utf-8') + '#' + ROBOT_CODE, "utf-8")))
                ws.close()
            socket_udp.close()
        except:
            pass


if __name__ == '__main__':
    threading.Thread(target=GET_STATUS).start()
