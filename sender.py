import socket


class Sender:
    PORT = 55555
    LOCAL_IP = ""
    BUFFER_SIZE = 512
    HELP_DATA_SIZE = 16

    def __init__(self, destIP, packetSize, packetsCount):
        self.destIP = destIP
        self.packetSize = packetSize
        self.packetsSend = packetsCount
        self.packetsLost = None

        self.measureSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #self.measureSocket.setsockopt()

        self.helpSocket = socket.socket(socket.AF_INET, socket.SOL_SOCKET)

    def measure(self):
        print("Проверка запущена")
        packet = bytes(Sender.PACKET_SIZE)
        for i in range(Sender.PACKET_COUNT):
            try:
                self.measureSocket.send(packet, (self.destIP, Sender.PORT))
            finally:
                self.measureSocket.close()
        self.getResults()

    def getResults(self):
        print("Получение результатов")
        try:
            self.helpSocket.bind((Sender.LOCAL_IP, Sender.PORT))
            connection = self.helpSocket.accept()
            results = connection.recv(Sender.BUFFER_SIZE)
            receivedPackets = int.from_bytes(results[:Sender.HELP_DATA_SIZE // 2], byteorder='little')
            totalTime = int.from_bytes(results[Sender.HELP_DATA_SIZE // 2:], byteorder='little')

            self.packetsLost = self.packetsSend - receivedPackets
            self.speed = self.packetsSend * self.packetSize * 8 // totalTime
        finally:
            self.helpSocket.close()

    def printResults(self):
        print("Отправлено {} пакетов, потеряно {}".format(self.packetsSend, self.packetsLost))
        print("Потеряно {}%".format(self.packetsLost / self.packetsSend))
        print("Скорость {} кбит/с".format(self.speed))
