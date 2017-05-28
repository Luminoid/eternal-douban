import re
import math
import sys
import traceback
from log.logger import get_logger
from downloader.getPage import get_bs
from page_processor.parseBookPage import parse_book_page
from page_processor.parseBookPage import generate_book


def get_book_collection(tracer, user_url):
    logger = get_logger()
    logger.info('[Start]  Scraping book collection')
    urls = [user_url + "/collect",
            user_url + "/do",
            user_url + "/wish"]

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
                    items = bs.find(id="content").find("ul", {"class": "interest-list"}).findAll("li")
                    for item in items:
                        book = generate_book(item, status)
                        tracer.collection.append(book)
    get_book_page(tracer, user_url)


def get_book_page(tracer, user_url):
    logger = get_logger()
    # scraping
    for book in tracer.book_collection:
        get_book_info(tracer, book, user_url)
    # rescraping
    for book in tracer.book_collection:
        if book.isbn13 is None and book.title is None:
            logger.warning('[Get]    Rescrape %s' % book.url)
            get_book_info(tracer, book, user_url)


def get_book_info(tracer, book, user_url):
    logger = get_logger()
    url = book.url
    bs = get_bs(tracer.session, url, user_url)
    if bs is not None:
        try:
            parse_book_page(bs, book)
            logger.info('[Get]    %s' % url)
        except Exception as e:
            logger.warning('[Error]  url: %s error: %s' % (url, e))
            traceback.print_exc()
            sys.exit(0)
