import os
import time

from const import DBPATH, HOMEDIR

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Holidays(object):
    __metaclass__ = Singleton

    def __init__(self):
        # self.holidays = self._get_from_db()
        self.holidays = self._get_from_file()

    def __contains__(self, k):
        if k in self.holidays:
            return True
        else:
            return False
    
    def __iter__(self):
        self.i = 0
        return self

    def next(self):
        if self.i >= len(self.holidays):
            raise StopIteration
        h = self.holidays[self.i]
        self.i += 1
        return h
    
    def _get_from_db(self):
        spec = {                                                                
                'tablename': 'P_HOLIDAYS',                                            
                'cols': ['day'],                                                    
               }                                                                       
        holidays = dbops.select(spec)
        return holidays

    def _get_from_file(self):
        holidays = []
        f = open(os.path.join(HOMEDIR, "holidays.txt"), "r")
        while True:
            l = f.readline()
            if not l:
                break

            ll = l.split()
            h = time.strptime(ll[0], "%d-%b-%Y")
            holidays.append(h)
        f.close()
        return holidays

def is_holiday(date):
    ''' date is timetuple '''

    SATURDAY = 5
    SUNDAY = 6

    if date.tm_wday in [SATURDAY, SUNDAY]:
        return True

    NSE_holidays = Holidays()
    if date in NSE_holidays:
        return True

    # Ideally all dates should Date class objects.
    for d in NSE_holidays:
        y = d.tm_year == date.tm_year
        m = d.tm_mon == date.tm_mon
        md = d.tm_mday == date.tm_mday
        if y and m and md:
            return True

    return False

