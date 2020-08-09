import socket

localIP = "127.0.0.1"

localPort = 20001

msgFromClient = "@2#17#6#1.5#$"

bytesToSend = str.encode(msgFromClient)

serverAddressPort = (localIP, localPort)

bufferSize = 1024

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Send to server using created UDP socket

UDPClientSocket.sendto(bytesToSend, serverAddressPort)

msgFromServer = UDPClientSocket.recvfrom(bufferSize)

msg = "Message from Server {}".format(msgFromServer[0])

print(msg)