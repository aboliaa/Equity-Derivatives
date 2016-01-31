import time
import traceback

from const import *
from utils.helper import *
from db.dberror import *
from data import DataGetter

class Report2DataGetter(DataGetter):
    def __init__(self, db, plot):
        super(Report2DataGetter, self).__init__(db)
        self.plot = plot

    def get_data_for_input(self):
        data = {}
        data["scrips"] = self.get_all_scrips()
        return data

    def _generate_data(self, scrip):
        dlog.info("Report2, Scrip=%s" % (scrip,))
        rlog.info("Report2,%s" % (scrip,))

        dlog.info("Starting to generate Report2")

        self.input = {"scrip": scrip}

        # TODO: Ideally, min_date and max_date for a scrip
        # (including informations about mergers and de-mergers),
        # can be stored in M_SCRIP_INFO table.

        min_date = self.get_min_value(scrip, FUTURE, 'timestamp')
        max_date = self.get_max_value(scrip, FUTURE, 'timestamp')

        data = {}
        for dt in datetimeIterator(min_date, max_date):

            clauses = [ [('timestamp', '=', dt)] ]
            series = self.get_all_series_for_date(scrip, dt)
            # near_series_date = self.get_min_value(scrip, FUTURE, 'exp_dt', clauses=clauses)

            # There are no rows in db for holidays. Hence aggregate query will
            # return output as None. Skip these dates.
            # TODO: Raise an proper exception from DB layer.
            if not series:
                continue

            near_series_date = series[0]

            # TODO: Check if this can be reused in other reports (report 3)
            cols = ['settle_pr']
            clauses = [ [('timestamp', '=', dt), ('exp_dt', '=', near_series_date)] ]
            settlement_price = self.get_scrip_data(scrip, FUTURE, cols=cols, clauses=clauses)
            settlement_price = settlement_price[0]['settle_pr']

            clauses = [[('timestamp', '=', dt), ('exp_dt', '=', sr)] for sr in series]
            s1 = self.get_sum(scrip, OPTION, 'open_int', clauses=clauses)
            s2 = self.get_sum(scrip, FUTURE, 'open_int', clauses=clauses)

            # TODO: Check if summation of OI can be reused in other reports (report 4),
            # so make it into a common function.
            OI_sum = s1 + s2

            data[from_pytime_to_str(dt)] = {}
            data[from_pytime_to_str(dt)]['settlement_price'] = settlement_price
            data[from_pytime_to_str(dt)]['summation_of_OI'] = OI_sum
        
        return data

    def generate_data(self, scrip):
        try:
            data = self._generate_data(scrip)
            error = None
        except DBError as fault:
            dlog.info(traceback.format_exc())
            if fault.errno <> ENOTFOUND:
                raise fault
            data = None
            error = EINVALIDINPUT
        return data, error

    def transform_data(self, data, json=False):
        x = []
        y1 = []
        y2 = []
        i = 1
        for d in sorted(data.iteritems()):
            x.append(d[0])
            i += 1
            y1.append(d[1]['settlement_price'])
            y2.append(d[1]['summation_of_OI'])

        title = "Settlement Price v/s Open Interest"
        title += " (For Scrip %s)" %(self.input["scrip"])

        data = self.plot.plotly.form_plotargs_report2(x, y1, y2, title)
        data = [data]
        if json:
            data = jsonify(data)
        dlog.info("Done generating Report2")
        return data

    def plot_data(self, data):
        self.plot.graph.plot_report2(data)
