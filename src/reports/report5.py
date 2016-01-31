import traceback
from const import *
from utils.helper import *
from error import *                                                             
from db.dberror import *
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
        series = self.get_all_series_for_date(scrip, date)
        clauses = [[('timestamp', '=', date), ('exp_dt', '=', sr)] for sr in series]
        try:
            sum_of_futures = self.get_sum(scrip, FUTURE, 'open_int', clauses=clauses)
            sum_of_options = self.get_sum(scrip, OPTION, 'open_int', clauses=clauses)
            sum_of_OI = sum_of_futures + sum_of_options
        except:
            dlog.info(traceback.format_exc())
            return 0
        
        # There are no rows in db for holidays. Hence aggregate query will
        # return output as None. Skip these dates.
        # TODO: Raise an proper exception from DB layer.
        if sum_of_OI is None:
            sum_of_OI = 0

        return sum_of_OI

    def validate_input(self, date):
        # TODO: Ideally db layer should raise this exception 
        clauses = [ [('timestamp', '=', date)] ]
        data = self.get_scrip_data("NIFTY", OPTION, cols=None, clauses=clauses)
        if not data:
            raise DBError(ENOTFOUND)

    def _generate_data(self, date):
        strdate = from_pytime_to_str(date)
        dlog.info("Report5, Date=%s" % (strdate,))
        rlog.info("Report5,%s" % (strdate,))

        dlog.info("Starting to generate Report5")

        self.validate_input(date)
        self.input = {"date": date}
        scrips = self.get_all_scrips()

        data = {'lowest': [], 'highest': []}
       
        for scrip in scrips:
            try:
                min_date = self.get_min_value(scrip, FUTURE, 'timestamp')
            except:
                dlog.info(traceback.format_exc())
                dlog.error("Exception in scrip %s" % (scrip,))
                continue

            max_date = date

            OI_sums = {}
            for dt in datetimeIterator(min_date, max_date):
                oi_sum = self.get_sum_of_OI_for_date(scrip, dt)
                if not oi_sum:
                    dlog.info("No OI_sum for scrip %s, for date %s" % (scrip, dt))
                    continue
                OI_sums[dt] = oi_sum
            
            if not OI_sums:
                dlog.info("No OI_sums for scrip %s" % (scrip))
                continue

            date_for_min_sum_of_OI = min(OI_sums, key=OI_sums.get)
            date_for_max_sum_of_OI = max(OI_sums, key=OI_sums.get)
          
            if date_for_min_sum_of_OI == max_date:
                data['lowest'].append((scrip, OI_sums[date_for_min_sum_of_OI]))
            elif date_for_max_sum_of_OI == max_date:
                data['highest'].append((scrip, OI_sums[date_for_max_sum_of_OI]))

        dlog.info("HIGHEST DATA = %s" % (data['highest'],))
        dlog.info("LOWEST DATA = %s" % (data['lowest'],))
        return data
   
    def generate_data(self, date):
        try:
            data = self._generate_data(date)
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
        y = []
        i = 0                                                                   
        for d in sorted(data['highest'], key=lambda x:x[1]):                                                          
            i += 1
            y.append(d[0])
            x.append(d[1])

        title = "Highest Open Interest"
        title += " (On Date %s)" %(from_pytime_to_str(self.input["date"]))
        height = max(len(y)*25, 500)
        data1 = self.plot.plotly.form_plotargs_report5(x, y, height, title)                
       
        x = []
        y = []
        i = 0
        for d in sorted(data['lowest'], key=lambda x:x[1]):                                                          
            i += 1
            y.append(d[0])
            x.append(d[1])

        title = "Lowest Open Interest"
        title += " (On Date %s)" %(from_pytime_to_str(self.input["date"]))
        height = max(len(y)*25, 500)
        data2 = self.plot.plotly.form_plotargs_report5(x, y, height, title)

        data = [data1, data2]
        
        if json:                                                                
            data = jsonify(data)

        dlog.info("Done generating Report5")
        return data

    def plot_data(self, data):
        self.plot.table.plot_report5(data)

