import socket

class Client:
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "45.79.206.22"
        self.port = 5555
        self.color = self.connect()
    
    def connect(self) -> int:
        self.client.connect((self.host, self.port))
        return int(self.client.recv(2048).decode())
    
    def send(self, to_send: str) -> str:
        try:
            self.client.send(str.encode(to_send))
            return self.client.recv(2048).decode()
        except:
            print("error sending data")
