from utils import *
from const import *

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

