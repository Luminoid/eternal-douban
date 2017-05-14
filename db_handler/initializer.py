import sqlite3


def initialize_db():
    conn = sqlite3.connect('../db/collection.db')
    curs = conn.cursor()
    curs.execute('''
    CREATE TABLE book (
        id           INT    PRIMARY KEY,
        /* User info */
        status       TEXT,           -- read, reading, wish
        updated      TEXT            -- date
        rating       INT,            -- 1 ~ 5
        tags         TEXT,           -- tag list
        comment      TEXT,           -- comment text
        /* Book info */
        title        TEXT,
        origin_title TEXT,
        author       TEXT,           -- author list
        pubdate      TEXT,           -- date
        image        TEXT,           -- path
        isbn13       INT,
        pages        INT,
        price        INT,
        catalog      TEXT,
        summary      TEXT,
        link         TEXT            -- douban link
    )
    
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    initialize_db()