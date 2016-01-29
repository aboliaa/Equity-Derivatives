from report1 import Report1DataGetter
from report2 import Report2DataGetter
from report3 import Report3DataGetter
from report4 import Report4DataGetter
from report5 import Report5DataGetter
from report6 import Report6DataGetter
from plot import Plot
from const import DBPATH

class Reports():
    def __init__(self):
        db = dbops
        plot = Plot()
        self.report1 = Report1DataGetter(db, plot)
        self.report2 = Report2DataGetter(db, plot)
        self.report3 = Report3DataGetter(db, plot)
        self.report4 = Report4DataGetter(db, plot)
        self.report5 = Report5DataGetter(db, plot)
        self.report6 = Report6DataGetter(db, plot)
    
    def get_render_data(self):
        return self.report1.get_data_for_input()

reports = Reports()
