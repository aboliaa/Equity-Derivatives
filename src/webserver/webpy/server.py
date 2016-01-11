import web
import itertools

import handlers

URLS = {
        "/"        : handlers.IndexHandler,
        "/reports(.*)" : handlers.ReportHandler 
        }

 
class WServer():
    def __init__(self):
        pass

    def make_app(self):
        urls = tuple(itertools.chain(*URLS.iteritems()))
        self.app = web.application(urls, globals(), autoreload=True)

    def run_app(self):
        self.app.run()
