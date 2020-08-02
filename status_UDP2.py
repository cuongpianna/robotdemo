import threading
import socket
from time import sleep
from constant import UDP_IP_STATUS, PORT2


sock_send_status = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock_send_status.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def SEND_STATUS():
    global robot_status, robot_status_updated
    robot_status_updated = 0
    while True:
        if robot_status_updated:
            robot_status_updated = 0
            msg_send = str(robot_status)
            sock_send_status.sendto(''.join(msg_send).encode(), (UDP_IP_STATUS, PORT2))

threading.Thread(target=SEND_STATUS).start()

def TEST_LOOP():
    global robot_status, robot_status_updated
    cnt = 0
    robot_status = 1
    while True:
        sleep(0.1)
        cnt = cnt + 1
        if cnt == 1:
            robot_status = '@5#14#0#1#800#876#90#0#0#0#95#1' # KHONG ket noi voi tram dieu khien trung tam + Che do DK bang tay
            robot_status_updated = 1
        elif cnt == 20:
            robot_status = '@5#14#1#1#1100#876#90#0#0#0#94#1'  # Ket noi tram dieu khien trung tam + Che do DK bang tay
            robot_status_updated = 1
        elif cnt == 40:
            robot_status = '@5#14#1#1#1300#876#90#0#0#0#93#1'  # Ket noi tram dieu khien trung tam + Che do tu dong
            robot_status_updated = 1
        elif cnt == 60:
            robot_status = '@5#14#1#1#1550#876#90#0#0#0#92#1'  # Ket noi tram dieu khien trung tam + Che do tu dong bam vach tu
            robot_status_updated = 1
        elif cnt == 80:  # reset loop
            robot_status = '@5#14#1#1#1750#876#90#0#0#0#92#1'  # Ket noi tram dieu khien trung tam + Che do tu dong bam vach tu
            robot_status_updated = 1
        elif cnt == 100:  # reset loop
            robot_status = '@5#14#1#1#2000#876#90#0#0#0#92#1'  # Ket noi tram dieu khien trung tam + Che do tu dong bam vach tu
            robot_status_updated = 1
        elif cnt == 120:  # reset loop
            robot_status = '@5#14#1#1#2250#876#90#0#0#0#92#1'  # Ket noi tram dieu khien trung tam + Che do tu dong bam vach tu
            robot_status_updated = 1
        elif cnt == 140:  # reset loop
            robot_status = '@5#14#1#1#2450#876#90#0#0#0#92#1'  # Ket noi tram dieu khien trung tam + Che do tu dong bam vach tu
            robot_status_updated = 1
        elif cnt == 160:  # reset loop
            robot_status = '@5#14#1#1#2700#876#90#0#0#0#92#1'  # Ket noi tram dieu khien trung tam + Che do tu dong bam vach tu
            robot_status_updated = 1
        elif cnt == 180:  # reset loop
            robot_status = '@5#14#1#1#2900#876#90#0#0#0#92#1'  # Ket noi tram dieu khien trung tam + Che do tu dong bam vach tu
            robot_status_updated = 1
        elif cnt == 200:  # reset loop
            robot_status = '@5#14#1#1#3150#876#90#0#0#0#92#1'  # Ket noi tram dieu khien trung tam + Che do tu dong bam vach tu
            robot_status_updated = 1
        elif cnt == 220:  # reset loop
            robot_status = '@5#14#1#1#3350#876#90#0#0#0#92#1'  # Ket noi tram dieu khien trung tam + Che do tu dong bam vach tu
            robot_status_updated = 1
        elif cnt == 240:  # reset loop
            robot_status = '@5#14#1#1#3600#876#90#0#0#0#92#1'  # Ket noi tram dieu khien trung tam + Che do tu dong bam vach tu
            robot_status_updated = 1
        elif cnt == 260:  # reset loop
            robot_status = '@5#14#1#1#3780#776#0#0#0#0#92#1'  # Ket noi tram dieu khien trung tam + Che do tu dong bam vach tu
            robot_status_updated = 1
        elif cnt == 280:  # reset loop
            robot_status = '@5#14#1#1#3780#366#180#0#0#0#92#1'  # Ket noi tram dieu khien trung tam + Che do tu dong bam vach tu
            robot_status_updated = 1
        # elif cnt == 300:  # reset loop
        #     robot_status = '@5#14#1#1#3780#776#90#0#0#0#92#1'
        #     robot_status_updated = 1
        elif cnt == 320:
            cnt = 0
        print(robot_status)


# ====================================== MAIN PROGRAM ============================#
if __name__ == '__main__':
    try:
        TEST_LOOP()
    except:
        pass
