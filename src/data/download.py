import os
import subprocess
import time
from datetime import datetime, timedelta

DATE_FORMAT = "%d%b%Y"
DOWNLOAD_PATH = "/Users/amitkulkarni/Downloaded_Bhavcopies"

def datetimeIterator(from_date, to_date, delta=timedelta(days=1)):
    from_date = time.strptime(from_date, DATE_FORMAT)
    to_date = time.strptime(to_date, DATE_FORMAT)
    from_date = datetime.fromtimestamp(time.mktime(from_date))
    to_date = datetime.fromtimestamp(time.mktime(to_date))

    while from_date <= to_date:
        strtime = time.strftime(DATE_FORMAT, from_date.date().timetuple()).upper()
        yield strtime 
        from_date = from_date + delta

def get_month(date):
    return date[2:5]

def get_year(date):
    return date[-4:]

def download_bhavcopy(date):
    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:42.0) Gecko/20100101 Firefox/42.0"
    referer = "http://www.nseindia.com/products/content/derivatives/equities/archieve_fo.htm"

    year = get_year(date)
    month = get_month(date)
    url = "http://www.nseindia.com/content/historical/DERIVATIVES/%s/%s/fo%sbhav.csv.zip" %(year, month, date)

    path = os.path.join(DOWNLOAD_PATH, year, month+year)
    zippath = os.path.join(path, "fo%sbhav.csv.zip" %date)
    if not os.path.exists(path):
        os.makedirs(path)
    if os.path.exists(zippath):
        return

    command = ["wget", 
                "--user-agent=%s"%user_agent, 
                "--directory-prefix=%s"%path,
                "--referer=%s"%referer, 
                url]
    # print command

    subprocess.Popen(command, stdout=None, stderr=None, shell=False)


if __name__ == "__main__":

    from_date = "01JAN2008"
    to_date = "31DEC2008"

    
    previous_month = None
    for dt in datetimeIterator(from_date, to_date):
        
        current_month = get_month(dt)
        if previous_month and (current_month != previous_month):
            print "************************** TIME TO SLEEP"
            time.sleep(100)
        
        print "Downloading bhavcopy for date", dt
        try:
            download_bhavcopy(dt)
            previous_month = current_month
        except:
            pass


