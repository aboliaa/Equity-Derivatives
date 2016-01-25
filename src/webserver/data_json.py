import web
import time

from reports import reports

FUNC_MAP = {
            1: "_get_data_report1",
            2: "_get_data_report2",
            3: "_get_data_report3",
            4: "_get_data_report4",
            5: "_get_data_report5",
            6: "_get_data_report6"
           }

class WebDataJSON(object):
    def __init__(self):
        self.reports = reports
        
    def get_render_data(self):
        data = self.reports.get_render_data()
        return data

    def get_data(self, reportseq, args):
        reportseq = int(reportseq)
        func = getattr(self, FUNC_MAP[reportseq])
        return func(args)
     
    def _get_data_report1(self, args):
        scrip = args["scrip"]
        dd = args["dd"]
        mm = args["mm"]
        yyyy = args["yyyy"]
        time_str = "%s-%s-%s" %(dd,mm,yyyy)
        date = time.strptime(time_str, "%d-%m-%Y")
        data, error = self.reports.report1.generate_data(scrip, date)
        if error:
            raise web.internalerror(error)
        data = self.reports.report1.transform_data(data, json=True)
        return data

    def _get_data_report2(self, args):
        scrip = args["scrip"]
        data, error = self.reports.report2.generate_data(scrip)
        if error:
            raise web.internalerror(error)
        data = self.reports.report2.transform_data(data, json=True)
        return data

    def _get_data_report3(self, args):
        scrip = args["scrip"]
        data, error = self.reports.report3.generate_data(scrip)
        if error:
            raise web.internalerror(error)
        data = self.reports.report3.transform_data(data, json=True)
        return data

    def _get_data_report4(self, args):
        dd = args["dd"]
        mm = args["mm"]
        yyyy = args["yyyy"]
        time_str = "%s-%s-%s" %(dd,mm,yyyy)
        date = time.strptime(time_str, "%d-%m-%Y")
        n = int(args["n"])
        data, error = self.reports.report4.generate_data(n, date)
        if error:
            raise web.internalerror(error)
        data = self.reports.report4.transform_data(data, json=True)
        return data

    def _get_data_report5(self, args):
        dd = args["dd"]
        mm = args["mm"]
        yyyy = args["yyyy"]
        time_str = "%s-%s-%s" %(dd,mm,yyyy)
        date = time.strptime(time_str, "%d-%m-%Y")
        data, error = self.reports.report5.generate_data(date)
        if error:
            raise web.internalerror(error)
        data = self.reports.report5.transform_data(data, json=True)
        return data

    def _get_data_report6(self, args):
        dd = args["dd"]
        mm = args["mm"]
        yyyy = args["yyyy"]
        time_str = "%s-%s-%s" %(dd,mm,yyyy)
        date = time.strptime(time_str, "%d-%m-%Y")
        n = int(args["n"])
        data, error = self.reports.report6.generate_data(n, date)
        if error:
            raise web.internalerror(error)
        data = self.reports.report6.transform_data(data, json=True)
        return data
