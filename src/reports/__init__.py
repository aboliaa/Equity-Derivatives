from report1 import Report1DataGetter
from report2 import Report2DataGetter
from report3 import Report3DataGetter
from report4 import Report4DataGetter
from report5 import Report5DataGetter
from report6 import Report6DataGetter
from db.dbops_sqlite3 import SQLite_DBOps
from plot import Plot
from const import DBPATH

class Reports():
    def __init__(self):
        db = SQLite_DBOps(DBPATH)
        plot = Plot()
        self.report1 = Report1DataGetter(db, plot)
        self.report2 = Report2DataGetter(db, plot)
        self.report3 = Report3DataGetter(db, plot)
        self.report4 = Report4DataGetter(db, plot)
        self.report5 = Report5DataGetter(db, plot)
        self.report6 = Report6DataGetter(db, plot)

reports = Reports()
