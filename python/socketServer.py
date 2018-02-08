# -*- coding: utf-8 -*-
import zmq
import threading
import logging
import socket

from manageRequest import manageRequest
from ranking import ranking
from loggerGS import loggerGS

ownLoggerGS = logging.getLogger()

# function that manage the query that arrives to the service in a thread
def manage_thread(message, socket=None, configFile=None):
    ownLoggerGS.info('socketServer. manage_thread. Received request %s', message)
    # do some 'work', manage the request
    request = manageRequest(socket=socket, configFile=configFile)
    sReturnValue = request.mananageRequest(message)
    socket.sendall(sReturnValue.encode())
    # close yhe socket client, We have send the message to the client
    socket.close()

class socketServer(loggerGS):
    def __init__(self, configFile):
        loggerGS.__init__(self)
        self.configFile = configFile
        self.context = None
        self.socket = None

    # create the server
    def initserver(self):
        self.logger.info('mainServer. initthread calculating ranking')
        ranking.initThreadCalculateRanking()

        self.logger.info('mainServer. initsocket')
        self.context = zmq.Context.instance()

        # we create the socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # We try to connect to bind the socket to the port
        bErrorBind = True
        iNumAttempts = 0
        # lopping trying to connect to a port and if it ocppied then try the next until self.configFile.numAttempsToConnect attempts
        while (bErrorBind and (iNumAttempts < self.configFile.numAttempsToConnect)):
            # create the string for creating the connection
            iPortConnection = self.configFile.portServer + iNumAttempts

            self.logger.info('mainServer. initserver. Scoket. Connection port: %s', iPortConnection)
            iNumAttempts += 1
            try:
                s.bind(("", iPortConnection))
            except Exception:
                # error trying to listen on the port specified
                self.logger.error('mainServer. initserver. Scoket. Exception binding')
            else:
                bErrorBind = False

        if bErrorBind:
            self.logger.error('mainServer. initserver. Scoket. error en bind()')
            return False

        # Aceept connections.
        s.listen(self.configFile.numMaxConnections)

        try:
            while 1:

                # we create a socket client connection and the addrs of the client connected
                sc, addr = s.accept()
                # We wait to receive a message from the client.
                data = sc.recv(self.configFile.maxDataSize)
                messageRecv = data.decode('utf-8')
                self.logger.info('mainServer. initsocket. Message received: %s', messageRecv)
                # create the htread to manage the request
                thread = threading.Thread(target=manage_thread, args=(messageRecv, sc, self.configFile))
                thread.start()
        finally:
            # close the socket connection
            s.close()
