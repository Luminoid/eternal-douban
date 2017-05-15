import sqlite3


def query_data(data_type, data_filter):
    conn = sqlite3.connect('../db/collection.db')
    curs = conn.cursor()

    query = 'SELECT * FROM %s %s' % (data_type, data_filter)  # where, orderby
    curs.execute(query)
    return curs.fetchall()
