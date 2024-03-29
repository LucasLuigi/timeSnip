# -*-coding:Latin-1 -*

class logPrint:

    # Debug level :
    #   0 : debug
    #   1 : log
    #   2 : error and informations
    logLevel = 2

    def __init__(self, debugLevel=2):
        if (debugLevel >= 0 and debugLevel <= 2):
            logPrint.logLevel = debugLevel
        else:
            logPrint.printError(
                "[ERR] debugLevel has not a correct value, "+debugLevel)
        pass

    def printDebug(cls, value):
        if (logPrint.logLevel == 0):
            print("[DBG] "+value)
        else:
            pass

    printDebug = classmethod(printDebug)

    def printLog(cls, value):
        if (logPrint.logLevel <= 1):
            print("[LOG] "+value)
        else:
            pass

    printLog = classmethod(printLog)

    def printError(cls, value):
        if (logPrint.logLevel <= 2):
            print("[ERR] "+value)
        else:
            pass

    printError = classmethod(printError)

    def printInfo(cls, value):
        if (logPrint.logLevel <= 2):
            print("[INF] "+value)
        else:
            pass

    printInfo = classmethod(printInfo)
