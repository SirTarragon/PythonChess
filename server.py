import socket
import multiprocessing as mulproc
import time

serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

_SERVER = "localhost"
_PORT = 5555

_SERVER_IP = socket.gethostbyname(_SERVER)

try:
    serv.bind((_SERVER, _PORT))
except socket.error as e:
    print(str(e))