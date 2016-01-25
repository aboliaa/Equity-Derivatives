class DBError(Exception):
    def __init__(self, errno, msg=''):
        super(DBError, self).__init__(msg)
        self.errno = errno
        self.msg = msg

EEXISTS         = 10000001
ENOTFOUND       = 10000002

