import web
import urlparse

from data_html import WebDataHTML
from data_json import WebDataJSON

from const import *

__all__ = ["IndexHandler", "ReportHandler", "ReportJSONHandler"]

render = web.template.render("templates/")
dbname = DBPATH
wdata_html = WebDataHTML()
wdata_json = WebDataJSON()

def get_input(func):
    def func_wrapper(self, arg):
        args = dict(web.input())
        querydata = get_input_from_query_string()
        args.update(querydata)
        return func(self, args)
    return func_wrapper

class IndexHandler():
    def GET(self):
        data = wdata_json.get_render_data()
        return render.index(data=data)

    def POST(self):
        return "IN POST INDEX FUNCTION"

class ReportHandler():
    @get_input
    def GET(self, args):
        reportseq = args["report"]
        report = "report" + reportseq
        d = wdata_html.get_template_data(reportseq)
        return render._template(report+"_input")(data=d)

    @get_input
    def POST(self, args):
        reportseq = args["report"]
        report = "report" + reportseq
        wdata_html.post_template_data(reportseq, args)
        return render._template("show_"+report)()

class ReportJSONHandler():
    def GET(self, args):
        params = web.input()
        reportseq = int(params["report"])
        return wdata_json.get_data(reportseq, params)

def get_input_from_query_string():
    query = web.ctx.query
    input_from_url = dict(urlparse.parse_qsl(query[1:]))
    return input_from_url
