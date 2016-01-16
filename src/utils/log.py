import logging
import sys

class Logger(object):
    def __init__(self, filepath, logname=None):
        logger = logging.getLogger(filepath)
        logger.setLevel(logging.DEBUG)
        if logname == 'stdout':
            handler = logging.StreamHandler(sys.stdout)
        else:
            handler = logging.FileHandler(filepath)
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.info(msg)

"""
def log(msg, msg_type=None, level=None):
    debughandler = logging.FileHandler(DEBUGLOG)
"""

