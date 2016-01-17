import web
import itertools

import handlers

URLS = {
        "/"        : handlers.IndexHandler,
        "/reports(.*)" : handlers.ReportHandler, 
        "/getdata(.*)" : handlers.ReportJSONHandler 
        }

 
class WServer():
    def __init__(self):
        pass

    def make_app(self):
        urls = tuple(itertools.chain(*URLS.iteritems()))
        self.app = web.application(urls, globals(), autoreload=False)

    def run_app(self):
        self.app.run()
