from const import DBPATH

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Holidays(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.holidays = self._get_from_db()

    def __contains__(self, k):
        if k in self.holidays:
            return True
        else:
            return False

    def _get_from_db(self):
        spec = {                                                                
                'tablename': 'P_HOLIDAYS',                                            
                'cols': ['day'],                                                    
               }                                                                       
        holidays = dbops.select(spec)
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

    return False


