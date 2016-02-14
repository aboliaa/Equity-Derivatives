import time
import traceback

from const import *
from utils.helper import *
from error import *                                                             
from db.dberror import *
from data import *

class Report6DataGetter(DataGetter):
    def __init__(self, db, plot):
        super(Report6DataGetter, self).__init__(db)
        self.plot = plot

    def validate_input(self, date):
        # TODO: Ideally db layer should raise this exception 
        clauses = [ [('timestamp', '=', date)] ]
        data = self.get_scrip_data("NIFTY", OPTION, cols=None, clauses=clauses)
        if not data:
            raise DBError(ENOTFOUND)

    def _generate_data(self, n, date):
        strdate = from_pytime_to_str(date)
        dlog.info("Report6, n=%s, Date=%s" % (n, strdate,))
        rlog.info("Report6,%s,%s" % (n, strdate,))

        dlog.info("Starting to generate Report6")

        self.validate_input(date)
        self.input = {"n": n, "date": date}
        scrips = get_all_scrips()
       
        data = {'calls': {}, 'puts': {}}

        dlog.info("Ignoring the scrips %s" % (ignore_scrips,))
        for scrip in scrips:
            if scrip in ignore_scrips:
                continue

            try:
                clauses = [ [('timestamp', '=', date), ('opt_type', '=', CE)] ]
                max_contracts = self.get_max_value(scrip, OPTION, 'contracts', clauses=clauses)
                data['calls'][scrip] = {'scrip': scrip, 'max_contracts': max_contracts} 
            except:
                # dlog.info(traceback.format_exc())
                dlog.error("Exception in getting calls for scrip %s" % (scrip,))
                continue

            try: 
                clauses = [ [('timestamp', '=', date), ('opt_type', '=', PE)] ]
                max_contracts = self.get_max_value(scrip, OPTION, 'contracts', clauses=clauses)
                data['puts'][scrip] = {'scrip': scrip, 'max_contracts': max_contracts}
            except:
                # dlog.info(traceback.format_exc())
                dlog.error("Exception in getting puts for scrip %s" % (scrip,))
                continue


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

    def generate_data(self, n, date):
        try:
            data = self._generate_data(n, date)
            error = None
        except DBError as fault:
            dlog.info(traceback.format_exc())
            if fault.errno <> ENOTFOUND:
                raise fault
            data = None
            error = EINVALIDINPUT
        return data, error

    def transform_data(self, data, json=False):
        x1 = []
        y1 = []
        text1 = []
        i = 1
        for d in sorted(data["calls"], key=lambda x:x["max_contracts"], reverse=True):
            x1.append(i)
            i += 1
            y1.append(d["max_contracts"])
            text1.append("Contracts: %s <br>Strike Price: %s <br>Expiry Series: %s" %(d3(d["max_contracts"]),
                                                                d3(d["strike_pr"]),
                                                                time.strftime("%d-%b-%Y", d["exp_dt"])))
        
        x2 = []
        y2 = []
        text2 = []
        for d in sorted(data["puts"], key=lambda x:x["max_contracts"], reverse=True):
            x2.append(i)
            i += 1
            y2.append(d["max_contracts"])
            text2.append("Contracts: %s <br>Strike Price: %s <br>Expiry Series: %s" %(d3(d["max_contracts"]),
                                                                d3(d["strike_pr"]),
                                                                time.strftime("%d-%b-%Y", d["exp_dt"])))

        tickval = range(1,i)
        ticktext = [d["scrip"] for d in data["puts"]] + [d["scrip"] for d in data["calls"]]

        title = "Most Active CALLs and PUTs"
        title += " (Top %s Scrips on %s)" %(self.input["n"],
                                                from_pytime_to_str(self.input["date"]))

        data = self.plot.plotly.form_plotargs_report6(x1, y1, text1, 
                                                      x2, y2, text2,
                                                      title, tickval, ticktext)
        data = [data]
        if json:
            data = jsonify(data)

        dlog.info("Done generating Report6")
        return data 

    def plot_data(self, data):
        self.plot.table.plot_report6(data)

