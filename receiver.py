import socket
from _datetime import datetime
from time import ctime

class Receiver:
    PORT = 55555
    LOCAL_IP = ""
    BUFFER_SIZE = 512
    HELP_DATA_SIZE = 16
    TIMEOUT = 10.0

    def __init__(self):
        self.measureSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.helpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.startTime = None
        self.endTime = None
        self.clientInfo = None
        self.totalTime = 0

        self.receivedPacketsCount = 0

    def writeLog(self, msg):
        print("{}: {}".format(ctime(), msg))

    def start(self):
        self.writeLog("ожидание подключения")
        try:
            self.measureSocket.bind((Receiver.LOCAL_IP, Receiver.PORT))

            data, self.clientInfo = self.measureSocket.recvfrom(Receiver.BUFFER_SIZE)
            self.receivedPacketsCount += 1
            self.startTime = datetime.now()
            self.writeLog("проверка запущена")

            self.measureSocket.settimeout(Receiver.TIMEOUT)

            while True:
                self.measureSocket.recv()
                self.receivedPacketsCount += 1
                self.endTime = datetime.now()
        except TimeoutError:
            self.writeLog("проверка завершена")
            self.totalTime = self.endTime - self.startTime
        finally:
            self.measureSocket.close()

    def sendResults(self):
        self.writeLog("отправка результатов")
        try:
            self.helpSocket.bind((Receiver.LOCAL_IP, Receiver.PORT))
            self.helpSocket.connect(self.clientInfo)

            results = bytes(Receiver.HELP_DATA_SIZE)

            results[:Receiver.HELP_DATA_SIZE // 2] = self.receivedPacketsCount.to_bytes(Receiver.HELP_DATA_SIZE // 2,
                                                                                        byteorder='little')
            results[Receiver.HELP_DATA_SIZE // 2:] = self.totalTime.seconds.to_bytes(Receiver.HELP_DATA_SIZE // 2,
                                                                                     byteorder='little')

            self.helpSocket.send(results)
        finally:
            self.helpSocket.close()
