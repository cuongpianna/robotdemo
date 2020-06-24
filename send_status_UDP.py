import threading
from threading import Timer, Thread, Event
import socket
from time import sleep
from constant import UDP_IP_STATUS, UDP_PORT_STATUS

UDP_IP_STATUS = '127.0.0.1'
UDP_PORT_STATUS = 12345


class QQTimer():
    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def stop(self):
        self.thread.cancel()


sock_send_status = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock_send_status.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def SEND_STATUS():
    global robot_status, robot_status_updated, status_cnt, cnt
    robot_status_updated = 0
    while True:
        if robot_status_updated:
            robot_status_updated = 0
            # Gui len UDP khi flag status_cnt bat tu 0 len 1
            if status_cnt:
                status_cnt = 0
                msg_send = str(robot_status)
                sock_send_status.sendto(''.join(msg_send).encode(), (UDP_IP_STATUS, UDP_PORT_STATUS))
                print(msg_send)


threading.Thread(target=SEND_STATUS).start()


def TEST_LOOP():
    global robot_status, robot_status_updated, status_cnt
    cnt = 0
    cnt_1 = 0
    robot_status = 1
    status_cnt = 0
    while True:
        sleep(0.1)
        # Tao ra dieu kien de gui trang thai qua UDP
        cnt_1 = cnt_1 + 1
        if cnt_1 > 10:
            status_cnt = 1;
            cnt_1 = 0

        # Tao ra trang thai gia lap
        cnt = cnt + 1
        robot_status_updated = 1
        if cnt == 1:
            robot_status = 1  # KHONG ket noi voi tram dieu khien trung tam + Che do DK bang tay
        elif cnt == 500:
            robot_status = 2  # Ket noi tram dieu khien trung tam + Che do DK bang tay
        elif cnt == 1000:
            robot_status = 3  # Ket noi tram dieu khien trung tam + Che do tu dong
        elif cnt == 1500:
            robot_status = 4  # Ket noi tram dieu khien trung tam + Che do tu dong bam vach tu
        elif cnt == 2000:  # reset loop
            cnt = 0


# ====================================== MAIN PROGRAM ============================#
if __name__ == '__main__':
    try:
        TEST_LOOP()
    except:
        pass
