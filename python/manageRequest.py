# -*- coding: utf-8 -*-
import json
from loggerGS import loggerGS
import parseRanking
from ranking import ranking
import utilsNumbers

class manageRequest(loggerGS):

    def __init__(self, socket, configFile):
        loggerGS.__init__(self)
        self.socket = socket
        self.configFile = configFile
        self.globalQuery = None
        self.jsonQuery = None

    # check if the query is for adding score. It checks that the string is a
    # valid json object. It also checks if the json objects has the attributes
    # user and total or scores, and if this two last are valid numbers
    def __isAddingScore(self):
        bErrorConvertingStringToJSON = False
        try:
            self.jsonQuery = json.loads(self.globalQuery)
            if not isinstance(self.jsonQuery, dict):
                bErrorConvertingStringToJSON = True
        except Exception:
            self.logger.error("manageRequest %s. __isAddingScore. Error reading json.", self.globalQuery)
            bErrorConvertingStringToJSON = True

        if bErrorConvertingStringToJSON is False:
            self.logger.error("manageRequest. __isAddingScore. json: %s", self.jsonQuery)
            if ('user' not in self.jsonQuery):
                return None
            if (self.jsonQuery['user'].strip() == ""):
                return None

            bHasTotal = ('total' in self.jsonQuery)
            bHasScore = ('score' in self.jsonQuery)
            if (bHasTotal):
                bIsNumber, iNumber = utilsNumbers.parseIntNumber(self.jsonQuery['total'])
                if (bIsNumber):
                    return self.jsonQuery
            if (bHasScore):
                bIsNumber, iNumber = utilsNumbers.parseIntNumber(self.jsonQuery['score'])
                if (bIsNumber):
                    return self.jsonQuery

        return None

    # add the ascore to the service
    def __addingScore(self, score):
        self.logger.info("manageRequest __addingScore. %s", score)
        rankingObj = ranking()
        return rankingObj.addScore(score)

    # check if query is a ranking
    def __isRanking(self):
        parseRankingObj = parseRanking.parseRanking()
        parseRankingObj.parse(self.globalQuery)
        if (parseRankingObj.typeRanking != parseRanking.NOT_SET):
            return parseRankingObj
        return None

    # get the ranking
    def __ranking(self, parseRanking):
        self.logger.info("manageRequest __ranking. %s", parseRanking)
        rankingObj = ranking()
        return rankingObj.getRanking(parseRanking)

    # manage a request. Check which type of request it is, and call the properly functions
    def mananageRequest(self, sGlobalQuery):
        self.globalQuery = sGlobalQuery  # .decode('utf-8')

        self.logger.debug("manageRequest. mananageRequest. Query %s ", self.globalQuery)
        newScore = self.__isAddingScore()
        parseRanking = self.__isRanking()

        if (newScore is not None):
            return self.__addingScore(newScore)

        if (parseRanking is not None):
            return self.__ranking(parseRanking)

        error = {}
        error['msg'] = "Invalid operation"
        return json.dumps(error)
