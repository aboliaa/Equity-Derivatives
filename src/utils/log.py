import logging

class Logger(object):
    def __init__(self, filepath):
        logger = logging.getLogger(filepath)
        logger.setLevel(logging.DEBUG)
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

