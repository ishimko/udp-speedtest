import socket
from time import ctime

class Sender:
    PORT = 55555
    LOCAL_IP = ""
    BUFFER_SIZE = 512
    HELP_DATA_SIZE = 16

    def __init__(self, destIP, packetSize, packetsToSend):
        self.destIP = destIP
        self.packetSize = packetSize
        self.packetsToSend = packetsToSend
        self.packetsLost = None

        self.measureSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.helpSocket = socket.socket(socket.AF_INET, socket.SOL_SOCKET)

    def writeLog(self, msg):
        print("{}: {}".format(ctime(), msg))

    def measure(self):
        self.writeLog("проверка запущена")

        self.measureSocket.bind((Sender.LOCAL_IP, Sender.PORT))
        packet = bytes(self.packetSize)
        try:
            for i in range(self.packetsToSend):
                self.measureSocket.sendto(packet, (self.destIP, Sender.PORT))
                print("\r\t{}/{} отправлено".format(i+1, self.packetsToSend), end='')
        finally:
            self.measureSocket.close()
            print("")
        self.getResults()
        self.printResults()

    def getResults(self):
        self.writeLog("ожидание результатов")
        try:
            self.helpSocket.bind((Sender.LOCAL_IP, Sender.PORT))
            self.helpSocket.listen(1)

            connection, address = self.helpSocket.accept()
            results = connection.recv(Sender.BUFFER_SIZE)
            receivedPackets = int.from_bytes(results[:Sender.HELP_DATA_SIZE // 2], byteorder='little')
            totalTime = int.from_bytes(results[Sender.HELP_DATA_SIZE // 2:], byteorder='little')

            self.packetsLost = self.packetsToSend - receivedPackets
            self.speed = self.packetsToSend * self.packetSize * 8 // totalTime * 10**6 // 1024**2
        finally:
            self.helpSocket.close()

    def printResults(self):
        self.writeLog('результаты получены:')
        print("\tотправлено {} пакетов, потеряно {}".format(self.packetsToSend, self.packetsLost))
        print("\tпотеряно {}%".format(self.packetsLost / self.packetsToSend * 100))
        print("\tскорость {} мбит/с".format(self.speed))
