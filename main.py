import sys
from enum import Enum


class Mode(Enum):
    wait = 0
    connect = 1


def parseArgs(args):
    if len(args) < 2:
        return -1

    if args[1].lower() == '-w':
        return Mode.wait,

    if args[1].lower() == '-c':
        if len(args) != 5:
            return -1
        try:
            return Mode.connect, (args[2], args[3], args[4])
        except ValueError:
            return -1



def fatalError(errorMsg):
    print("Ошибка: {}".format(errorMsg))
    exit(1)


def printHelp():
    print("""
            -w - ожидание сеанса измерения скорости
            -с - подключ
          """)


if __name__ == "__main__":
    argsInfo = parseArgs(sys.argv)

    if argsInfo == -1:
        fatalError("Некорректные параметры параметров!")

    if argsInfo[0] == Mode.wait:
        pass
    else:
        pass
