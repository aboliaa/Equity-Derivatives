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

DBNAME = "/Users/amitkulkarni/temp_Derivatives/populate_test.db"
PLOT_PATH = "/Users/amitkulkarni/Derivatives/src/static/"

DATATABLE_PREFIX = "D_"

DAY_ZERO = '01-01-1980'

