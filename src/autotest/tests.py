# List of methods which will be called for autotest purpose

from reports import reports

from utils.helper import from_str_to_pytime

from autotest import verify

def report_1(dbname):
    r1 = reports.report1
    # TODO: Better way to pick scrip randomly
    scrip = "NIFTY"
    # TODO: Better way to pick date randomly
    date = from_str_to_pytime("2015-12-24")
    data = r1.generate_data(scrip, date)
    csvfilepath = '/Users/amitkulkarni/bhavcopies/fo24DEC2015bhav.csv'
    f = open(csvfilepath, 'r')
    # TODO: Verify header ?
    f.readline()
    result = verify.verify_report_1(scrip, data, f)
    f.close()
    return result

def report_2(dbname):
    r2 = reports.report2
    # TODO: Better way to pick scrip randomly
    scrip = "NIFTY"
    data = r2.generate_data(scrip)
    # TODO: Better way to pick all csv files
    csvfiles = [
            '/Users/amitkulkarni/bhavcopies/fo21DEC2015bhav.csv',
            '/Users/amitkulkarni/bhavcopies/fo22DEC2015bhav.csv',
            '/Users/amitkulkarni/bhavcopies/fo23DEC2015bhav.csv',
            '/Users/amitkulkarni/bhavcopies/fo24DEC2015bhav.csv',
    ]
    file_list = []
    for csvfile in csvfiles:
        f = open(csvfile, "r")
        # TODO: Verify header ?
        f.readline()
        file_list.append(f)
    result = verify.verify_report_2(scrip, data, file_list)

    for f in file_list:
        f.close()

    return result


def report_3(dbname):
    r3 = reports.report3
    # TODO: Better way to pick scrip randomly
    scrip = "SBIN"
    data = r3.generate_data(scrip)
    # TODO: Better way to pick all csv files
    csvfiles = [
            '/Users/amitkulkarni/bhavcopies/fo21DEC2015bhav.csv',
            '/Users/amitkulkarni/bhavcopies/fo22DEC2015bhav.csv',
            '/Users/amitkulkarni/bhavcopies/fo23DEC2015bhav.csv',
            '/Users/amitkulkarni/bhavcopies/fo24DEC2015bhav.csv',
    ]
    file_list = []
    for csvfile in csvfiles:
        f = open(csvfile, "r")
        # TODO: Verify header ?
        f.readline()
        file_list.append(f)
    result = verify.verify_report_3(scrip, data, file_list)

    for f in file_list:
        f.close()

    return result

