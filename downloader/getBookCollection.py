import math
import re
import sys
import traceback
from downloader.getPage import get_bs
from page_processor.parseBookPage import parse_my_book
from page_processor.parseBookPage import parse_book_page
from db_handler.insertData import insert_collection
from db_handler.insertData import insert_entry
from db_handler.queryData import get_collection_list
from util.util import get_user_url
from util.logger import get_logger
from util.settings import *


def get_book_collection(tracer):
    user_url = get_user_url('book', tracer.user_id)
    logger = get_logger()
    logger.info('[Start]    Scraping book collection')
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
                    items = bs.find(id="content").find("ul", {"class": "interest-list"}).findAll("li")
                    for item in items:
                        my_book = parse_my_book(item, status)
                        insert_collection(tracer.user_id, my_book, DATA_MY_BOOK)
                        tracer.book_collection.add(my_book[0])
    get_book_page(tracer, user_url)


def get_book_page(tracer, user_url):
    user_book_set = tracer.book_collection
    db_book_lst = get_collection_list(DATA_BOOK)
    db_book_set = {item[0] for item in db_book_lst}
    scrape_set = user_book_set - db_book_set
    logger = get_logger()
    # scraping
    failed_page = set()
    for book_id in scrape_set:
        if not get_book_info(tracer, book_id, user_url):
            failed_page.add(book_id)
    # rescraping
    if len(failed_page) != 0:
        logger.warning('[Rescrape] Rescraping book collection')
        for book_id in failed_page:
            get_book_info(tracer, book_id, user_url)


def get_book_info(tracer, book_id, user_url):
    logger = get_logger()
    url = 'https://book.douban.com/subject/%s/' % book_id
    bs = get_bs(tracer.session, url, user_url)
    if bs is not None:
        try:
            book = parse_book_page(bs, url)
            insert_entry(book, DATA_BOOK)
            logger.info('[Get]      url: %s' % url)
            return True
        except Exception as e:
            logger.warning('[Error]    url: %s error: %s' % (url, e))
            traceback.print_exc()
            sys.exit(0)
    else:
        return False
