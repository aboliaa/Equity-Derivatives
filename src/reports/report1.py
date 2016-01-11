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
        return data
    
    def plot_data(self, data):
        self.plot.graph.plot_report1(data)
