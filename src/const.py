import sys
import os

# Types of derivatives
OPTION = 1
FUTURE = 2

# Types of indexes
FUTIDX = 1
FUTSTK = 2
FUTIVX = 3
OPTIDX = 4
OPTSTK = 5 

# Option types
XX = 0
CE = 1
PE = 2

IDX_MAP = {
    "FUTIDX": FUTIDX, 
    "FUTSTK": FUTSTK, 
    "FUTIVX": FUTIVX, 
    "OPTIDX": OPTIDX, 
    "OPTSTK": OPTSTK,
}

INDEX = 1
STOCK = 2

DERIVATIVE_TYPE_MAP = {
    OPTION: "OPT",
    FUTURE: "FUT"
}

#TODO change name to INSTRU_TYPE_MAP
OPT_TYPE_MAP = {
    "IDX": INDEX,
    "STK": STOCK,
}

REV_INSTRU_TYPE_MAP = {
    INDEX: "IDX",
    STOCK: "STK"
}

REV_IDX_MAP = {
    FUTIDX: "FUTIDX", 
    FUTSTK: "FUTSTK", 
    FUTIVX: "FUTIVX", 
    OPTIDX: "OPTIDX", 
    OPTSTK: "OPTSTK",
}

OPT_TYPE_MAP = {"XX": XX, "CE": CE, "PE": PE}

DATATABLE_PREFIX = "D_"
INDEX_TABLE_PREFIX = "I_"
METADATA_TABLE_PREFIX = "M_"
PERIPHERAL_TABLE_PREFIX = "P_"

DAY_ZERO = '01-01-2000'
NUM_SERIES = 3

if sys.platform == 'win32':
    # TODO: Change this to app data
    HOMEDIR = "C:\\AppHome"
    NULLLOG = "NUL"
else:
    USER_HOME = os.path.expanduser('~')
    HOMEDIR = os.path.join(USER_HOME, "AppHome")
    NULLLOG = "/dev/null"

DEBUGLOG = os.path.join(HOMEDIR, "debug.log")
REQUESTLOG = os.path.join(HOMEDIR, "request.log")
PROFILELOG = os.path.join(HOMEDIR, "profile.log")

DBPATH = os.path.join(HOMEDIR, "Derivatives.db")

CSVSTORE = os.path.join(HOMEDIR, "bhavcopies")

# TODO: remove PLOT_PATH
PLOT_PATH = "./static/reports/"

# May need to remove INDIAVIX later
IGNORE_SCRIPS = ['DJIA', 'S&P500', 'FTSE100', 'INDIAVIX']

