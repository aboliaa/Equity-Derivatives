# Implement verification methods

import copy

from const import *

from utils.helper import get_date
from utils.helper import from_pytime_to_str

SUCCESS = 1
FAILED = 0

def get_records(f, n=None, scrip=None, opt_only=False, fut_only=None):
    i = 0
    while True:
        if n and i > n:
            break

        line = f.readline()
        if not line:
            break

        elements = line.split(",")
        if opt_only and not elements[0].startswith("OPT"):
            continue

        if fut_only and not elements[0].startswith("FUT"):
            continue

        if scrip and elements[1] <> scrip:
            continue

        yield elements
        i += 1

def verify_report_1(scrip, data, f): 
    result = SUCCESS
    for e in get_records(f, n=10, scrip=scrip, opt_only=True):
        open_int = long(e[12])
        # TODO: Convert date to python date
        exp_dt = from_pytime_to_str(get_date(e[2]))
        strike_pr = float(e[3])
        opt_type = OPT_TYPE_MAP[e[4]]
        d = {'open_int': open_int, 'exp_dt': exp_dt, 'strike_pr': strike_pr,
             'opt_type': opt_type}
        if d not in data:
            dlog.info('%s not found in data' % (d,))
            dlog.info('data = %s' % (data,))
            result = FAILED
    return result

def verify_report_2(scrip, data, files):
    result = SUCCESS
    for f in files:
        # dlog.info("starting verifiecation for a csv file")
        near_series = None
        near_series_record = None
        date = None
        sumOI = 0
        for e in get_records(f, scrip=scrip):
            if e[0].startswith("FUT"):
                # dlog.info("got a record : %s" % (e,))
                date = from_pytime_to_str(get_date(e[14]))
                exp_dt = from_pytime_to_str(get_date(e[2]))
                if not near_series:
                    near_series = exp_dt
                    near_series_record = copy.deepcopy(e)
                if exp_dt < near_series:
                    near_series = exp_dt
                    near_series_record = copy.deepcopy(e)
            sumOI += long(e[12])
            
        if not date:
            dlog.info("Date missing")
            result = FAILED

        # TODO: Detailed cases like that scrip actually was not there on that date

        settle_pr = near_series_record[9]
        if data[date]['settlement_price'] <> float(settle_pr):
            dlog.info('Near series settlement price for date %s does not match' % (date,))
            result = FAILED
        
        if data[date]['summation_of_OI'] <> sumOI:
            dlog.info('Sum of OI does not match')
            result = FAILED 
        # dlog.info("Settlement price verified")
    return result

def verify_report_3(scrip, data, files):
    result = SUCCESS
    for f in files:
        # dlog.info("starting verifiecation for a csv file")
        near_series = None
        near_series_record = None
        date = None
        sum_puts_oi, sum_puts_trade = 0, 0
        sum_calls_oi, sum_calls_trade = 0, 0
        for e in get_records(f, scrip=scrip):
            if e[0].startswith("FUT"):
                # dlog.info("got a record : %s" % (e,))
                date = from_pytime_to_str(get_date(e[14]))
                exp_dt = from_pytime_to_str(get_date(e[2]))
                if not near_series:
                    near_series = exp_dt
                    near_series_record = copy.deepcopy(e)
                if exp_dt < near_series:
                    near_series = exp_dt
                    near_series_record = copy.deepcopy(e)
            otype = OPT_TYPE_MAP[e[4]]
            oi = long(e[12])
            trade = long(e[10])
            if otype == CE:
                sum_calls_oi += oi
                sum_calls_trade += trade
            if otype == PE:
                sum_puts_oi += oi
                sum_puts_trade += trade
 
        if not date:
            dlog.info("Date missing")
            result = FAILED

        # TODO: Detailed cases like that scrip actually was not there on that date

        settle_pr = near_series_record[9]
        if data[date]['settlement_price'] <> float(settle_pr):
            dlog.info('Near series settlement price for date %s does not match' % (date,))
            result = FAILED
        # dlog.info("Settlement price verified")

        pcr_oi = float(sum_puts_oi) / float(sum_calls_oi)
        if data[date]['PCR_OI'] <> pcr_oi:
            dlog.info('PCR OI for date %s does not match' % (date,))
            result = FAILED
 
        pcr_trade = float(sum_puts_trade) / float(sum_calls_trade)
        if data[date]['PCR_trade'] <> pcr_trade:
            dlog.info('PCR trade for date %s does not match' % (date,))
            result = FAILED

    return result

