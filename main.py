#!/usr/bin/python3

import sys
from enum import Enum
from sender import Sender
from receiver import Receiver

class Mode(Enum):
    wait = 0
    connect = 1
    help = 2


def parseArgs(args):
    if len(args) < 2:
        return Mode.help

    if args[1].lower() == '-w':
        return Mode.wait,

    if args[1].lower() == '-c':
        if len(args) != 5:
            return Mode.help
        try:
            return Mode.connect, {"ip": args[2], "packet_size": int(args[3]), "packets_count": int(args[4])}
        except ValueError:
            return Mode.help


def fatalError(errorMsg):
    print("Ошибка: {}".format(errorMsg))
    exit(1)


def printHelp():
    print("""
            -w - ожидание сеанса измерения скорости
            -с [ip] [packet size] [packets count] - измерение скорости с ip, отправка packet count пакетов
            по packet size байт каждый
          """)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        printHelp()
    else:
        argsInfo = parseArgs(sys.argv)

        if argsInfo == Mode.help:
            printHelp()
        try:
            if argsInfo[0] == Mode.wait:
                receiver = Receiver()
                receiver.start()
            else:
                sender = Sender(destIP=argsInfo[1]["ip"], packetSize=argsInfo[1]["packet_size"],
                                packetsToSend=argsInfo[1]["packets_count"])
                sender.measure()
        except Exception as e:
            fatalError(e)

