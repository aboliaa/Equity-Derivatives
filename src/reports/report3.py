import time
import traceback

from const import *
from utils.helper import *
from db.dberror import *
from data import *

class Report3DataGetter(DataGetter):
    def __init__(self, db, plot):
        super(Report3DataGetter, self).__init__(db)
        self.plot = plot

    def _generate_data(self, scrip):
        dlog.info("Report3, Scrip=%s" % (scrip,))
        rlog.info("Report3,%s" % (scrip,))

        self.input = {"scrip": scrip}

        dlog.info("Starting to generate Report3")

        # TODO: Ideally, min_date and max_date for a scrip
        # (including informations about mergers and de-mergers),
        # can be stored in M_SCRIP_INFO table.

        min_date = self.get_min_value(scrip, OPTION, 'timestamp')
        max_date = self.get_max_value(scrip, OPTION, 'timestamp')

        data = {}
        for dt in datetimeIterator(min_date, max_date):

            clauses = [ [('timestamp', '=', dt)] ]
            near_series_date = self.get_min_value(scrip, FUTURE, 'exp_dt', clauses=clauses)

            # There are no rows in db for holidays. Hence aggregate query will
            # return output as None. Skip these dates.
            # TODO: Raise an proper exception from DB layer.
            if near_series_date is None:
                continue

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
            dlog.error(traceback.format_exc())
            if fault.errno <> ENOTFOUND:
                raise fault
            data = None
            error = EINVALIDINPUT
        return data, error


    def transform_data(self, data, json=False):
        x = []
        y1 = []
        y2 = []
        y3 = []
        t1 = []
        t2 = []
        t3 = []
        i = 1
        for k in sorted(data):
            v = data[k]
            time_struct = time.strptime(k, "%Y-%m-%d")                       
            day = time.strftime("%d %b %Y", time_struct)
            x.append(day)
            i += 1
            y1.append(v['settlement_price'])
            t1.append(d3(v['settlement_price']))
            y2.append(v['PCR_OI'])
            t2.append(d3(v['PCR_OI']))
            y3.append(v['PCR_trade'])
            t3.append(d3(v['PCR_trade']))
        
        title = "Settlement Price v/s PCR"
        title += " (%s)" %(self.input["scrip"])

        data = self.plot.plotly.form_plotargs_report3(x, y1, t1, y2, t2, y3, t3, title)
        data = [data]
        if json:
            data = jsonify(data)

        dlog.info("Done generating Report3")
        return data

    def plot_data(self, data):
        self.plot.graph.plot_report3(data)
