from utils import *
from const import *
from data import DataGetter

class Report1DataGetter(DataGetter):
    def __init__(self, db, plot):
        super(Report1DataGetter, self).__init__(db)
        self.plot = plot

    def get_data_for_input(self):
        data = {}
        data["scrips"] = self.get_all_scrips()
        data["day_zero"] = self.get_day_zero()
        return data

    def generate_data(self, scrip, date):
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

    def transform_data(self, data, json=False):

        call_strike_prices = data['call_strike_prices']
        call_open_interests = data['call_open_interests']                       
        put_strike_prices = data['put_strike_prices']                           
        put_open_interests = data['put_open_interests']                         
        expiry_series = data['expiry_series']

        for e in expiry_series:
            x1 = call_strike_prices[e]                                   
            y1 = call_open_interests[e]
            
            x2 = put_strike_prices[e]                                   
            y2 = put_open_interests[e]
            
            break

        data = self.plot.plotly.form_plotargs_report1(x1, y1, x2, y2)
        if json:
            data = jsonify(data)
        return data

    def plot_data(self, data):
        self.plot.graph.plot_report1(data)
