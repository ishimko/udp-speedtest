import socket


class Sender:
    PORT = 55555
    LOCAL_IP = ''

    def __init__(self, destIP):
        self.destIP = destIP

        self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpSocket.bind((Sender.LOCAL_IP, Sender.PORT))

    def measure(self):
        packet = bytes(Sender.PACKET_SIZE)
        for i in range(Sender.PACKET_COUNT):
            try:
                self.udpSocket.send(packet, (self.destIP, Sender.PORT))
            finally:
                self.udpSocket.close()

    def printResults(self):
        print("Отправлено {} пакетов, потеряно {}".format())
        print("Потеряно {}".format())
        print("Скорость {} кбит/с".format())
