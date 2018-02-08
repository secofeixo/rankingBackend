import json
import parseRanking
import utilsNumbers
import operator
import time
import threading

from loggerGS import loggerGS
from readWriteLock import ReadWriteLock

class ranking(loggerGS):
    lstRanking = []
    lstUsers = {}
    addedScore = False
    threadCalculating = None
    threadLogger = None

    lock = ReadWriteLock()

    def __init__(self):
        loggerGS.__init__(self)
        ranking.threadLogger = self.logger

    # method that creates the thread to update the ranking of the users
    @classmethod
    def initThreadCalculateRanking(self):
        ranking.threadCalculating = threading.Thread(target=ranking.calculateRanking)
        ranking.threadCalculating.start()

    # methos to alculate the ranking of the users
    @classmethod
    def calculateRanking(self):
        while 1:
            if (ranking.addedScore):
                time_i = time.time()
                ranking.lock.acquire_write()
                try:
                    ranking.lstRanking = sorted(ranking.lstUsers.items(),
                                                key=operator.itemgetter(1),
                                                reverse=True)
                    ranking.addedScore = False
                finally:
                    ranking.lock.release_write()
                batch_time = time.time() - time_i
                if (ranking.threadLogger is not None):
                    ranking.threadLogger.debug("ranking. calculateRanking. Time sort results = %f", batch_time)
                else:
                    print("ranking. calculateRanking. Time sort results = ", batch_time)
            # sleep the process one second. It can make that some queries
            # does not have the last results, but I think it is acceptable
            time.sleep(1)

    # return the array with the ranking
    def getRanking(self, parseRankingObj):
        if parseRankingObj.typeRanking == parseRanking.ABSOLUTE:
            self.logger.debug("ranking. getRanking. ABSOLUTE. Value %f", parseRankingObj.topValue)
            if (parseRankingObj.topValue > 0):
                iNumStart = parseRankingObj.skip
                iNumEnds = parseRankingObj.topValue
                if (parseRankingObj.limit > 0):
                    if ((iNumStart + parseRankingObj.limit) < parseRankingObj.topValue):
                        iNumEnds = iNumStart + parseRankingObj.limit

                ranking.lock.acquire_read()
                try:
                    lstAbsRanking = ranking.lstRanking[iNumStart:iNumEnds]
                finally:
                    ranking.lock.release_read()
                # json_string = json.dumps(dict(lstAbsRanking))
                somedict = [{'user': x[0], 'score': x[1], 'position': ranking.lstRanking.index(x) + 1} for x in lstAbsRanking]
                json_string = json.dumps(somedict)
                return json_string
        elif parseRankingObj.typeRanking == parseRanking.RELATIVE:
            ranking.lock.acquire_read()
            try:
                iNumUsers = len(ranking.lstRanking)
            finally:
                ranking.lock.release_read()
            self.logger.debug("ranking. getRanking. Num Users: %f ", iNumUsers)
            iNumStart = 0
            iNumEnds = iNumUsers
            if (parseRankingObj.relValue - parseRankingObj.relNumValues) > 0:
                iNumStart = parseRankingObj.relValue - parseRankingObj.relNumValues - 1
            if (parseRankingObj.relValue + parseRankingObj.relNumValues) < iNumUsers:
                iNumEnds = parseRankingObj.relValue + parseRankingObj.relNumValues

            self.logger.debug("ranking. getRanking. Relative. Start %f. Total: %f ", iNumStart, iNumEnds)
            if (iNumStart <= iNumEnds):
                # adding skip and limit
                iNumStart += parseRankingObj.skip
                if (parseRankingObj.limit > 0):
                    if ((iNumStart + parseRankingObj.limit) < iNumEnds):
                        iNumEnds = iNumStart + parseRankingObj.limit
                ranking.lock.acquire_read()
                try:
                    lstRelativeRanking = ranking.lstRanking[iNumStart:iNumEnds]
                finally:
                    ranking.lock.release_read()
                somedict = [{'user': x[0], 'score': x[1], 'position': ranking.lstRanking.index(x) + 1} for x in lstRelativeRanking]
                json_string = json.dumps(somedict)
                return json_string

        lstDummy = []
        json_string = json.dumps(lstDummy)
        return json_string

    # add a new score the to service
    def addScore(self, newScore):
        error = {}
        error['msg'] = "Not valid values"

        bTotal = False
        if ('user' not in newScore):
            return
        sUser = newScore['user']

        # check if the new score is a total score or an updating score
        if ('total' in newScore):
            bIsNumber, iTotal = utilsNumbers.parseIntNumber(newScore['total'])
            if (bIsNumber is False):
                return json.dumps(error)
            bTotal = True
        elif ('score' in newScore):
            bIsNumber, iPoints = utilsNumbers.parseIntNumber(newScore['score'])
            if bIsNumber is False:
                return json.dumps(error)
        else:
            return json.dumps(error)

        newScorePoints = 0
        if bTotal:
            # add a new total socre to the data
            newScorePoints = iTotal
            self.logger.debug("ranking. addScore. User %s. Total: %f ", sUser, iTotal)
            ranking.lock.acquire_write()
            try:
                ranking.lstUsers[sUser] = iTotal
                ranking.addedScore = True
            finally:
                ranking.lock.release_write()
        else:
            # first check if the user already exists or not.
            # if the user exists the score is updated
            # if the user does not exists the score is assigned as a total value
            if (sUser in ranking.lstUsers):
                self.logger.debug("ranking. addScore. User %s. Score: %f ", sUser, iPoints)
                ranking.lock.acquire_write()
                try:
                    ranking.lstUsers[sUser] += iPoints
                    newScorePoints = ranking.lstUsers[sUser]
                    ranking.addedScore = True
                finally:
                    ranking.lock.release_write()
            else:
                self.logger.debug("ranking. addScore. User doesn't exists. User %s. Score: %f ", sUser, iPoints)
                ranking.lock.acquire_write()
                try:
                    ranking.lstUsers[sUser] = iPoints
                    newScorePoints = iPoints
                    ranking.addedScore = True
                finally:
                    ranking.lock.release_write()

        newScore = {}
        newScore['score'] = newScorePoints

        return json.dumps(newScore)
