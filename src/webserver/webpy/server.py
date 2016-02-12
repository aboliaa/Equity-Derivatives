import web
import itertools
import threading

import handlers

URLS = {
        "/"        : handlers.IndexHandler,
        "/reports(.*)" : handlers.ReportHandler, 
        "/getdata(.*)" : handlers.ReportJSONHandler 
        }

 
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
            return handle()
        finally:
            self.inprogress = False

    def make_app(self):
        urls = tuple(itertools.chain(*URLS.iteritems()))
        self.app = web.application(urls, globals(), autoreload=False)
        self.app.add_processor(self.request_locked)

    def run_app(self):
        self.app.run()

