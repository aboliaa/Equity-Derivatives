import traceback

from utils.helper import *
from const import *
from error import *                                                             
from db.dberror import *
from data import DataGetter

class Report4DataGetter(DataGetter):
    def __init__(self, db, plot):
        super(Report4DataGetter, self).__init__(db)
        self.plot = plot

    def get_data_for_input(self):
        data = {}
        data["day_zero"] = self.get_day_zero()
        return data
    
    def get_sum_of_OI_for_scrip(self, scrip, derivative_type, clauses):
        try:
            s = self.get_sum(scrip, derivative_type, 'open_int', clauses=clauses)
        except:
            # TODO: Ideally we should handle specific errors here
            dlog.error("Exception in getting data for %s:%s" % (scrip, derivative_type))
            s = 0

        # There are no rows in db for holidays. Hence aggregate query will
        # return output as None. Skip these dates.
        # TODO: Raise an proper exception from DB layer.
        if s is None:
            s = 0

        return s

    def validate_input(self, n, date):
        # TODO: Ideally db layer should raise this exception 
        clauses = [ [('timestamp', '=', date)] ]
        data = self.get_scrip_data("NIFTY", OPTION, cols=None, clauses=clauses)
        if not data:
            raise DBError(ENOTFOUND)

    def _generate_data(self, n, date):
        strdate = from_pytime_to_str(date)
        dlog.info("Rport4, n=%s, Date=%s" % (n, strdate))
        rlog.info("Rport4,%s,%s" % (n, strdate))

        self.validate_input(n, date)
        self.input = {"n": n, "date": date}

        sums = {'near': {}, 'next': {}, 'far': {}}
        movements = {'near': {}, 'next': {}, 'far': {}, 'cumulative': {}}
        scrips = self.get_all_scrips()
        prev_date = get_prev_date(date)

        for scrip in scrips:
            try:
                _series = self.get_all_series(scrip, FUTURE, date)
            except:
                dlog.error("Nothing found for scrip, derivative_type = %s:%s" % (scrip, FUTURE))
                series_future = set()
            else:
                series_future = set([x[0] for x in _series])
            
            
            try:
                _series = self.get_all_series(scrip, OPTION, date)
            except:
                dlog.error("Nothing found for scrip, derivative_type = %s:%s " % (scrip, OPTION))
                series_option = set()
            else:
                series_option = set([x[0] for x in _series])
    
            _series = series_future.union(series_option)
            series = sorted(list(_series))

            # dlog.info("For scrip %s series = %s:%s" % (scrip, series))
        
            n_series = len(series)
            if n_series < 3:
                dlog.error("For scrip %s there are less than 3 series" % (scrip,))
                continue

            i = 0
            for _s in ['near', 'next', 'far']:
                sdate = series[i]

                clauses = [ [('timestamp', '=', date), ('exp_dt', '=', sdate)] ]
                s1 = self.get_sum_of_OI_for_scrip(scrip, FUTURE, clauses)

                s2 = self.get_sum_of_OI_for_scrip(scrip, OPTION, clauses)

                sum1 = s1 + s2

                # TODO: What if previous date series is different than date?

                clauses = [ [('timestamp', '=', prev_date), ('exp_dt', '=', sdate)] ]
                s1 = self.get_sum_of_OI_for_scrip(scrip, FUTURE, clauses)

                s2 = self.get_sum_of_OI_for_scrip(scrip, OPTION, clauses)

                sum2 = s1 + s2
                
                # dlog.info("for scrip %s sum1 and sum2 for series %s are: %s, %s " % (scrip, _s, sum1, sum2))
                
                sums[_s][scrip] = (sum1, sum2)

                move = sum1 - sum2
                if sum2 == 0:
                    dlog.info('For scrip %s the OI_sum_prev_date is zero' % (scrip))
                    continue

                move_percent = move * 100.0 / sum2
                movements[_s][scrip] = {'scrip': scrip, 'movement': move,
                        'move_percent': move_percent, 'open_int': sum1}

                i += 1


        movements_near = sorted(movements['near'].values(), key=lambda k: k['move_percent'])
        movements_next = sorted(movements['next'].values(), key=lambda k: k['move_percent'])
        movements_far = sorted(movements['far'].values(), key=lambda k: k['move_percent'])


        # TODO: Is it okay to add only 3 series for cumulative ?
        for scrip in scrips:
            if not sums['near'].get(scrip):
                continue

            sum1 =  sums['near'][scrip][0] + sums['next'][scrip][0] + sums['far'][scrip][0]
            sum2 =  sums['near'][scrip][1] + sums['next'][scrip][1] + sums['far'][scrip][1]

            move = sum1 - sum2
            if sum2 == 0:
                dlog.info('For scrip %s the OI_sum_prev_date is zero' % (scrip,))
                continue

            move_percent = move * 100.0 / sum2
            movements['cumulative'][scrip] = {'scrip': scrip, 'movement': move,
                    'move_percent': move_percent, 'open_int': sum1}
            

        movements_cumulative = sorted(movements['cumulative'].values(), key=lambda k: k['move_percent'])

        # TODO: What if nth and n+1th values are same ?
        
        near_incr = [e for e in movements_near if e['move_percent'] > 0][-n:]
        next_incr = [e for e in movements_next if e['move_percent'] > 0][-n:]
        far_incr = [e for e in movements_far if e['move_percent'] > 0][-n:]
        cumulative_incr = [e for e in movements_cumulative if e['move_percent'] > 0][-n:]
        

        near_incr.reverse()
        next_incr.reverse()
        far_incr.reverse()
        cumulative_incr.reverse()

        near_decr = [e for e in movements_near if e['move_percent'] < 0][:n]
        next_decr = [e for e in movements_next if e['move_percent'] < 0][:n]
        far_decr = [e for e in movements_far if e['move_percent'] < 0][:n]
        cumulative_decr = [e for e in movements_cumulative if e['move_percent'] < 0][:n]
        
        data = [
            (near_incr, near_decr),
            (next_incr, next_decr),
            (far_incr, far_decr),
            (cumulative_incr, cumulative_decr),
        ]

        return data

    def generate_data(self, n, date):
        try:
            data = self._generate_data(n, date)
            error = None
        except DBError as fault:
            traceback.print_exc()
            if fault.errno <> ENOTFOUND:
                raise fault
            data = None
            error = EINVALIDINPUT
        return data, error

    def transform_data(self, data, json=False):
        ix = []
        iy = []
        itext = []
        isize = []
        isymbol = []
        icolor = []

        symbols = ['circle', 'square', 'diamond', 'cross']
        cnt = 0
        for d in data:
            x = []
            y = []
            text = []
            size = []
            for i in d[0]:
                x.append(i["scrip"])
                y.append(i["move_percent"])
                text.append("Open interest: %s" %i["open_int"])
                size.append(int(i["move_percent"] * 10))
            ix.append(x)
            iy.append(y)
            itext.append(text)
            isize.append(size)
            isymbol.append(symbols[cnt])
            icolor.append("rgb(93, 164, 214)")
            
            x = []
            y = []
            text = []
            size = []
            for i in d[1]:
                x.append(i["scrip"])
                y.append(i["move_percent"])
                text.append("Open interest: %s" %i["open_int"])
                size.append(int(i["move_percent"] * -10))
            ix.append(x)
            iy.append(y)
            itext.append(text)
            isize.append(size)
            isymbol.append(symbols[cnt])
            icolor.append("rgb(255, 144, 14)")

            cnt += 1

        title = "OI Movements"
        title += " (Top %s Scrips on Date %s)" %(self.input["n"],               
                                                from_pytime_to_str(self.input["date"]))
        
        data = self.plot.plotly.form_plotargs_report4(ix, iy, itext, isize, 
                                                      icolor, isymbol, title)
        data = [data]
        if json:
            data = jsonify(data)

        return data

    def plot_data(self, data):
        self.plot.table.plot_report4(data)

