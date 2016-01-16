import web
import urlparse

from data import WebData

from const import *

__all__ = ["IndexHandler", "ReportHandler"]

render = web.template.render("webserver/templates/")
dbname = DBPATH
wdata = WebData()

def get_input(func):
    def func_wrapper(self, arg):
        args = dict(web.input())
        querydata = get_input_from_query_string()
        args.update(querydata)
        return func(self, args)
    return func_wrapper

class IndexHandler():
    def GET(self):
        return render.index()

    def POST(self):
        return "IN POST INDEX FUNCTION"

class ReportHandler():
    @get_input
    def GET(self, args):
        reportseq = args["report"]
        report = "report" + reportseq
        d = wdata.get_template_data(reportseq)
        return render._template(report+"_input")(data=d)

    @get_input
    def POST(self, args):
        reportseq = args["report"]
        report = "report" + reportseq
        wdata.post_template_data(reportseq, args)
        return render._template("show_"+report)()

def get_input_from_query_string():
    query = web.ctx.query
    input_from_url = dict(urlparse.parse_qsl(query[1:]))
    return input_from_url
