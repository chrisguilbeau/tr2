from lib.db import sql_execute

from os import walk
from os.path import join
from os.path import abspath

CSV_PATH = 'csv'

def getCommands():
    for root, dirs, files in walk(CSV_PATH):
        for filename in sorted(files):
            path = abspath(join(root, filename))
            table_name = filename.split('.')[0]
            yield "copy {} from '{}' delimiter ',' csv header;".format(
                table_name,
                path,
                )

def load():
    for command in getCommands():
        sql_execute(command)

if __name__ == '__main__':
    load()
