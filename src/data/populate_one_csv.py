"""
A module for populating the data:
Steps:
    1. Get list of tables from DB. Store the list in-memory.
    2. Take CSV for reading.
    3. For each entry in CSV,
        3.1. Check if table for that entry exists,
             If not, create the table. 
             Add the table name in the in memory table list.
        3.2. Store the entry in the table.

Should application take multiple CSV's as input?
    
"""

import os
from zipfile import ZipFile

from db import dbops_sqlite3
from data import read_one_csv

from utils import get_tablename
from utils import get_date
from utils import tablename_to_symbol
from utils import tablename_to_idx

from const import *

CDBOps = dbops_sqlite3.SQLite_DBOps

class Populator(object):
    __doc__ = """
                csvs: list of full paths of csv files
                dbname: full path of the db file (for sqlite)
                
                TODO: need to improve for mysql where username and passwd is needed
              """

    def __init__(self, csvs, dbname):
        self.csvs = csvs
        self.dbname = dbname
        self.init_dbops()
        self.get_tables()
        self.scrips = []

    def init_dbops(self):
        self.dbops = CDBOps(self.dbname)

    def get_tables(self):
        spec = {'cols': ['name'], 'clauses': [[('type', '=', 'table')]]}
        tables = self.dbops.select_meta(spec)
        self.tablenames = [x[0] for x in tables]
        self.scrip_info = True if 'M_SCRIP_INFO' in self.tablenames else False 
        dlog.info('Exising table list = ' + str(self.tablenames))

    def create_table(self, tablename):
        # Create scrip info table if needed.
        if not self.scrip_info:
            spec = {
                'primary_key': [('symbol', 'string-32')],
                'non_key': [('instru_type', 'int')],
                'tablename': 'M_SCRIP_INFO',
            }
            self.dbops.create(spec)
            self.scrip_info = True 
            dlog.info("M_SCRIP_INFO table created")

        # Add entry for this table in scrip info table
        instru_type = 0
        itype_str = tablename_to_idx(tablename)
        if itype_str.endswith('IDX'):
            instru_type = INDEX
        elif itype_str.endswith('STK'):
            instru_type = STOCK

        symbol = tablename_to_symbol(tablename)
        if (symbol, instru_type) not in self.scrips:
            spec = {
                'tablename': 'M_SCRIP_INFO',
                'values': [ ('symbol', symbol), 
                            ('instru_type', instru_type)]
            }
            self.dbops.put(spec)
            self.scrips.append((symbol, instru_type))
            dlog.info("Entry created for " + tablename + " in M_SCRIP_INFO")

        # Create table for this scrip
        spec = {
            'primary_key': [ ('exp_dt', 'date'), ('timestamp', 'date'),
                             ('strike_pr', 'double'), ('opt_type', 'int') ],
            'non_key': [ ('contracts', 'long'), ('open_int', 'long'),
                         ('settle_pr', 'double') ],
            'tablename': tablename,
        }
        self.dbops.create(spec)
        dlog.info("Table created for " + tablename)

    def get_put_spec(self, e, tablename):
        open_int, strike_pr = e[12], e[3]
        contracts, opt_type = e[10], e[4]
        _exp_dt, _timestamp = e[2], e[14]
        settle_pr = e[9]
        # print "entries = ", open_int, strike_pr, contracts, opt_type, _exp_dt, _timestamp
        exp_dt = get_date(_exp_dt)
        timestamp = get_date(_timestamp)
        spec = {
            'tablename': tablename,
            'values': [ ('open_int', open_int), ('exp_dt', exp_dt), 
                        ('timestamp', timestamp), ('strike_pr', strike_pr), 
                        ('opt_type',  opt_type), ('contracts', contracts),
                        ('settle_pr', settle_pr)]
        }
        return spec

    def start(self):
        for csv in self.csvs:
            reader = read_one_csv.CSVReader(csv)
            for e in reader.walk():
                # print 'e = ', e
                idx, symbol = e[0], e[1]
                tablename = get_tablename(idx, symbol)
                if tablename not in self.tablenames:
                    self.create_table(tablename)
                    self.tablenames.append(tablename)
                spec = self.get_put_spec(e, tablename)
                self.dbops.put(spec)

def unzip_csv(path, f):
    with ZipFile(os.path.join(path,f), mode='r') as zf:
        name = zf.namelist()[0]
        zf.extract(name, path=path)
        return name

def walk_path(path):
    csvs = []
    for path, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('csv.zip'):
                name = unzip_csv(path, f)
                csvs.append(os.path.join(path, name))
    return csvs


if __name__ == '__main__':
    csvs = [
             '/Users/amitkulkarni/bhavcopies/fo21DEC2015bhav.csv',
             '/Users/amitkulkarni/bhavcopies/fo22DEC2015bhav.csv',
             '/Users/amitkulkarni/bhavcopies/fo23DEC2015bhav.csv',
             '/Users/amitkulkarni/bhavcopies/fo24DEC2015bhav.csv',
           ]
    
    path = '/Users/amitkulkarni/Downloaded_Bhavcopies/2015/DEC2015'
    csvs = walk_path(path)
    print "*****************", csvs

    dbname = '/Users/amitkulkarni/temp_Derivatives/populate_test.db'
    
    populator = Populator(csvs, dbname)
    populator.start()

