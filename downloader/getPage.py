import re
import time
import json
import requests
from bs4 import BeautifulSoup
from util.logger import get_logger


# TODO: proxy
def get_bs(session, url, referer):
    host = re.match(r'.*//(.*?)/.*', url).group(1)
    headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "accept-encoding": "gzip, deflate, sdch, br",
               "accept-language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
               "connection": "keep-alive",
               "host": host,
               "referer": referer,
               "upgrade-insecure-requests": "1",
               "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/58.0.3029.110 Safari/537.36"}
    # proxies = {
    #     'http': 'http://10.10.1.10:3128',
    #     'https': 'http://10.10.1.10:1080',
    # }
    time.sleep(5)
    res = session.get(url, headers=headers)
    if res.status_code == requests.codes.ok:
        bs_obj = BeautifulSoup(res.text, "html.parser")
        return bs_obj
    else:
        logger = get_logger()
        logger.error('[Error]    url: %s status_code: %s' % (url, res.status_code))
        return None


def get_json(session, url):
    headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "accept-encoding": "gzip, deflate, sdch, br",
               "accept-language": "zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4",
               "Cache-Control": "max-age=0",
               "connection": "keep-alive",
               "host": 'api.douban.com',
               "upgrade-insecure-requests": "1",
               "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/58.0.3029.110 Safari/537.36"}
    time.sleep(5)
    res = session.get(url, headers=headers)
    if res.status_code == requests.codes.ok:
        res_json = json.loads(res.text)
        return res_json
    else:
        logger = get_logger()
        logger.error('[Error]    url: %s status_code: %s' % (url, res.status_code))
        return None
