import os
import time
import traceback

from utils import log
from utils import from_pytime_to_str
from data.populate_one_csv import Populator
from db import dbops_sqlite3
from const import *

CDBOps = dbops_sqlite3.SQLite_DBOps

class DailyUpdate:
    def __init__(self, dbname, csvstore):
        self.dbname = dbname
        # TODO: need to improve for mysql where username and passwd is needed
        self.csvstore = csvstore
        self.init_dbops()
        self.check_csv_db()
        self.populator = Populator(self.dbops)

    def init_dbops(self):
        self.dbops = CDBOps(self.dbname)

    def check_csv_db(self):
        spec = {
                'cols': ['name'], 
                'clauses': [[('type', '=', 'table'), ('name', '=', 'P_CSVS')]]
                }
        csvs = self.dbops.select_meta(spec)
        # dlog.debug('csvs = %s' % (csvs,))
        if not csvs:
            spec = {
                    'primary_key': [('timestamp', 'date')],
                    'non_key' : [],
                    'tablename': 'P_CSVS',
                    }
            self.dbops.create(spec)
            dlog.info('P_CSVS table created')

    def get_csvs_in_store(self):
        """
        Assuming that all csvs in store will be at the top level
        directory. If there is directory hierarchy in the store,
        the code will ignore the subdirectories and csv files
        inside subdirectories.
        """
        csvs = list()
        for f in os.listdir(self.csvstore):
            if f.endswith(".csv"):
                csvs.append(os.path.join(self.csvstore, f))
        return csvs

    def get_csvs_in_db(self):
        spec = {
                'cols': ['timestamp'],
                'tablename': 'P_CSVS',
                }
        l = self.dbops.select(spec)
        return [x[0] for x in l]
    
    def put_csv_in_db(self, timestamp):
        spec = {
                'tablename': 'P_CSVS',
                'values': [ ('timestamp', timestamp) ]
                }
        self.dbops.put(spec)
    
    def start(self):
        dlog.info("Starting daily update of csvs")
        csvs_store = self.get_csvs_in_store()
        csvs_db = self.get_csvs_in_db()
        dlog.info('csvs_db = %s' % (csvs_db,))
        for csv in csvs_store:
            dlog.info("CSV %s found." % (csv,))
            csvname = csv.split(os.path.sep)[-1].split(".")[0]
            csvdate = csvname[2:11]
            timestamp = time.strptime(csvdate, "%d%b%Y")
            tsname = from_pytime_to_str(timestamp)
            if tsname in csvs_db:
                continue

            try:
                p = Populator(self.dbops)
                p.start([csv])
            except:
                traceback.print_exc()
                dlog.info("Population failed for %s" % (csv,))
            else:
                self.put_csv_in_db(timestamp)
                dlog.info("Population done for %s" % (csv,))

        dlog.info("Done with daily update of csvs")

if __name__ == "__main__":
    __builtins__.dlog = log.Logger('stdout', logname='stdout')
    # __builtins__.rlog = log.Logger(NULLLOG)

    dbname = "/Users/amitkulkarni/temp_Derivatives/daily_update_1.db"
    updater = DailyUpdate(DBPATH, CSVSTORE)
    updater.start()

