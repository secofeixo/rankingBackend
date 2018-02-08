# -*- coding: utf-8 -*-
import logging
import json
import os.path
from loggerGS import loggerGS

class configServer(loggerGS):
    def __init__(self):
        loggerGS.__init__(self)
        self.__setDefaultValuesServer()
        self.__setDefaultValuesLogging()
        self.jsonConfig = None

    def __setDefaultValuesServer(self):
        # set defaults values to attributes of the object
        self.portServer = 4550
        self.numMaxConnections = 10
        self.maxDataSize = 2048
        self.numAttempsToConnect = 10

    def __setDefaultValuesLogging(self):
        self.logLevel = logging.INFO
        self.logger.setLevel(self.logLevel)

    def __loadConfigServer(self):
        # read from the config file read the data of the tcp server
        self.__setDefaultValuesServer()
        if ('server' not in self.jsonConfig):
            self.logger.info('config_server.py. __loadConfigServer. Using default values, key SERVER does not exists in config file')
            return

        server = self.jsonConfig['server']
        if ('port' in server):
            if (isinstance(server['port'], int)):
                port = int(server['port'])
                if (port > 0):
                    self.portServer = port
        if ('maxdatasize' in server):
            if (isinstance(server['maxdatasize'], int)):
                maxdatasize = int(server['maxdatasize'])
                if (maxdatasize > 0):
                    self.maxDataSize = maxdatasize
        if ('maxnumconnections' in server):
            if (isinstance(server['maxnumconnections'], int)):
                maxconnections = int(server['maxnumconnections'])
                if (maxconnections > 0):
                    self.numMaxConnections = maxconnections
        if ('numportstotry' in server):
            if (isinstance(server['numportstotry'], int)):
                numportstry = int(server['numportstotry'])
                if (numportstry > 0):
                    self.numAttempsToConnect = numportstry

    def __loadConfigLog(self):
        # read from the config file read the data of the log
        self.__setDefaultValuesLogging()
        if ('log' not in self.jsonConfig):
            self.logger.info('config_server.py. __loadConfigLog. Using default values, key LOG does not exists in config file')
            return
        log = self.jsonConfig['log']
        if ('level' in log):
            if (isinstance(log['level'], int)):
                level = int(log['level'])
                if (level >= 0):
                    self.logLevel = level
                    self.logger.setLevel(self.logLevel)

    def debuggingValues(self):
        # show in the logger the values read from the config file
        self.logger.debug("logLevel: %s", self.logLevel)
        self.logger.debug("maxDataSize: %s", self.maxDataSize)
        self.logger.debug("numAttemps: %s", self.numAttempsToConnect)
        self.logger.debug("maxConnections: %s", self.numMaxConnections)
        self.logger.debug("portServer: %s", self.portServer)

    def loadConfig(self, filename):
        # read the config file and parse it into json format
        if os.path.isfile(filename) is False:
            self.logger.error('config_server.py. loadConfig. File does not exists %s', filename)
            self.jsonConfig = None
            return False

        bOk = True
        try:
            with open(filename) as data_file:
                self.jsonConfig = json.load(data_file)
        except Exception:
            self.logger.error('config_server.py. loadConfig. Exception reading config file %s', filename)
            bOk = False
        else:
            self.__loadConfigLog()
            self.__loadConfigServer()
            self.logger.info('config_server.py. loadConfig. Reading config file %s OK', filename)

        return bOk
