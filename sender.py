import socket


class Sender:
    PORT = 55555
    LOCAL_IP = ''

    def __init__(self, destIP):
        self.destIP = destIP

        self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSocket.bind((Sender.LOCAL_IP, Sender.PORT))

    def measure(self):
        pass
