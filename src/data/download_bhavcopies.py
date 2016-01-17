'''
A scrip to download bhavcopies for Equity derivatives from NSE website
http://www.nseindia.com/products/content/derivatives/equities/archieve_fo.htm

Equity derivatives were commenced in June 2000, but bhavcopies are available 
from September 2000. Format of the bhavcopies remains the same.

Usage:
    python download_bhavcopies.py --from=<from-date> --to=<to-date> --outdir=<path>
    Dates are ddBYYYY, e.g. 01JAN2001

Author: Aboli Aradhye <aboli.a.aradhye@gmail.com> January 2016
'''

import os
import subprocess
import time
from optparse import OptionParser
from datetime import datetime, timedelta

DATE_FORMAT = "%d%b%Y"

def is_holiday(date):
    ''' date is timetuple '''
    SATURDAY = 5
    SUNDAY = 6

    # TODO: Also skip NSE holidays
    if date.tm_wday in [SATURDAY, SUNDAY]:
        return True
    return False

def datetimeIterator(from_date, to_date, delta=timedelta(days=1)):
    from_date = time.strptime(from_date, DATE_FORMAT)
    to_date = time.strptime(to_date, DATE_FORMAT)
    from_date = datetime.fromtimestamp(time.mktime(from_date))
    to_date = datetime.fromtimestamp(time.mktime(to_date))

    while from_date <= to_date:
        date = from_date.date().timetuple()
        if is_holiday(date):
            pass
        else:
            strtime = time.strftime(DATE_FORMAT, from_date.date().timetuple()).upper()
            yield strtime 
        from_date = from_date + delta

def get_month(date):
    return date[2:5]

def get_year(date):
    return date[-4:]

def download_bhavcopy(date, path):
    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:42.0) Gecko/20100101 Firefox/42.0"
    referer = "http://www.nseindia.com/products/content/derivatives/equities/archieve_fo.htm"

    year = get_year(date)
    month = get_month(date)
    url = "http://www.nseindia.com/content/historical/DERIVATIVES/%s/%s/fo%sbhav.csv.zip" %(year, month, date)

    path = os.path.expanduser(path)
    path = os.path.join(path, year, month+year)
    zippath = os.path.join(path, "fo%sbhav.csv.zip" %date)
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(zippath):
        return

    print "Downloading bhavcopy for date", date
    command = ["wget", 
                "--user-agent=%s"%user_agent, 
                "--directory-prefix=%s"%path,
                "--referer=%s"%referer, 
                url]
    subprocess.Popen(command, stdout=None, stderr=None, shell=False)

def parse_options():
    parser = OptionParser()                                                     
    parser.add_option("--from", dest="from_date")
    parser.add_option("--to", dest="to_date")
    parser.add_option("--outdir", dest="path", default=".")
    options, _ = parser.parse_args()
    return options

if __name__ == "__main__":

    options = parse_options()
    from_date = options.from_date
    to_date = options.to_date
    path = options.path

    print "From date =", from_date
    print "To date =", to_date
    print "Out dir =", path

    previous_month = None
    for dt in datetimeIterator(from_date, to_date):
        
        current_month = get_month(dt)
        if previous_month and (current_month != previous_month):
            print "TIME TO SLEEP"
            time.sleep(100)
        
        try:
            download_bhavcopy(dt, path)
            previous_month = current_month
        except:
            pass

