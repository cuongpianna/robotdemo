import threading
import socket
from constant import UDP_IP_STATUS, PORT2, UDP_PORT_STATUS, ROBOT_CODE, LOCAL_WS, SERVER_WS, IS_PRODUCT
from websocket import create_connection
import base64

# ========================================================================================


def GET_STATUS():
    if IS_PRODUCT:
        ws_url = SERVER_WS
    else:
        ws_url = LOCAL_WS
    while True:
        try:
            socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            socket_udp.bind((UDP_IP_STATUS, 12349))
            msg_robot_status, addr = socket_udp.recvfrom(1024)
            if (addr[0] == UDP_IP_STATUS):
                print(msg_robot_status)
                ws = create_connection(ws_url)
                ws.send(base64.b64encode(bytes(msg_robot_status.decode('utf-8') + '#' + ROBOT_CODE, "utf-8")))
                ws.close()
            socket_udp.close()
        except:
            pass


if __name__ == '__main__':
    threading.Thread(target=GET_STATUS).start()
