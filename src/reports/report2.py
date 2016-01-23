import time

from const import *
from utils import *
from data import DataGetter

class Report2DataGetter(DataGetter):
    def __init__(self, db, plot):
        super(Report2DataGetter, self).__init__(db)
        self.plot = plot

    def get_data_for_input(self):
        data = {}
        data["scrips"] = self.get_all_scrips()
        return data

    def generate_data(self, scrip):
        # TODO: Ideally, min_date and max_date for a scrip
        # (including informations about mergers and de-mergers),
        # can be stored in M_SCRIP_INFO table.

        min_date = self.get_min_value(scrip, FUTURE, 'timestamp')
        min_date = from_str_to_pytime(min_date)
       
        max_date = self.get_max_value(scrip, FUTURE, 'timestamp')
        max_date = from_str_to_pytime(max_date)

        data = {}
        for dt in datetimeIterator(min_date, max_date):

            clauses = [ [('timestamp', '=', dt)] ]
            near_series_date = self.get_min_value(scrip, FUTURE, 'exp_dt', clauses=clauses)

            # There are no rows in db for holidays. Hence aggregate query will
            # return output as None. Skip these dates.
            # TODO: Raise an proper exception from DB layer.
            if near_series_date is None:
                continue

            near_series_date = from_str_to_pytime(near_series_date)
       
            # TODO: Check if this can be reused in other reports (report 3)
            cols = ['settle_pr']
            clauses = [ [('timestamp', '=', dt), ('exp_dt', '=', near_series_date)] ]
            settlement_price = self.get_scrip_data(scrip, FUTURE, cols=cols, clauses=clauses)
            settlement_price = settlement_price[0]['settle_pr']

            clauses = [ [('timestamp', '=', dt)] ]
            s1 = self.get_sum(scrip, OPTION, 'open_int', clauses=clauses)

            clauses = [ [('timestamp', '=', dt)] ]
            s2 = self.get_sum(scrip, FUTURE, 'open_int', clauses=clauses)

            # TODO: Check if summation of OI can be reused in other reports (report 4),
            # so make it into a common function.
            OI_sum = s1 + s2

            data[from_pytime_to_str(dt)] = {}
            data[from_pytime_to_str(dt)]['settlement_price'] = settlement_price
            data[from_pytime_to_str(dt)]['summation_of_OI'] = OI_sum
        
        return data

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

        data = self.plot.plotly.form_plotargs_report2(x, y1, y2)
        if json:
            data = jsonify(data)
        return data

    def plot_data(self, data):
        self.plot.graph.plot_report2(data)
