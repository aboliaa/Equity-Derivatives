import sys
import posixpath
import urllib
import os
import web
import itertools
import threading
import cProfile
import pstats
import StringIO
import psutil
import time

from const import *
import handlers

URLS = {
        "/"        : handlers.IndexHandler,
        "/reports(.*)" : handlers.ReportHandler, 
        "/getdata(.*)" : handlers.ReportJSONHandler 
        }

class StaticApp(web.httpserver.StaticApp):
    """ StaticApp to access static files outside working directory. """
    def translate_path(self, path):
        return path

class StaticMiddleware():
    """ WSGI middleware for changing static files location. """
    def __init__(self, app, prefix="/static/", root_path=None):
        self.app = app
        self.prefix = prefix
        self.root_path = root_path

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO")
        path = self.normpath(path)

        if path.startswith(self.prefix):
            if self.root_path:
                path = path.replace('/', os.path.sep)
                prefix = self.prefix.replace('/', os.path.sep)
                p = web.lstrips(path, prefix)
                environ["PATH_INFO"] = os.path.join(self.root_path, p)
                return StaticApp(environ, start_response)
            else:
                return web.httpserver.StaticApp(environ, start_response)
        else:
            return self.app(environ, start_response)

    def normpath(self, path):
        path2 = posixpath.normpath(urllib.unquote(path))
        if path.endswith("/"):
            path2 += "/"
        return path2

def start_profiler():
    pr = cProfile.Profile()                                                         
    pr.enable()
    return pr

def collect_profiler(pr):
    pr.disable()
    s = StringIO.StringIO()                                                         
    sortby = 'cumulative'                                                           
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)                              
    plog.info("\n\n")
    plog.info(ps.print_stats())
    plog.info(s.getvalue())

class WServer():
    def __init__(self):
        self.lock = threading.Lock()
        self.inprogress = False
        self.usage_interval = 2
        t = threading.Thread(target=self.system_usage)
        t.start()

    def system_usage(self):
        dlog.debug("Starting system usage thread")
        while True:
            try:
                if self.inprogress:
                    cpu = psutil.cpu_percent()
                    if cpu > CPU_THRESHOLD:
                        ps = psutil.Process(os.getpid())
                        pscpu = ps.cpu_percent()
                        dlog.warn("CPU consumed is %s, CPU percentage of DVServer is %s" % (cpu,pscpu))

                    mem = psutil.virtual_memory().percent
                    if mem > MEMORY_THRESHOLD:
                        ps = psutil.Process(os.getpid())
                        psmem = ps.memory_percent()
                        dlog.warn("Memory consumed is %s, memory percentage of DVServer is %s" % (mem,psmem))
            except Exception, fault:
                dlog.error(traceback.format_exc())

            time.sleep(self.usage_interval)

    def request_locked(self, handle):
        msg = "Hold your Horses. Some other request is in progress."
        if self.inprogress:
            raise web.internalerror(msg)

        with self.lock: 
            if self.inprogress:
                raise web.internalerror(msg)

            self.inprogress = True

        try:
            if profile:
                pr = start_profiler()
            return handle()
        finally:
            if profile:
                collect_profiler(pr)
            self.inprogress = False

    def _get_static_path(self):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            static_path = os.path.join(sys._MEIPASS, 'static')
        except:
            static_path = None
        print "Static path =", static_path
        return static_path

    def make_app(self):
        urls = tuple(itertools.chain(*URLS.iteritems()))
        self.app = web.application(urls, globals(), autoreload=False)
        self.app.add_processor(self.request_locked)

        wsgifunc = self.app.wsgifunc()
        wsgifunc = StaticMiddleware(wsgifunc, root_path=self._get_static_path())
        wsgifunc = web.httpserver.LogMiddleware(wsgifunc)
        self.server = web.httpserver.WSGIServer(("0.0.0.0", 8080), wsgifunc)
        print "http://%s:%d/" % ("0.0.0.0", 8080)

    def run_app(self):
        try:
            self.server.start()
        except KeyboardInterrupt:
            self.server.stop()

