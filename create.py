from schema import tr_tables
from lib.db import sql_execute

def create():
    for table in tr_tables:
	print 'creating' table
        sql_execute(table._create_sql)
        for sql in table._create_index_sqls:
            sql_execute(sql)

if __name__ == '__main__':
    create()
