import os
import shutil
import time
import json
from glob import glob
from datetime import datetime,timedelta

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

