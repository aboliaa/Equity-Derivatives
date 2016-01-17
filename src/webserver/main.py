from const import *

from utils import log

WEBPY = "webpy"

import webpy

class WebServer():
    def __init__(self, webserver_type=WEBPY):
        module = __import__(webserver_type)
        self.webserver = module.WServer()

    def make_app(self):
        self.webserver.make_app()

    def run_app(self):
        self.webserver.run_app()

if __name__ == "__main__":
    debuglogger = log.Logger(DEBUGLOG)
    __builtins__.dlog = debuglogger

    dlog.info("Starting server at port %s" % ("8080",))

    # TODO: Ideally request logs should go in DB.
    requestlogger = log.Logger(REQUESTLOG)
    __builtins__.rlog = requestlogger

    srv = WebServer()
    srv.make_app()
    srv.run_app()

