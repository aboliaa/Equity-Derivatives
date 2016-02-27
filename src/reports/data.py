import time

from bisect import bisect

from utils.helper import *
from const import *

__all__ = ["DataGetter", "get_all_scrips", "get_render_data", "get_expiry_series_for_date"]

class DataGetter(object):
    def __init__(self, db):
        self.dbobj = db

    def _dictify_db_data(self, cols, data):
        data = [dict(zip(cols,r)) for r in data]
        return data

    def get_all_scrips(self):
        _spec = { 
                'cols': ['name'],
                'clauses': [ [('type', '=', 'table')] ],
                }
        tables = self.dbobj.select_meta(_spec)
        tables = [x[0] for x in tables]
        tables = [tablename_to_symbol(x) for x in tables if is_scripdata_tablename(x)]
        scrips = list(set(tables))
        scrips.sort()
        return scrips

    def get_day_zero(self):
        return DAY_ZERO

    # TODO: Many of the functions in this class accept scripname as input. 
    # Should we define a class for 'scrip'?
    def get_all_series(self, scrip, derivative_type, date):
        tablename = self.get_tablename_from_scrip(scrip, derivative_type)
        _spec = {
                'tablename' : tablename,
                'cols'      : [ 'exp_dt' ],
                'clauses'   : [ [('timestamp', '=', date)] ]
                }
        return self.dbobj.select(_spec)

    def get_all_series_for_date(self, scrip, date, limit=NUM_SERIES):
        # Get all series of FUTURE and OPTION and union them
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

        if limit:
            return series[:limit]
        else:
            return series

    def get_tablename_from_scrip(self, scrip, derivative_type):
        _spec = {
                'tablename' : 'M_SCRIP_INFO',
                'cols'      : ['instru_type'],
                'clauses'   : [ [('symbol', '=', scrip)] ]
                }
        scrip_info = self.dbobj.select(_spec)
        instru_type = scrip_info[0][0]
        tablename = "%s%s%s_%s" %(DATATABLE_PREFIX,
                                  DERIVATIVE_TYPE_MAP[derivative_type],
                                  REV_INSTRU_TYPE_MAP[instru_type],
                                  scrip)
        return tablename

    def get_scrip_data(self, scrip, derivative_type, cols=None, clauses=None):
        tablename = self.get_tablename_from_scrip(scrip, derivative_type)
        
        if not clauses:
            clauses = []
        if not cols:
            cols = '*'

        _spec = {
                'tablename' : tablename,
                'cols'      : cols,
                'clauses'   : clauses
                }
        result = self.dbobj.select(_spec)
        data = self._dictify_db_data(cols, result)
        return data
 
    def get_aggregate_value(self, scrip, derivative_type, op, col, clauses=[]):
        tablename = self.get_tablename_from_scrip(scrip, derivative_type)

        _spec = {
                'tablename' : tablename,
                'agg'       : [op, col],
                'clauses'   :  clauses
                }
        data = self.dbobj.select(_spec)
        data = data[0][0]
        return data
       
    def get_min_value(self, scrip, derivative_type, col, clauses=[]):
        data = self.get_aggregate_value(scrip, derivative_type, op='min', col=col, clauses=clauses)
        return data
     
    def get_max_value(self, scrip, derivative_type, col, clauses=[]):
        data = self.get_aggregate_value(scrip, derivative_type, op='max', col=col, clauses=clauses)
        return data
       
    def get_sum(self, scrip, derivative_type, col, clauses=[]):
        data = self.get_aggregate_value(scrip, derivative_type, op='sum', col=col, clauses=clauses)
        return data

    def get_latest_date(self):
        return self.get_max_value("NIFTY", FUTURE, 'timestamp')

def get_all_scrips():
    if cache.has_key('scrips') and len(cache['scrips']) > 0:
        scrips = cache['scrips']
    else:
        rd = DataGetter(dbops)
        scrips = rd.get_all_scrips()
        cache['scrips'] = scrips

    return scrips

def get_latest_date():
    rd = DataGetter(dbops)
    return rd.get_latest_date()

def get_render_data():
    data = {}                                                               
    data["scrips"] = get_all_scrips()
    data["day_zero"] = DAY_ZERO
    ldate = get_latest_date()
    _ldate = from_pytime_to_str(ldate, "%d-%b-%Y")
    data['latest_date'] = _ldate
    return data

def get_expiry_series_for_date(scrip, date, limit=NUM_SERIES):
    if cache.has_key('expiry_series') and len(cache['expiry_series']) > 0:
        datestr = from_pytime_to_str(date)
        index = bisect(cache['expiry_series'], datestr)
        if len(cache['expiry_series']) >= (index-1 + NUM_SERIES):
            series = cache['expiry_series'][index:index+NUM_SERIES]
            series = [from_str_to_pytime(s) for s in series]
            return series
    cache['expiry_series'] = []

    rd = DataGetter(dbops)
    series = rd.get_all_series_for_date(scrip, date, limit)

    for s in series:
        sdate = from_pytime_to_str(s)
        index = bisect(cache['expiry_series'], sdate)
        cache['expiry_series'].insert(index, sdate)

    return series

