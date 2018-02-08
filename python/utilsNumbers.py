# funtion to parse a integer from a string
def parseIntNumber(sValue):
    iRes = -1
    bRes = False
    try:
        iRes = int(sValue)
        bRes = True
    except ValueError:
        iRes = -1

    return bRes, iRes
