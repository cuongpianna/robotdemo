import threading
import socket
from constant import UDP_IP_STATUS, PORT2, UDP_PORT_STATUS
from websocket import create_connection
import base64

# ========================================================================================#

sock_get_status = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock_get_status.bind((UDP_IP_STATUS, 12349))


def GET_STATUS():
    while True:
        msg_robot_status, addr = sock_get_status.recvfrom(1024)
        if (addr[0] == UDP_IP_STATUS):
            print(msg_robot_status)
            ws = create_connection("ws://localhost:49411/downloadMedia")
            # ws = WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
            # ws.connect('wss://178.128.26.135/agency/downloadMedia')
            # ws = create_connection("wss://178.128.26.135/agency/downloadMedia")
            ws.send(base64.b64encode(bytes(msg_robot_status.decode('utf-8') + '#' + '127.0.0.1:8000', "utf-8")))
            ws.close()


if __name__ == '__main__':
    threading.Thread(target=GET_STATUS).start()
