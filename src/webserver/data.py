import time

from const import DBNAME
from reports import reports

class WebData(object):
    def __init__(self):
        self.reports = reports
         
    def get_template_data(self, reportseq):
        reportseq = int(reportseq)
        if reportseq == 1:
            return self._get_template_data_report1()
        if reportseq == 2:
            return self._get_template_data_report2()
        if reportseq == 3:
            return self._get_template_data_report3()
        if reportseq == 4:
            return self._get_template_data_report4()
        if reportseq == 5:
            return self._get_template_data_report5()
        if reportseq == 6:
            return self._get_template_data_report6()
    
    def post_template_data(self, reportseq, args):
        reportseq = int(reportseq)
        if reportseq == 1:
            return self._post_template_data_report1(args)
        if reportseq == 2:
            return self._post_template_data_report2(args)
        if reportseq == 3:
            return self._post_template_data_report3(args)
        if reportseq == 4:
            return self._post_template_data_report4(args)
        if reportseq == 5:
            return self._post_template_data_report5(args)
        if reportseq == 6:
            return self._post_template_data_report6(args)
     
    def _get_template_data_report1(self):
        data = self.reports.report1.get_data_for_input()
        return data

    def _get_template_data_report2(self):
        data = self.reports.report2.get_data_for_input()
        return data

    def _get_template_data_report3(self):
        data = self.reports.report3.get_data_for_input()
        return data

    def _get_template_data_report4(self):
        data = self.reports.report4.get_data_for_input()
        return data

    def _get_template_data_report5(self):
        data = self.reports.report5.get_data_for_input()
        return data

    def _get_template_data_report6(self):
        data = self.reports.report6.get_data_for_input()
        return data

    def _post_template_data_report1(self, args):
        scrip = args["scrip"]
        dd = args["dd"]
        mm = args["mm"]
        yyyy = args["yyyy"]
        time_str = "%s-%s-%s" %(dd,mm,yyyy)
        date = time.strptime(time_str, "%d-%m-%Y")
        data = self.reports.report1.generate_data(scrip, date)
        self.reports.report1.plot_data(data)

    def _post_template_data_report2(self, args):
        scrip = args["scrip"]
        data = self.reports.report2.generate_data(scrip)
        self.reports.report2.plot_data(data)

    def _post_template_data_report3(self, args):
        scrip = args["scrip"]
        data = self.reports.report3.generate_data(scrip)
        self.reports.report3.plot_data(data)

    def _post_template_data_report4(self, args):
        dd = args["dd"]
        mm = args["mm"]
        yyyy = args["yyyy"]
        time_str = "%s-%s-%s" %(dd,mm,yyyy)
        date = time.strptime(time_str, "%d-%m-%Y")
        n = int(args["n"])
        data = self.reports.report4.generate_data(n, date)
        # print 'type(data) = ', type(data)
        self.reports.report4.plot_data(data)

    def _post_template_data_report5(self, args):
        dd = args["dd"]
        mm = args["mm"]
        yyyy = args["yyyy"]
        time_str = "%s-%s-%s" %(dd,mm,yyyy)
        date = time.strptime(time_str, "%d-%m-%Y")
        data = self.reports.report5.generate_data(date)
        self.reports.report5.plot_data(data)

    def _post_template_data_report6(self, args):
        dd = args["dd"]
        mm = args["mm"]
        yyyy = args["yyyy"]
        time_str = "%s-%s-%s" %(dd,mm,yyyy)
        date = time.strptime(time_str, "%d-%m-%Y")
        n = int(args["n"])
        data = self.reports.report6.generate_data(n, date)
        self.reports.report6.plot_data(data)
