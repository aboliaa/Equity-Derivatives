import os
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

def verify_db_version(dbops, sver):
    spec = {
        'cols': ['name'],
        'clauses': [[('type', '=', 'table'), ('name', '=', 'P_DB_VERSION')]]
    }
    table = dbops.select_meta(spec)
    if not table:
        dlog.error("DB Version information not found. Exiting...")
        os._exit(1)

    spec = {
        'tablename': "P_DB_VERSION",
        'cols': ['version'],
    }
    dbver = dbops.select(spec)[0][0]
    dlog.info("DB version %s" % dbver)
    if dbver <> sver:
        dlog.error("DB version does not match with server version. Exiting...")
        os._exit(1)

if __name__ == "__main__":
    __builtins__.profile = "--profile" in sys.argv
    debuglogger = log.Logger(DEBUGLOG)
    __builtins__.dlog = debuglogger
    profilelogger = log.Logger(PROFILELOG)
    __builtins__.plog = profilelogger

    dbops = SQLite_DBOps(DBPATH)
    __builtins__.dbops = dbops

    __builtins__.cache = {}

    __builtins__.ignore_scrips = IGNORE_SCRIPS

    sver = VERSION
    dlog.info("====================== Version %s =========================" % sver)
    dlog.info("Starting server at port %s" % ("8080",))

    verify_db_version(dbops, sver)

    # TODO: Ideally request logs should go in DB.
    requestlogger = log.Logger(REQUESTLOG)
    __builtins__.rlog = requestlogger

    t = threading.Thread(target=spawn_chrome)
    t.start()

    srv = WebServer()
    srv.make_app()
    srv.run_app()

