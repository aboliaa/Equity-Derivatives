import os
import shutil
import time
import json
from glob import glob
from datetime import datetime,timedelta
import calendar

import const
from holidays import is_holiday

def get_tablename(idx, symbol):
    idx_str = const.REV_IDX_MAP[idx]
    return const.DATATABLE_PREFIX + idx_str + "_" + symbol

def get_date(time_str):
    return time.strptime(time_str, "%d-%b-%Y")

def tablename_to_idx(tablename):
    return tablename.split("_")[1]

def tablename_to_symbol(tablename):
    return tablename.split("_")[2]

def is_scripdata_tablename(tablename):
    return tablename.startswith(const.DATATABLE_PREFIX)
 
def from_pytime_to_str(pytime):
    # TODO: move all time format strings to const
    return time.strftime("%Y-%m-%d", pytime)

def from_str_to_pytime(strtime):
    try:
        t = time.strptime(strtime, "%Y-%m-%d")
    except ValueError:
        t = None
    return t

def datetimeIterator(from_date, to_date, delta=timedelta(days=1), skip_holidays=True):

    from_date = datetime.fromtimestamp(time.mktime(from_date))
    to_date = datetime.fromtimestamp(time.mktime(to_date))

    while from_date <= to_date:
        date = from_date.date().timetuple()

        if skip_holidays and is_holiday(date):
            pass
        else:
            yield date
        from_date = from_date + delta

def get_prev_date(date, skip_holidays=True):
    dt = datetime.fromtimestamp(time.mktime(date))
    delta = timedelta(days=1)
    while True:
        dt = dt - timedelta(days=1)
        if not skip_holidays:
            break
        _dt = dt.date().timetuple()
        if not is_holiday(_dt):
            break
    return dt.date().timetuple()

def jsonify(data):
    return json.dumps(data)

def remove_path(path):
    if not path.startswith(const.PLOT_PATH):
        return

    if os.path.isdir(path):
        # Path is a folder
        if os.path.exists(path):
            shutil.rmtree(path)
    else:
        # Path is a file
        if os.path.exists(path):
            os.remove(path)

def remove_fileglob(path):
    for p in glob(path):
        remove_path(p)

def get_last_day_of_month(y, m, day):
    month = calendar.monthcalendar(y, m)
    days = [week[day] for week in month if week[day]>0]
    return days[-1]

def next_day(date):
    dt = datetime.fromtimestamp(time.mktime(date))
    dt = dt + timedelta(days=1)
    return dt.date().timetuple()

def get_exp_series(date, limit=const.NUM_SERIES):
    l = []
    dt = date
    for i in range(limit):
        y, m = dt.tm_year, dt.tm_mon
        last = get_last_day_of_month(y, m, 3)
        if last < dt.tm_mday:
            m = m + 1
            if m > 12:
                y = y + 1
                m = 1
            last = get_last_day_of_month(y, m, 3)
        
        exp = time.struct_time((y, m, last, 0, 0, 0, 3, 0, 0))
        if is_holiday(exp):
            exp = get_prev_date(exp)

        # We need to dump-load pytime to ensure that it works fine
        str_time = from_pytime_to_str(exp)
        exp = from_str_to_pytime(str_time)

        l.append(exp)
        dt = next_day(exp)

    return l

def get_date_range(date):
    l = []
    series = get_exp_series(date, limit=1)
    expiry = series[0]
    dt = date
    l.append(dt)
    while True:
        dt = next_day(dt)
        if dt > expiry:
            break
        if is_holiday(dt):
            continue
        l.append(dt)
    return l

def d3(value):
    def _add_comma(i):
        if i%2 == 1 and i > 2:
            return True

    splits = str(round(value,2)).split(".")
    value = splits[0]
    if len(splits) == 2:
        fraction = splits[1]
    else:
        fraction = None

    r = []
    for i,c in enumerate(value[::-1]):
        if _add_comma(i):
            r.append(',')
        r.append(c)

    d3val = "".join(r[::-1])
    if fraction:
        d3val += "." + fraction[:2]

    return "".join(r[::-1])
 
