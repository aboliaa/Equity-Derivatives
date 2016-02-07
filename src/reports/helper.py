from const import *
from error import *
from db.dberror import *
from data import DataGetter

__all__ = ["get_all_scrips", "get_render_data"]

class ReportDataGetter(DataGetter):
    def __init__(self, db):
        super(ReportDataGetter, self).__init__(db)

def get_all_scrips():
    if cache.has_key('scrips') and len(cache['scrips']) > 0:
        print "********************** SCRIPS GET FROM CACHE"
        scrips = cache['scrips']
    else:
        print "********************** SCRIPS GET FROM DB"
        rd = ReportDataGetter(dbops)
        scrips = rd.get_all_scrips()
        cache['scrips'] = scrips

    return scrips

def get_render_data():
    data = {}                                                               
    data["scrips"] = get_all_scrips()                                  
    data["day_zero"] = DAY_ZERO                       
    return data

def get_expiry_series_for_date(scrip, date, limit=NUM_SERIES):
    pass
