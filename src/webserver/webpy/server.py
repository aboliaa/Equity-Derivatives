import web
import itertools
import threading
import cProfile
import pstats
import StringIO                                               

import handlers

URLS = {
        "/"        : handlers.IndexHandler,
        "/reports(.*)" : handlers.ReportHandler, 
        "/getdata(.*)" : handlers.ReportJSONHandler 
        }

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

    def request_locked(self, handle):
        msg = "Hold your Horses. Some other request is in progress."
        if self.inprogress:
            raise web.internalerror(msg)
            # return web.webapi.InternalError(message=msg)

        with self.lock: 
            if self.inprogress:
                raise web.internalerror(msg)
                # return web.webapi.InternalError(message=msg)

            self.inprogress = True

        try:
            if profile:
                pr = start_profiler()
            return handle()
        finally:
            if profile:
                collect_profiler(pr)
            self.inprogress = False

    def make_app(self):
        urls = tuple(itertools.chain(*URLS.iteritems()))
        self.app = web.application(urls, globals(), autoreload=False)
        self.app.add_processor(self.request_locked)

    def run_app(self):
        self.app.run()

