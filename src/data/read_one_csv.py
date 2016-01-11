from utils import log
from const import *

HEADERS_V1 = [
    "INSTRUMENT", "SYMBOL", "EXPIRY_DT", "STRIKE_PR", "OPTION_TYP", 
    "OPEN", "HIGH", "LOW", "CLOSE", "SETTLE_PR", "CONTRACTS", 
    "VAL_INLAKH", "OPEN_INT", "CHG_IN_OI", "TIMESTAMP"
]

class CSVReader():
    def __init__(self, filepath):
        self.filepath = filepath
        self.f = open(self.filepath, "r")
        self.read_header()

    def walk(self):
        while True:
            l = self.f.readline()
            if l == "\n":
                continue
            if not l:
                break
            values = l.split(',')
            idx = IDX_MAP[values[0]]
            otype = OPT_TYPE_MAP[values[4]]
            symbol, exp_dt, strike_pr = values[1], values[2], float(values[3])
            _open, high, low = values[5], values[6], values[7]
            close, settle_pr, contracts = values[8], values[9], long(values[10])
            val, open_int, change = values[11], long(values[12]), values[13]
            timestamp = values[14]
            yield (idx, symbol, exp_dt, strike_pr, otype, _open, high, low,
                   close, settle_pr, contracts, val, open_int, change, 
                   timestamp)

    def read_header(self):
        l = self.f.readline()
        headers = l.split(',')
        if headers[-1] == "\n":
            headers = headers[:-1]
        # print 'headers = ', headers
        # print 'HEADERS_V1 = ', HEADERS_V1
        if headers <>  HEADERS_V1:
            log.log("Headers changed! new headers = %s", headers)
            raise Exception("New Headers")

    def __del__(self):
        self.f.close()        

if __name__ == '__main__':
    fname = '/Users/amitkulkarni/Downloads/fo14DEC2015bhav.csv'
    r = CSVReader(fname)
    for e in r.walk():
        print e

