import traceback
from const import *
from utils.helper import *
from error import *                                                             
from db.dberror import *
from data import *

class Report5DataGetter(DataGetter):
    def __init__(self, db, plot):
        super(Report5DataGetter, self).__init__(db)
        self.plot = plot

    def get_sum_of_OI_for_date(self, scrip, date):
        # series = get_expiry_series_for_date(scrip, date)
        series = get_exp_series(date)
        clauses = [[('timestamp', '=', date), ('exp_dt', '=', sr)] for sr in series]
        # dlog.info("clauses = %s" % (clauses,))
        try:
            sum_of_futures = self.get_sum(scrip, FUTURE, 'open_int', clauses=clauses)
            sum_of_options = self.get_sum(scrip, OPTION, 'open_int', clauses=clauses)
            if not sum_of_futures or not sum_of_options:
                return 0
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

    def get_sum_of_OI_for_date_range(self, scrip, drange):
        pass

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
        scrips = get_all_scrips()

        data = {'lowest': [], 'highest': []}
       
        dlog.info("Ignoring the scrips %s" % (ignore_scrips,))
        for scrip in scrips:
            if scrip in ignore_scrips:
                continue

            skipped_dates = []
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
                    skipped_dates.append(from_pytime_to_str(dt))
                    continue
                OI_sums[dt] = oi_sum
            
            if not OI_sums:
                dlog.info("No OI_sums for scrip %s" % (scrip))
                continue

            if skipped_dates:
                dlog.info("For scrip %s, skipped dates = %s" % (scrip, skipped_dates))

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
        title += " (On %s)" %(from_pytime_to_str(self.input["date"]))
        height = max(len(y)*25, 500)
        data1 = self.plot.plotly.form_plotargs_report5(x, y, height, title)                
       
        x = []
        y = []
        i = 0
        for d in sorted(data['lowest'], key=lambda x:x[1], reverse=True): 
            i += 1
            y.append(d[0])
            x.append(d[1])

        title = "Lowest Open Interest"
        title += " (%s)" %(from_pytime_to_str(self.input["date"]))
        height = max(len(y)*25, 500)
        data2 = self.plot.plotly.form_plotargs_report5(x, y, height, title)

        data = [data1, data2]
        
        if json:                                                                
            data = jsonify(data)

        dlog.info("Done generating Report5")
        return data

    def plot_data(self, data):
        self.plot.table.plot_report5(data)

