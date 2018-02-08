from loggerGS import loggerGS
import utilsNumbers

NOT_SET = 0
ABSOLUTE = 1
RELATIVE = 2

class parseRanking(loggerGS):
    def __init__(self):
        loggerGS.__init__(self)
        self.__initValues()

    def __initValues(self):
        self.typeRanking = NOT_SET
        self.topValue = -1
        self.relValue = -1
        self.relNumValues = -1
        self.skip = 0
        self.limit = 0

    # internal function to show the value of this object, showing all its attributes
    def __str__(self):
        resStr = "typeRanking " + str(self.typeRanking) + "\n"
        resStr += "topValue " + str(self.topValue) + "\n"
        resStr += "relValue " + str(self.relValue) + "\n"
        resStr += "relNumValues " + str(self.relNumValues) + "\n"
        resStr += "skip " + str(self.skip) + "\n"
        resStr += "limit " + str(self.limit) + "\n"
        return resStr

    # parse if the query has skip and limit parameters
    def parsePageOptions(self, pageOptions):
        parameters = pageOptions.split('&')
        for parameter in parameters:
            sParamValue = parameter.split('=')
            if (len(sParamValue) == 2):
                if (sParamValue[0].lower() == "skip"):
                    bIsNumber, iNumber = utilsNumbers.parseIntNumber(sParamValue[1])
                    if (bIsNumber) and (iNumber >= 0):
                        self.skip = iNumber
                elif (sParamValue[0].lower() == "limit"):
                    bIsNumber, iNumber = utilsNumbers.parseIntNumber(sParamValue[1])
                    if (bIsNumber):
                        self.limit = iNumber

    # parse the query, in order to get values for the ranking query
    def parse(self, sValue):
        self.__initValues()

        pageOptions = sValue.split("&")
        if (len(pageOptions) > 1):
            self.parsePageOptions(pageOptions[1])
            sValue = pageOptions[0]

        if (sValue.startswith("Top")):
            sNumValue = sValue[3:]
            bIsNumber, iNumber = utilsNumbers.parseIntNumber(sNumValue)
            if (bIsNumber):
                self.typeRanking = ABSOLUTE
                self.topValue = iNumber
        else:
            if (sValue.startswith("At")):
                sValues = sValue[2:]
                valuesComponents = sValues.split("/")
                if (len(valuesComponents) == 2):
                    bIsNumber1, iNumber1 = utilsNumbers.parseIntNumber(valuesComponents[0])
                    bIsNumber2, iNumber2 = utilsNumbers.parseIntNumber(valuesComponents[1])
                    if (bIsNumber1 and bIsNumber2):
                        if (iNumber1 > 0) and (iNumber2 > 0):
                            self.typeRanking = RELATIVE
                            self.relValue = iNumber1
                            self.relNumValues = iNumber2
