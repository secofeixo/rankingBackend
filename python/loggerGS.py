# -*- coding: utf-8 -*-
import logging

# basic class to include a logger system
class loggerGS(object):
    def __init__(self):
        self.logger = logging.getLogger()
