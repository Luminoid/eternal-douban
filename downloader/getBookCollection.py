import re
import math
import sys
import traceback
from log.logger import get_logger
from downloader.getPage import get_bs
from page_processor.parseBookPage import parse_book_page
from page_processor.parseBookPage import generate_book


def get_book_collection(session, user_url):
    logger = get_logger()
    logger.info('Scraping book collection')
    urls = [user_url + "/collect",
            user_url + "/do",
            user_url + "/wish"]
    collection = []

    for url in urls:
        status = url.split("/")[-1]
        bs = get_bs(session, url, user_url)
        if bs is not None:
            num = bs.find(id="wrapper").find("div", {"class": "info"}).h1.get_text()
            num = re.match(r'.*\((.*)\)', num).group(1)
            for i in range(int(math.ceil(int(num) / 15))):
                url_para = url
                url_referer = user_url
                if i != 0:
                    url_para = url + "?start=%s&sort=time&rating=all&filter=all&mode=grid" % str(i * 15)
                    url_referer = url + "?start=%s&sort=time&rating=all&filter=all&mode=grid" % str((i - 1) * 15)
                bs = get_bs(session, url_para, url_referer)
                if bs is not None:
                    items = bs.find(id="content").find("ul", {"class": "interest-list"}).findAll("li")
                    for item in items:
                        book = generate_book(item, status)
                        collection.append(book)
    return collection


def get_book_info(session, collection, user_url):
    for book in collection:
        url = book.url
        bs = get_bs(session, url, user_url)
        if bs is not None:
            try:
                parse_book_page(bs, book)
            except Exception as e:
                logger = get_logger()
                logger.warning('url: %s error: %s' % (url, e))
                traceback.print_exc()
                sys.exit(0)
    return collection
