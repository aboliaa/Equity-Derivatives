import traceback

from utils.helper import *
from const import *
from error import *
from db.dberror import *
from data import *

class Report1DataGetter(DataGetter):
    def __init__(self, db, plot):
        super(Report1DataGetter, self).__init__(db)
        self.plot = plot

    def validate_input(self, scrip, date):
        # TODO: Ideally db layer should raise this exception 
        clauses = [ [('timestamp', '=', date)] ]
        data = self.get_scrip_data(scrip, OPTION, cols=['*'], clauses=clauses)
        if not data:
            raise DBError(ENOTFOUND)

    def _generate_data(self, scrip, date):
        strdate = from_pytime_to_str(date)
        dlog.info("Report1, Scrip=%s, Date=%s" % (scrip, strdate))
        rlog.info("Report1,%s,%s" % (scrip, strdate))

        dlog.info("Starting to generate Report1")

        self.validate_input(scrip, date)
        self.input = {'scrip': scrip, 'date': date}

        cols = ['open_int', 'exp_dt', 'strike_pr', 'opt_type']
        clauses = [ [('timestamp', '=', date)] ]
        data = self.get_scrip_data(scrip, OPTION, cols=cols, clauses=clauses)

        call_strike_prices = {}
        call_open_interests = {}
        put_strike_prices = {}
        put_open_interests = {}
 
        for d in data:
            if d['opt_type'] == CE:
                if d['exp_dt'] not in call_strike_prices:
                    call_strike_prices[d['exp_dt']] = []
                if d['exp_dt'] not in call_open_interests:
                    call_open_interests[d['exp_dt']] = []
                call_strike_prices[d['exp_dt']].append(d['strike_pr'])
                call_open_interests[d['exp_dt']].append(d['open_int'])
            elif d['opt_type'] == PE:
                if d['exp_dt'] not in put_strike_prices:
                    put_strike_prices[d['exp_dt']] = []
                if d['exp_dt'] not in put_open_interests:
                    put_open_interests[d['exp_dt']] = []
                put_strike_prices[d['exp_dt']].append(d['strike_pr'])
                put_open_interests[d['exp_dt']].append(d['open_int'])

        expiry_series = call_strike_prices.keys()
        expiry_series.sort()

        # Ignore expiry series after 3
        expiry_series = expiry_series[:3]

        data = {}
        data['call_strike_prices'] = call_strike_prices
        data['call_open_interests'] = call_open_interests
        data['put_strike_prices'] = put_strike_prices
        data['put_open_interests'] = put_open_interests
        data['expiry_series'] = expiry_series

        return data

    def generate_data(self, scrip, date):
        try:
            data = self._generate_data(scrip, date)
            error = None
        except DBError as fault:
            dlog.error(traceback.format_exc())
            if fault.errno <> ENOTFOUND:
                raise fault
            data = None
            error = EINVALIDINPUT
        return data, error

    def transform_data(self, data, json=False):

        call_strike_prices = data['call_strike_prices']
        call_open_interests = data['call_open_interests']                       
        put_strike_prices = data['put_strike_prices']                           
        put_open_interests = data['put_open_interests']                         
        expiry_series = data['expiry_series']

        series_map = {
                        0: "Near series",
                        1: "Next series",
                        2: "Far series",
                     }
        data = []
        i = 0
        for e in expiry_series:
            x1 = call_strike_prices[e]                                   
            y1 = call_open_interests[e]
            t1 = [d3(d) for d in call_open_interests[e]]
            
            x2 = put_strike_prices[e]                                   
            y2 = put_open_interests[e]                                   
            t2 = [d3(d) for d in put_open_interests[e]]
        
            title = "Distribution of PUTs and CALLs: %s" %(series_map[i])
            title += " (%s on %s)" %(self.input["scrip"], from_pytime_to_str(self.input["date"], "%d-%b-%Y"))
            
            data.append(self.plot.plotly.form_plotargs_report1(x1, y1, t1, x2, y2, t2, title))
            i += 1

        if json:
            data = jsonify(data)

        dlog.info("Done generating Report1")
        return data

    def plot_data(self, data):
        self.plot.graph.plot_report1(data)
