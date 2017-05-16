import re
import math
import logging
from downloader.getPage import get_bs
from downloader.tracer import Tracer
from model.book import Book


logging.basicConfig(level=logging.INFO, filename='../log/collection.log')
logging.info('Book collection:')


def generate_book(item, status):
    book = Book()
    print(item)
    info = item.find("div", {"class": "info"})
    note = info.find("div", {"class": "short-note"})
    # url
    book.url = info.h2.a["href"]
    # status
    book.status = status
    # updated
    book.updated = note.div.find("span", {"class": "date"}).split()[0]
    # rating
    try:
        rating_str = note.div.children[0]["class"]
        book.rating = re.match(r'.*(\d*).*', rating_str).group(1)
    except AttributeError as e:
        book.rating = None
    # tags
    try:
        tag_list = note.div.find("span", {"class": "tags"}).split()[1:]
        book.tags = ' '.join(tag_list)
    except AttributeError as e:
        book.tags = None
    # comment
    try:
        book.comment = note.p.get_text()
    except AttributeError as e:
        book.comment = None
    return book


def get_book_collection(tracer, user_id):
    people_url = "https://book.douban.com/people/" + str(user_id)
    urls = [people_url + "/collect",
            people_url + "/do",
            people_url + "/wish"
            ]
    collection = []

    for url in urls:
        status = url.split("/")[-1]
        bs = get_bs(tracer, url, people_url)
        if bs is not None:
            num = bs.find("div", {"id": "wrapper"}).find("div", {"class": "info"}).h1.get_text()
            num = re.match(r'.*\((.*)\)', num).group(1)
            for i in range(int(math.ceil(int(num) / 15))):
                url_para = url
                if i != 0:
                    url_para = url + "?start=%s&sort=time&rating=all&filter=all&mode=grid" % str(i * 15)
                bs = get_bs(tracer, url_para, url)
                if bs is not None:
                    items = bs.find("div", {"id": "content"}).find("ul", {"class": "interest-list"}).findAll("li")
                    for item in items:
                        print(item.contents)
                        book = generate_book(item, status)
                        collection.append(book)
    return collection


if __name__ == '__main__':
    m_tracer = Tracer()
    collections = get_book_collection(m_tracer.session, "eeop")
    for col in collections:
        print(col.__dict__)
