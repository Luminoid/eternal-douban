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
    return 'INSERT INTO MOVIE VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'


def insert_tv():
    return 'INSERT INTO TV VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'


def insert_celebrity():
    return 'INSERT INTO CELEBRITY VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'


def insert_music():
    return 'INSERT INTO MUSIC VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'


def insert_singer():
    return 'INSERT INTO SINGER VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'


def insert_my_book():
    return 'INSERT INTO MY_BOOK VALUES (?,?,?,?,?,?)'


def insert_my_movie():
    return 'INSERT INTO MY_MOVIE VALUES (?,?,?,?,?,?)'


def insert_my_tv():
    return 'INSERT INTO MY_TV VALUES (?,?,?,?,?,?)'


def insert_my_music():
    return 'INSERT INTO MY_MUSIC VALUES (?,?,?,?,?,?)'


insert_enum = {
    "book": insert_book,
    "author": insert_author(),
    "movie": insert_movie(),
    "tv": insert_tv(),
    "celebrity": insert_celebrity(),
    "music": insert_music(),
    "singer": insert_singer(),
    "my_book": insert_my_book,
    "my_movie": insert_my_movie(),
    "my_tv": insert_my_tv(),
    "my_music": insert_my_music()
}

