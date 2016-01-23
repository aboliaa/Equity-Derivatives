import sqlite3
import time

from db import dbops
from utils import from_pytime_to_str, from_str_to_pytime
from const import *

class SQLite_DBOps(dbops.DBOps):
    def __init__(self, dbname):
        super(SQLite_DBOps, self).__init__()
        self.dbname = dbname
        self.schemas = {}
        self.init_db_conn()
 
    def init_db_conn(self):
        self.conn = sqlite3.connect(self.dbname, check_same_thread=False)
        rc = self.conn.execute("PRAGMA journal_mode=WAL;")
        self.cur = self.conn.cursor()
    
    def _process_put_vals(self, vals):
        _vals = []
        for c, v in vals:
            if type(v) == time.struct_time:
                tval = from_pytime_to_str(v)
                _vals.append((c, "\"" + tval + "\""))
            elif type(v) in [str, unicode]:
                val = "\"" + v + "\""
                _vals.append((c, val))
            elif type(v) in [int, long, float]:
                val = str(v)
                _vals.append((c, val))
            else:
                raise NotImplementedError
        return _vals

    def _process_create_cols(self, cols):
        _cols = []
        for k, v in cols:
            if v.find('string') <> -1:
                sz = v.split('-')[1]
                t = 'varchar(%s)' % sz
                _cols.append((k, t))
            else:
                _cols.append((k, v))
        return _cols

    def _process_select_clauses(self, _clauses):
        if not _clauses:
            return []

        clauses = []
        for clause in _clauses:
            cl = []
            for k, c, v in clause:
                if type(v) == time.struct_time: 
                    cl.append((k, c,  "\"" + from_pytime_to_str(v) + "\""))
                elif type(v) in [str, unicode]:
                    cl.append((k, c,  "\"" + v + "\""))
                elif type(v) in [int, long, float]:
                    cl.append((k, c, str(v)))
                else:
                    raise NotImplementedError
            clauses.append(cl)
        return clauses 

    def _process_select_output(self, l):
        ll = []
        for e in l:
            lle = []
            for i in range(len(e)):
                v = e[i]
                new_v = v
                if type(v) == str and len(v.split("-")) == 3:
                    t = from_str_to_pytime()
                    new_v = t if t else v
                lle.append(v)
            ll.append(tuple(lle))
        return ll
        

    def create(self, spec):
        super(SQLite_DBOps, self).create(spec)
        schema = self.schema
        # dlog.info('schema = %s' % (schema,))
        tablename = schema['tablename']
        cols = schema['cols']
        cols = self._process_create_cols(cols)
        _pk = ",".join([x[0] for x in schema['primary_key']])
        l = [" %s %s NOT NULL" % (k, v) for k, v in cols]
        _cols = ",".join(l)
        _cols += ", PRIMARY KEY (%s)" % (_pk,)
        query = """CREATE TABLE "%s" (%s)""" % (tablename, _cols)
        # dlog.info('sqlite create query = %s' % (query,))
        rc = self.cur.execute(query)
        self.conn.commit()

    def put(self, spec):
        super(SQLite_DBOps, self).put(spec)
        query = self.query
        # dlog.info('query = %s' % (query,))
        tablename = query['tablename']
        values = self._process_put_vals(query['values'])
        _cols = [x[0] for x in values]
        # dlog.info('_cols = ' % (_cols,))
        _vals = [x[1] for x in values]
        # dlog.info('_vals = %s' % (_vals,))
        cols = ", ".join([x[0] for x in values])
        vals = ", ".join([x[1] for x in values])
        _query = """INSERT INTO "%s" (%s) VALUES (%s)""" % (tablename, cols, vals)
        # dlog.info('sqlite put query = %s' % (_query,))
        rc = self.cur.execute(_query)
        self.conn.commit()

    def select(self, _spec):
        super(SQLite_DBOps, self).select(_spec)
        spec = self.query
        # dlog.debug('spec for select = %s' % (spec,))
        clauses = self._process_select_clauses(spec.get('clauses'))
        _cols = ''
        if spec.get('cols'):
            _cols = "*" if spec['cols'] == "*" else ", ".join(spec['cols'])
        agg = ''
        if spec.get('agg'):
            op = spec['agg'][0]
            col = spec['agg'][1]
            agg = op + "(" + col  + ")"
        if _cols and agg:
            cols = ", ".join([_cols, agg])
        else:
            cols = _cols if _cols else agg

        tablename = spec['tablename']
        query = """ SELECT %s FROM "%s" """ % (cols, tablename)
        if spec.get('clauses'):
            cls = []
            for _clause in clauses:
                cl = " AND ".join(["(%s%s%s)" % (x[0], x[1], x[2]) for x in _clause])
                cls. append(cl)
            clause = " OR ".join(cls)
            query += " WHERE " + clause
        # dlog.info('sqlite select query is %s' % (query,))
        rc = self.cur.execute(query)
        l = self.cur.fetchall()
        # TODO: ideally, this method should be an iterator
        ll = self._process_select_output(l)
        return ll

    def select_meta(self, spec):
        spec['tablename'] = 'sqlite_master'
        return self.select(spec)
        
    def __del__(self):
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
    dbname = '/Users/amitkulkarni/temp_Derivatives/temp_db.db'
    dbobj = SQLite_DBOps(dbname)
    spec = {
                'primary_key': [('exp_dt', 'date'), ('timestamp', 'date'), 
                                ('strike_pr', 'long'), ('opt_type', 'int')],
                'non_key': [ ('contracts', 'long'), ('open_int', 'long')],
                'tablename': 'NIFTY_FUTIDX',
           }
    # dbobj.create(spec)

    t = time.gmtime()
    spec = {
                'tablename': 'NIFTY_FUTIDX',
                'values': [ 
                            ('open_int', 2000), ('exp_dt', t), ('timestamp', t),
                            ('strike_pr', 0), ('opt_type', XX), ('contracts', 1000), 
                          ]
           }
    # dbobj.put(spec)

    spec = { 
                'cols': ['name'],
                'clauses': [ [('type', '=', 'table')] ],
           }
    dbobj.select_meta(spec)

