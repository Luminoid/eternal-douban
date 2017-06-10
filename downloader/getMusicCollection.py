import math
import re
import sys
import traceback
from downloader.getPage import get_bs
from page_processor.parseMusicPage import parse_my_music
from page_processor.parseMusicPage import parse_music_page
from db_handler.insertData import insert_collection
from db_handler.insertData import insert_entry
from db_handler.queryData import get_collection_list
from util.util import get_user_url
from util.logger import get_logger
from util.settings import *


def get_music_collection(tracer):
    user_url = get_user_url('music', tracer.user_id)
    logger = get_logger()
    logger.info('[Start]    Scraping music collection')
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
                        my_music = parse_my_music(item, status)
                        insert_collection(tracer.user_id, my_music, DATA_MY_MUSIC)
                        tracer.music_collection.add(my_music[0])
    get_music_page(tracer, user_url)


def get_music_page(tracer, user_url):
    user_music_set = tracer.music_collection
    db_music_set = {item[0] for item in get_collection_list(DATA_MUSIC)}
    scrape_set = user_music_set - db_music_set
    logger = get_logger()
    # scraping
    failed_page = set()
    for music_id in scrape_set:
        if not get_music_info(tracer, music_id, user_url):
            failed_page.add(music_id)
    # rescraping
    if len(failed_page) != 0:
        logger.warning('[Rescrape] Rescraping music collection')
        tracer.reconnect()
        for music_id in failed_page:
            get_music_info(tracer, music_id, user_url)


def get_music_info(tracer, music_id, user_url):
    logger = get_logger()
    url = 'https://music.douban.com/subject/%s/' % music_id
    bs = get_bs(tracer.session, url, user_url)
    if bs is not None:
        try:
            music = parse_music_page(bs, url)
            insert_entry(music, DATA_MUSIC)
            logger.info('[Get]      url: %s' % url)
            return True
        except Exception as e:
            logger.warning('[Error]    url: %s error: %s' % (url, e))
            traceback.print_exc()
            sys.exit(0)
    else:
        return False
