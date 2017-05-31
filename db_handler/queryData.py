import sqlite3


def query_data(data_type, data_filter):
    conn = sqlite3.connect('../db/collection.db')
    curs = conn.cursor()

    query = 'SELECT * FROM %s %s' % (data_type, data_filter)  # where, orderby
    curs.execute(query)
    return curs.fetchall()


def get_collection_list(data_type):
    conn = sqlite3.connect('../db/collection.db')
    curs = conn.cursor()

    query = 'SELECT id FROM %s' % data_type
    curs.execute(query)
    return curs.fetchall()  # [(1,), (2,), (3,), (4,)]
