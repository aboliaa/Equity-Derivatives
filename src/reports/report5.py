import traceback
from const import *
from utils import *
from data import DataGetter

class Report5DataGetter(DataGetter):
    def __init__(self, db, plot):
        super(Report5DataGetter, self).__init__(db)
        self.plot = plot

    def get_data_for_input(self):
        data = {}
        data["day_zero"] = self.get_day_zero()
        return data

    def get_sum_of_OI_for_date(self, scrip, date):
        clauses = [ [('timestamp', '=', date)] ]
        try:
            sum_of_futures = self.get_sum(scrip, FUTURE, 'open_int', clauses=clauses)
            sum_of_options = self.get_sum(scrip, OPTION, 'open_int', clauses=clauses)
            sum_of_OI = sum_of_futures + sum_of_options
        except:
            traceback.print_exc()
            return 0
        
        # There are no rows in db for holidays. Hence aggregate query will
        # return output as None. Skip these dates.
        # TODO: Raise an proper exception from DB layer.
        if sum_of_OI is None:
            sum_of_OI = 0

        return sum_of_OI

    def generate_data(self, date):
        scrips = self.get_all_scrips()

        data = {'lowest': [], 'highest': []}
        
        for scrip in scrips:
            try:
                min_date = self.get_min_value(scrip, FUTURE, 'timestamp')
            except:
                traceback.print_exc()
                dlog.error("Exception in scrip %s" % (scrip,))
                continue

            min_date = from_str_to_pytime(min_date)

            max_date = date

            OI_sums = {}
            for dt in datetimeIterator(min_date, max_date):
                OI_sums[dt] = self.get_sum_of_OI_for_date(scrip, dt)
            
            dlog.info("for scrip %s OI_sums = %s" % (scrip, OI_sums))

            date_for_min_sum_of_OI = min(OI_sums, key=OI_sums.get)
            date_for_max_sum_of_OI = max(OI_sums, key=OI_sums.get)
          
            if date_for_min_sum_of_OI == max_date:
                data['lowest'].append((scrip, OI_sums[date_for_min_sum_of_OI]))
            elif date_for_max_sum_of_OI == max_date:
                data['highest'].append((scrip, OI_sums[date_for_max_sum_of_OI]))

        dlog.info("HIGHEST DATA = %s" % (data['highest'],))
        dlog.info("LOWEST DATA = %s" % (data['lowest'],))
        return data
    
    def transform_data(self, data, json=False):
       
        x = []
        y = []
        i = 0                                                                   
        for d in sorted(data['highest'], key=lambda x:x[1]):                                                          
            i += 1
            y.append(d[0])
            x.append(d[1])

        data = self.plot.plotly.form_plotargs_report5(x, y)                
        
        if json:                                                                
            data = jsonify(data)
        return data

    def plot_data(self, data):
        self.plot.table.plot_report5(data)

