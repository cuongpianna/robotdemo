import threading
import socket
from constant import UDP_IP_STATUS, UDP_PORT_STATUS

# ========================================================================================#

sock_get_status = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock_get_status.bind(('127.0.0.1', 1111))


def GET_STATUS():
    while True:
        msg_robot_status, addr = sock_get_status.recvfrom(35)
        if (addr[0] == UDP_IP_STATUS):
            print(msg_robot_status)


if __name__ == '__main__':
    threading.Thread(target=GET_STATUS).start()