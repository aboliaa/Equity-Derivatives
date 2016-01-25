import time
import traceback

from const import *
from utils import *
from data import DataGetter

class Report3DataGetter(DataGetter):
    def __init__(self, db, plot):
        super(Report3DataGetter, self).__init__(db)
        self.plot = plot

    def get_data_for_input(self):
        data = {}
        data["scrips"] = self.get_all_scrips()
        return data

    def _generate_data(self, scrip):
        self.input = {"scrip": scrip}

        # TODO: Ideally, min_date and max_date for a scrip
        # (including informations about mergers and de-mergers),
        # can be stored in M_SCRIP_INFO table.

        min_date = self.get_min_value(scrip, OPTION, 'timestamp')
        min_date = from_str_to_pytime(min_date)
       
        max_date = self.get_max_value(scrip, OPTION, 'timestamp')
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

            clauses = [ [('timestamp', '=', dt), ('opt_type', '=', CE)] ]
            sum_of_calls = self.get_sum(scrip, OPTION, 'open_int', clauses=clauses)
            
            clauses = [ [('timestamp', '=', dt), ('opt_type', '=', PE)] ]
            sum_of_puts = self.get_sum(scrip, OPTION, 'open_int', clauses=clauses)

            PCR_OI = float(sum_of_puts) / float(sum_of_calls)
            
            clauses = [ [('timestamp', '=', dt), ('opt_type', '=', CE)] ]
            sum_of_calls = self.get_sum(scrip, OPTION, 'contracts', clauses=clauses)
            
            clauses = [ [('timestamp', '=', dt), ('opt_type', '=', PE)] ]
            sum_of_puts = self.get_sum(scrip, OPTION, 'contracts', clauses=clauses)

            PCR_trade = sum_of_puts / sum_of_calls
            PCR_trade = float(sum_of_puts) / float(sum_of_calls)

            data[from_pytime_to_str(dt)] = {}
            data[from_pytime_to_str(dt)]['settlement_price'] = settlement_price
            data[from_pytime_to_str(dt)]['PCR_OI'] = PCR_OI
            data[from_pytime_to_str(dt)]['PCR_trade'] = PCR_trade
        
        return data

    def generate_data(self, scrip):
        try:
            data = self._generate_data(scrip)
            error = None
        except DBError as fault:
            traceback.print_exc()
            if fault.errno <> ENOTFOUND:
                raise fault
            data = None
            error = EINVALIDINPUT
        return data, error


    def transform_data(self, data, json=False):
        x = []
        y = []
        y1 = []
        y2 = []
        i = 1
        for k in sorted(data):
            v = data[k]
            x.append(k)
            i += 1
            y.append(v['settlement_price'])
            y1.append(v['PCR_OI'])
            y2.append(v['PCR_trade'])
        
        title = "Settlement Price v/s PCR"
        title += " (For scrip %s)" %(self.input["scrip"])

        data = self.plot.plotly.form_plotargs_report3(x, y, y1, y2, title)
        data = [data]
        if json:
            data = jsonify(data)
        return data

    def plot_data(self, data):
        self.plot.graph.plot_report3(data)
