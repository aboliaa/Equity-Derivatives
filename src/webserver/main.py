import webbrowser
import platform
import time
import threading
import subprocess

from const import *

from utils import log
from db.dbops_sqlite3 import SQLite_DBOps

WEBPY = "webpy"


class WebServer():
    def __init__(self, webserver_type=WEBPY):
        import webpy
        module = __import__(webserver_type)
        self.webserver = module.WServer()

    def make_app(self):
        self.webserver.make_app()

    def run_app(self):
        self.webserver.run_app()

def spawn_chrome():
    time.sleep(2)
    if platform.system() == 'Windows':
        subprocess.Popen(["start", "chrome", "http://localhost:8080"], shell=True)
    elif platform.system() == 'Darwin':
        # webbrowser.geit('macosx').open("http://localhost:8080")
        pass

if __name__ == "__main__":
    debuglogger = log.Logger(DEBUGLOG)
    __builtins__.dlog = debuglogger

    dbops = SQLite_DBOps(DBPATH)
    __builtins__.dbops = dbops

    dlog.info("====================== Version 0.1 =========================")
    dlog.info("Starting server at port %s" % ("8080",))

    # TODO: Ideally request logs should go in DB.
    requestlogger = log.Logger(REQUESTLOG)
    __builtins__.rlog = requestlogger

    t = threading.Thread(target=spawn_chrome)
    t.start()

    srv = WebServer()
    srv.make_app()
    srv.run_app()
