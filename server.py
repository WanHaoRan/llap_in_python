import time
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

PORT = 1060

network = '192.168.1.255'
a = str(time.time())
s.sendto(a.encode('utf-8'),(network, PORT))
