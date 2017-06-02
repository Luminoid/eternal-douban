import sqlite3


def insert_entry(data, data_type):
    conn = sqlite3.connect('../db/collection.db')
    curs = conn.cursor()

    query = insert_enum[data_type]()
    curs.execute(query, data)

    conn.commit()
    conn.close()


def insert_collection(user_id, data, data_type):
    conn = sqlite3.connect('../db/user_%s.db' % user_id)
    curs = conn.cursor()

    query = insert_enum[data_type]()
    curs.execute(query, data)

    conn.commit()
    conn.close()


def insert_book():
    return 'INSERT INTO BOOK VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'


def insert_author():
    return 'INSERT INTO AUTHOR VALUES (?,?,?,?,?,?,?,?,?,?,?)'


def insert_movie():
    return 'INSERT INTO MOVIE VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'


def insert_celebrity():
    return 'INSERT INTO CELEBRITY VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'


def insert_music():
    return 'INSERT INTO MUSIC VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'


def insert_singer():
    return 'INSERT INTO SINGER VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'


def insert_my_book():
    return 'INSERT OR REPLACE INTO MY_BOOK VALUES (?,?,?,?,?,?)'


def insert_my_movie():
    return 'INSERT OR REPLACE INTO MY_MOVIE VALUES (?,?,?,?,?,?)'


def insert_my_music():
    return 'INSERT OR REPLACE INTO MY_MUSIC VALUES (?,?,?,?,?,?)'


insert_enum = {
    "BOOK": insert_book,
    "AUTHOR": insert_author,
    "MOVIE": insert_movie,
    "TV": insert_tv,
    "CELEBRITY": insert_celebrity,
    "MUSIC": insert_music,
    "SINGER": insert_singer,
    "MY_BOOK": insert_my_book,
    "MY_MOVIE": insert_my_movie,
    "MY_TV": insert_my_tv,
    "MY_MUSIC": insert_my_music
}
