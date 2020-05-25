import threading
import socket

from base.browser_factory import WebDriverFactory
from constant import URL_BASE, URL_ENDPOINT
from constant import UDP_PORT_STATUS, UDP_IP_STATUS


def get_driver():
    print("Running one time setUp")
    wdf = WebDriverFactory('firefox')
    driver = wdf.get_web_driver_instance()
    return driver


driver = get_driver()

# ======================================================================================== #

sock_get_status = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
sock_get_status.bind((UDP_IP_STATUS, UDP_PORT_STATUS))


def GET_STATUS():
    while True:
        msg_robot_status, addr = sock_get_status.recvfrom(10)
        if (addr[0] == UDP_IP_STATUS):
            status = int(msg_robot_status)
            if status == 1:
                driver.get('{}?status={}'.format(URL_BASE, status))
            else:
                driver.get('{}?status={}'.format(URL_ENDPOINT, status))


if __name__ == '__main__':
    threading.Thread(target=GET_STATUS).start()
