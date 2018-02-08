# -*- coding: utf-8 -*-
import logging
from configServer import configServer
from socketServer import socketServer

# configure the logging system with default values
logging.basicConfig(format='%(asctime)s. %(levelname)s. %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
loggerGS = logging.getLogger()

def main():
    pathConfigFile = 'config.json'
    configFile = configServer()
    # read config file
    if configFile.loadConfig(pathConfigFile):
        # show config values
        configFile.debuggingValues()

        # create mainserver
        mainServerObj = socketServer(configFile=configFile)
        # init main server
        mainServerObj.initserver()
    else:
        loggerGS.error('Error reading config file %s', pathConfigFile)

if __name__ == "__main__":
    main()
