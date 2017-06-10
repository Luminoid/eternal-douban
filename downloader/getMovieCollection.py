import math
import re
import sys
import traceback
from downloader.getPage import get_bs
from page_processor.parseMoviePage import parse_my_movie
from page_processor.parseMoviePage import parse_movie_page
from db_handler.insertData import insert_collection
from db_handler.insertData import insert_entry
from db_handler.queryData import get_collection_list
from util.util import get_user_url
from util.logger import get_logger
from util.settings import *


def get_movie_collection(tracer):
    user_url = get_user_url('movie', tracer.user_id)
    logger = get_logger()
    logger.info('[Start]    Scraping movie collection')
    urls = [user_url + "collect",
            user_url + "do",
            user_url + "wish"]

    for url in urls:
        status = url.split("/")[-1]
        bs = get_bs(tracer.session, url, user_url)
        if bs is not None:
            num = bs.find(id="wrapper").find("div", {"class": "info"}).h1.get_text()
            num = re.match(r'.*\((.*)\)', num).group(1)
            for i in range(int(math.ceil(int(num) / 15))):
                url_para = url
                url_referer = user_url
                if i != 0:
                    url_para = url + "?start=%s&sort=time&rating=all&filter=all&mode=grid" % str(i * 15)
                    url_referer = url + "?start=%s&sort=time&rating=all&filter=all&mode=grid" % str((i - 1) * 15)
                bs = get_bs(tracer.session, url_para, url_referer)
                if bs is not None:
                    logger.info('[Parse]    url: %s' % url_para)
                    items = bs.find(id="content").find("div", {"class": "grid-view"}).findAll("div", {"class": "item"})
                    for item in items:
                        my_movie = parse_my_movie(item, status)
                        insert_collection(tracer.user_id, my_movie[1:], DATA_MY_MOVIE)
                        tracer.movie_collection.add((my_movie[1], my_movie[0]))
    get_movie_page(tracer, user_url)


def get_movie_page(tracer, user_url):
    db_movie_set = {item[0] for item in get_collection_list(DATA_MOVIE)}
    scrape_set = {(movie_id, title) for movie_id, title in tracer.movie_collection if movie_id not in db_movie_set}
    logger = get_logger()
    # scraping
    failed_page = set()
    for movie_id, title in scrape_set:
        if not get_movie_info(tracer, movie_id, user_url, title):
            failed_page.add((movie_id, title))
    # rescraping
    if len(failed_page) != 0:
        logger.warning('[Rescrape] Rescraping movie collection')
        tracer.reconnect()
        for movie_id, title in failed_page:
            get_movie_info(tracer, movie_id, user_url, title)


def get_movie_info(tracer, movie_id, user_url, title):
    logger = get_logger()
    url = 'https://movie.douban.com/subject/%s/' % movie_id
    bs = get_bs(tracer.session, url, user_url)
    if bs is not None:
        try:
            movie = parse_movie_page(bs, url, title)
            insert_entry(movie, DATA_MOVIE)
            logger.info('[Get]      url: %s' % url)
            return True
        except Exception as e:
            logger.warning('[Error]    url: %s error: %s' % (url, e))
            traceback.print_exc()
            sys.exit(0)
    else:
        return False
