import traceback
from const import *
from data import DataGetter

class Report6DataGetter(DataGetter):
    def __init__(self, db, plot):
        super(Report6DataGetter, self).__init__(db)
        self.plot = plot

    def get_data_for_input(self):
        data = {}
        data["day_zero"] = self.get_day_zero()
        return data

    def generate_data(self, n, date):
        scrips = self.get_all_scrips()
       
        data = {'calls': {}, 'puts': {}}
        for scrip in scrips:
            try:
                clauses = [ [('timestamp', '=', date), ('opt_type', '=', CE)] ]
                max_contracts = self.get_max_value(scrip, OPTION, 'contracts', clauses=clauses)
                data['calls'][scrip] = {'scrip': scrip, 'max_contracts': max_contracts} 
            except:
                # traceback.print_exc()
                dlog.error("Exception in getting calls for scrip %s" % (scrip,))

            try: 
                clauses = [ [('timestamp', '=', date), ('opt_type', '=', PE)] ]
                max_contracts = self.get_max_value(scrip, OPTION, 'contracts', clauses=clauses)
                data['puts'][scrip] = {'scrip': scrip, 'max_contracts': max_contracts}
            except:
                # traceback.print_exc()
                dlog.error("Exception in getting puts for scrip %s" % (scrip,))


        data['calls'] = sorted(data['calls'].values(), key=lambda k:k['max_contracts'], reverse=True)
        data['puts'] = sorted(data['puts'].values(), key=lambda k:k['max_contracts'], reverse=True)

        data['calls'] = data['calls'][:n]
        data['puts'] = data['puts'][:n]

        cols = ['strike_pr', 'exp_dt']
        for call in data['calls']:
            clauses = [ [('timestamp', '=', date), 
                         ('opt_type', '=', CE), 
                         ('contracts', '=', call['max_contracts'])] ]
            scrip = self.get_scrip_data(call['scrip'], OPTION, cols=cols, clauses=clauses)
            call.update(scrip[0])
        
        for put in data['puts']:
            clauses = [ [('timestamp', '=', date), 
                         ('opt_type', '=', PE), 
                         ('contracts', '=', put['max_contracts'])] ]
            scrip = self.get_scrip_data(put['scrip'], OPTION, cols=cols, clauses=clauses)
            put.update(scrip[0])

        dlog.info("DATA = %s" % (data,))

        return data
    
    def plot_data(self, data):
        self.plot.table.plot_report6(data)

