import os
import sqlite3


def initialize_collection():
    if not os.path.exists('../db/collection.db'):
        conn = sqlite3.connect('../db/collection.db')
        curs = conn.cursor()
        curs.execute('''
            CREATE TABLE BOOK (
                id             INT    PRIMARY KEY,
                /* Book info */
                isbn13         INT,
                title          TEXT,
                origin_title   TEXT,
                subtitle       TEXT,
                url            TEXT,           -- douban link
                author         TEXT,           -- array
                translator     TEXT,           -- array
                publisher      TEXT,
                pubdate        TEXT,           -- date
                pages          INT,
                price          TEXT,
                binding        TEXT,
                /* Detail info */
                image          TEXT,           -- path
                summary        TEXT,
                catalog        TEXT,
                author_intro   TEXT,
                /* Rating info */
                average_rating INT,
                ratings_count  INT
            )
            ''')
        curs.execute('''
            CREATE TABLE AUTHOR (
                id             INT    PRIMARY KEY,
                /* Author info */
                name           TEXT,
                name_en        TEXT,
                url            TEXT,           -- douban link
                gender         TEXT,
                birthday       TEXT,
                country        TEXT,
                aka            TEXT,
                /* Detail info */
                avatars        TEXT,           -- path
                summary        TEXT,
                works          TEXT            -- array
            );
            ''')
        curs.execute('''
            CREATE TABLE MOVIE (
                id             INT    PRIMARY KEY,
                /* Movie info */
                imdb           INT,
                title          TEXT,
                origin_title   TEXT,
                aka            TEXT,           -- array
                url            TEXT,           -- douban link
                directors      TEXT,           -- array
                writers        TEXT,           -- array
                casts          TEXT,           -- array
                pubdate        TEXT,           -- date
                genres         TEXT,           -- array
                durations      TEXT,           -- array
                countries      TEXT,           -- array
                languages      TEXT,           -- array
                /* TV info */
                seasons_count  INT,
                current_season INT,
                episodes_count INT,
                /* Detail info */
                image          TEXT,           -- path
                summary        TEXT,
                photos         TEXT,           -- array
                /* Rating info */
                average_rating INT,
                ratings_count  INT
            );
            ''')
        curs.execute('''
            CREATE TABLE CELEBRITY (
                id             INT    PRIMARY KEY,
                /* Celebrity info */
                imdb           TEXT,
                name           TEXT,
                name_en        TEXT,
                url            TEXT,           -- douban link
                gender         TEXT,
                birthday       TEXT,
                born_place     TEXT,
                professions    TEXT,
                /* Detail info */
                avatars        TEXT,           -- path
                summary        TEXT,
                photos         TEXT,           -- array
                works          TEXT            -- array
            );
            ''')
        curs.execute('''
            CREATE TABLE MUSIC (
                id             INT    PRIMARY KEY,
                /* Music info */
                title          TEXT,
                aka            TEXT,
                url            TEXT,           -- douban link
                singer         TEXT,           -- array
                publisher      TEXT,           -- array
                pubdate        TEXT,           -- date
                genres         TEXT,           -- array
                durations      TEXT,           -- array
                media          TEXT,           -- array
                version        TEXT,           -- array
                /* Detail info */
                image          TEXT,           -- path
                summary        TEXT,
                tracks         TEXT,           -- array
                /* Rating info */
                average_rating INT,
                ratings_count  INT
            );
            ''')
        curs.execute('''
            CREATE TABLE SINGER (
                id             INT    PRIMARY KEY,
                /* Singer info */
                name           TEXT,
                name_en        TEXT,
                url            TEXT,           -- douban link
                birthday       TEXT,
                country        TEXT,
                labels         TEXT,
                members        TEXT,
                genres         TEXT,
                /* Detail info */
                avatars        TEXT,           -- path
                summary        TEXT,
                photos         TEXT,           -- array
                works          TEXT            -- array
            )
            ''')
        conn.commit()
        conn.close()


def initialize_user(user_id):
    path = '../db/user_%s.db' % user_id
    if not os.path.exists(path):
        conn = sqlite3.connect(path)
        curs = conn.cursor()
        curs.execute('''
            CREATE TABLE MY_BOOK (
                book_id        INT    PRIMARY KEY,
                /* User info */
                status         TEXT,           -- collect, do, wish
                updated        TEXT,           -- date
                rating         INT,            -- 1 ~ 5
                tags           TEXT,           -- tag list
                comment        TEXT            -- comment text
            )
            ''')
        curs.execute('''
            CREATE TABLE MY_MOVIE (
                movie_id       INT    PRIMARY KEY,
                /* User info */
                status         TEXT,           -- collect, do, wish
                updated        TEXT,           -- date
                rating         INT,            -- 1 ~ 5
                tags           TEXT,           -- tag list
                comment        TEXT            -- comment text
            );
            ''')
        curs.execute('''
            CREATE TABLE MY_TV (
                tv_id             INT    PRIMARY KEY,
                /* User info */
                status         TEXT,           -- collect, do, wish
                updated        TEXT,           -- date
                rating         INT,            -- 1 ~ 5
                tags           TEXT,           -- tag list
                comment        TEXT            -- comment text
            );
            ''')
        curs.execute('''
            CREATE TABLE MY_MUSIC (
                music_id       INT    PRIMARY KEY,
                /* User info */
                status         TEXT,           -- collect, do, wish
                updated        TEXT,           -- date
                rating         INT,            -- 1 ~ 5
                tags           TEXT,           -- tag list
                comment        TEXT            -- comment text
            );
            ''')
        conn.commit()
        conn.close()
