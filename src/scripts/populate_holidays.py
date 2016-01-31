import time
import sys

from db import dbops_sqlite3
from utils.helper import from_pytime_to_str
from const import *
from utils import log

CDBOps = dbops_sqlite3.SQLite_DBOps

class HolidayPopulator:
    def __init__(self, dbname):
        self.dbname = dbname
        self.init_dbops()
        self.check_holidays_table()

    def init_dbops(self):
        self.dbops = CDBOps(self.dbname)

    def check_holidays_table(self):
        spec = {
                'cols': ['name'], 
                'clauses': [[('type', '=', 'table'), ('name', '=', 'P_HOLIDAYS')]]
                }
        table = self.dbops.select_meta(spec)
        if not table:
            spec = {
                'primary_key'   : [('day', 'date')],
                'non_key'       : [('name', 'varchar(64)')],
                'tablename'     : 'P_HOLIDAYS',
            }
            self.dbops.create(spec)
            dlog.info("Creating Holiday Table")

    def insert(self, date, name):
        spec = {
                'tablename': 'P_HOLIDAYS',
                'values': [ ('day', date), ('name', name) ]
                }
        self.dbops.put(spec)

    def populate(self, f):
        while True:
            l = f.readline()
            if not l:
                break
            
            ll = l.split(" ", 1)
            d, name = ll[0], ll[1]
            _d = time.strptime(d, "%d-%b-%Y")
            self.insert(_d, name)

if __name__ == "__main__":
    __builtins__.dlog = log.Logger('stdout', logname='stdout')

    filepath = sys.argv[1]
    dlog.info('filepath = %s' % (filepath,))
    f = open(filepath, "r")

    Populator = HolidayPopulator(DBPATH)
    Populator.populate(f)
    f.close()

