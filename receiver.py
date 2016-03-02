import socket
from _datetime import datetime

class Receiver:
    PORT = 55555
    LOCAL_IP = ""

    def __init__(self):
        self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSocket.bind((Receiver.IP, Receiver.PORT))

        #self.

    def recevive(self):
        print("Ождание начала измерения...")

        data, address = self.udpSocket.recvfrom(Receiver.BUFFER_SIZE)

        self.startTime = datetime.now()
        self.senderInfo = data, address
        self.udpSocket.settimeout(5.0)
        self.receivedPacketsCount = 0

        try:
            data, address = self.udpSocket.recvfrom(Receiver.BUFFER_SIZE)
            while True:
                self.receivedPacketsCount += 1
        except TimeoutError:

        finally:
            self.udpSocket.close()
