import socket
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 12345

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(20)
    print(data)