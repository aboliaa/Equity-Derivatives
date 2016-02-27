import traceback

from utils.helper import *
from const import *
from error import *                                                             
from db.dberror import *
from data import *

class Report4DataGetter(DataGetter):
    def __init__(self, db, plot):
        super(Report4DataGetter, self).__init__(db)
        self.plot = plot

    def get_sum_of_OI_for_scrip(self, scrip, derivative_type, clauses):
        try:
            s = self.get_sum(scrip, derivative_type, 'open_int', clauses=clauses)
        except:
            # TODO: Ideally we should handle specific errors here
            dlog.error("Exception in getting data for %s:%s" % (scrip, derivative_type))
            s = 0

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
        dlog.info("Report4, n=%s, Date=%s" % (n, strdate))
        rlog.info("Report4,%s,%s" % (n, strdate))

        dlog.info("Starting to generate Report4")

        self.validate_input(n, date)
        self.input = {"n": n, "date": date}

        sums = {'near': {}, 'next': {}, 'far': {}}
        movements = {'near': {}, 'next': {}, 'far': {}, 'cumulative': {}}
        scrips = get_all_scrips()
        dlog.info("date=%s" % date)
        prev_date = get_prev_date(date)
        dlog.info("prev_date=%s" % prev_date)

        dlog.info("Ignoring the scrips %s" % (ignore_scrips,))
        for scrip in scrips:
            if scrip in ignore_scrips:
                continue

            """
            series = get_expiry_series_for_date(scrip, date)
            pseries = get_expiry_series_for_date(scrip, prev_date)
            """

            series = get_exp_series(date)
            pseries = get_exp_series(prev_date)
            
            if len(series) < 3:
                dlog.error("For scrip %s there are less than 3 series" % (scrip,))
                continue
            if len(pseries) < 3:
                dlog.error("For scrip %s there are less than 3 series for previous day" % (scrip,))
                continue

            i = 0
            for _s in ['near', 'next', 'far']:
                sdate = series[i]
                psdate = pseries[i]

                clauses = [ [('timestamp', '=', date), ('exp_dt', '=', sdate)] ]
                s1 = self.get_sum_of_OI_for_scrip(scrip, FUTURE, clauses)
                s2 = self.get_sum_of_OI_for_scrip(scrip, OPTION, clauses)
                sum1 = s1 + s2

                clauses = [ [('timestamp', '=', prev_date), ('exp_dt', '=', psdate)] ]
                s1 = self.get_sum_of_OI_for_scrip(scrip, FUTURE, clauses)
                s2 = self.get_sum_of_OI_for_scrip(scrip, OPTION, clauses)
                sum2 = s1 + s2
                
                # dlog.info("for scrip %s sum1 and sum2 for series %s are: %s, %s " % (scrip, _s, sum1, sum2))
                
                sums[_s][scrip] = (sum1, sum2)

                move = sum1 - sum2
                if sum2 == 0:
                    if sum1 <> 0:
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
            dlog.error(traceback.format_exc())
            if fault.errno <> ENOTFOUND:
                raise fault
            data = None
            error = EINVALIDINPUT
        return data, error

    def transform_data(self, data, json=False):

        cnt = 0
        plotdata = []
        series_map = {
                        0: "Near Series",        
                        1: "Next Series",        
                        2: "Far Series",        
                        3: "Cumulative Series" 
                     }

        for d in data:

            x1 = [i["scrip"] for i in d[0]]
            y1 = [i["move_percent"] for i in d[0]]
            t1 = ["Change in OI: %s%% <br>Open interest: %s" %(d3(i["move_percent"]), d3(i["open_int"])) for i in d[0]]
            
            x2 = [i["scrip"] for i in d[1]]
            y2 = [i["move_percent"] for i in d[1]]
            t2 = ["Change in OI: %s%% <br>Open interest: %s" %(d3(i["move_percent"]), d3(i["open_int"])) for i in d[1]]

            
            title = "OI Movements: %s" %series_map[cnt]
            title += " (Top %s Scrips on %s)" %(self.input["n"],               
                                                from_pytime_to_str(self.input["date"], "%d-%b-%Y"))
        
            plotdata.append(self.plot.plotly.form_plotargs_report4([x1,x2], [y1,y2], [t1,t2], title))
            cnt += 1
            
        if json:
            plotdata = jsonify(plotdata)

        dlog.info("Done generating Report4")
        return plotdata

    def plot_data(self, data):
        self.plot.table.plot_report4(data)

