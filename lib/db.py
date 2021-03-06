from psycopg2 import connect
from collections import namedtuple
import time
from config import DBNAME
from config import DB_USER
from config import DB_PASSWORD

def timeit(f):

    def timed(*args, **kw):

        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        print 'func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts)
        return result

    return timed

def _getConnection():
    return connect("dbname='{}' user='{}' host='localhost' password='{}'".format(
        DBNAME, DB_USER, DB_PASSWORD))

cnn = _getConnection()

def getConnection():
    global cnn
    if cnn.closed:
        print 'reconnecting to db'
        cnn = _getConnection()
    assert cnn.closed == 0
    return cnn

@timeit
def sql_execute(sql, params=None):
    cnn = getConnection()
    with cnn.cursor() as cur:
        cur.execute(sql)
        cnn.commit()

@timeit
def sql_select(sql, params=None):
    cnn = getConnection()
    def yieldRows():
        with cnn.cursor() as cur:
            cur.execute(sql, params)
            Row = namedtuple('Row', [desc[0] for desc in cur.description])
            rows = cur.fetchall()
        for row in rows:
            yield Row(*row)
    return list(yieldRows())
