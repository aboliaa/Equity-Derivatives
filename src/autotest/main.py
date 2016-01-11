# Run this file to run all the testcases in config file

# TODO: Ideally, we should use unittest

from utils.log import log

from autotest.config import testcases

SUCCESS = 1
FAILED = 0

dbname = '/Users/amitkulkarni/temp_Derivatives/populate_test_4csv.db'

def run(tc):
    result = tc(dbname)
    return result

def main():
    success = 0
    failed = 0
    log("Test excution started")
    for tc in testcases:
        log('Running ' + tc.__name__)
        result = run(tc)
        if result == SUCCESS:
            log(tc.__name__ + ' Successful')
        else:
            log( tc.__name__ + ' Failed')
    log("Test excution complete")
            
if  __name__ == '__main__':
    main()

