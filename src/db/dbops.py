import copy

from utils.log import log

"""
This module implements the methods used for creation of db.
"""

# TODO: DBOPS should raise a specific type of erros

class DBOps(object):
    def __init__(self):
        pass

    def verify_put_spec(self, spec):
        if spec.has_key('foreign_key'):
            raise NotImplementedError

        vals = spec.get('values')
        tn = spec.get('tablename')
        if not vals or not tn:
            raise Exception("Spec Verification Failed")

    def verify_create_spec(self, spec):
        if spec.has_key('foreign_key'):
            raise NotImplementedError

        pk = spec.get('primary_key')
        nk = spec.get('non_key')
        tn = spec.get('tablename')
        if not pk or not nk or not tn:
            raise Exception("Spec Verification Failed")

    def verify_select_spec(self, spec):
        # TODO: Check for the operators in clause
 
        tn = spec.get('tablename')
        cols = spec.get('cols')
        agg = spec.get('agg')
        if not tn or not (cols or agg):
            raise Exception("Spec Verification Failed") 

        if cols and agg:
            raise NotImplementedError

    def create(self, _spec):
        """
        Example spec for student marks table is
        {
            'primary_key': [('roll_no', 'int'), ('subject_id', 'int')],
            'non_key': [('marks', 'int')],
            'tablename': <tablename>,
        }
        
        No Foreign key implementation as of now.
        """

        self.verify_create_spec(_spec)
        schema = {}
        spec = copy.deepcopy(_spec)
        schema['primary_key'] = spec['primary_key']
        schema['tablename'] = spec['tablename']
        spec['non_key'].extend(spec['primary_key'])
        schema['cols'] = spec['non_key']
        self.schema = schema

    def put(self, _spec):
        """
        Example spec for student marks table is
        {
            'tablename': <tablename>,
            'values': [ ('roll_no', <roll_no>), 
                        ('subject_id', <subject_id>),
                        ('marks', <marks>) ]
        }
        
        No Foreign key implementation as of now.
        """
        self.verify_put_spec(_spec)
        self.query = _spec

    def select(self, _spec):
        """
        Example spec to get list of all students with
        sum of their marks
        {
            'tablename': <tablename>,
            'cols': ['roll_no'],
            'condition': {'sum': 'marks'},
        """
        # TODO: need to implement aggregate queries
        # Conditionals etc. in detail

        self.verify_select_spec(_spec)
        self.query = _spec

    def select_meta(self, _spec):
        """
            Need to see if needed.
        """
        # TODO: need to implement aggregate queries
        # Conditionals etc. in detail

        # self.verify_select_spec(_spec)
        # self.query = _spec
        pass


