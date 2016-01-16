# Run this file to run all the testcases in config file

# TODO: Ideally, we should use unittest

from autotest.config import testcases

SUCCESS = 1
FAILED = 0

# TODO; use const.DBPATH
dbname = '/Users/amitkulkarni/temp_Derivatives/populate_test_4csv.db'

def run(tc):
    result = tc(dbname)
    return result

def main():
    debuglogger = log.Logger(DEBUGLOG)
    __builtins__.dlog = debuglogger

    requestlogger = log.Logger(NULLLOG)
    __builtins__.rlog = requestlogger

    success = 0
    failed = 0
    dlog.info("Test excution started")
    for tc in testcases:
        dlog.info('Running ' + tc.__name__)
        result = run(tc)
        if result == SUCCESS:
            dlog.info(tc.__name__ + ' Successful')
        else:
            dlog.info( tc.__name__ + ' Failed')
    dlog.info("Test excution complete")
            
if  __name__ == '__main__':
    main()

