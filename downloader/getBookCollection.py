import re
import math
import logging
from urllib.request import urlretrieve
from downloader.getPage import get_bs
from downloader.tracer import Tracer
from model.book import Book


logging.basicConfig(level=logging.INFO, filename='../log/collection.log')
logging.info('Book collection:')


def generate_book(item, status):
    book = Book()
    info = item.find("div", {"class": "info"})
    note = info.find("div", {"class": "short-note"})
    # url
    book.url = info.h2.a["href"]
    # status
    book.status = status
    # updated
    book.updated = note.div.find("span", {"class": "date"}).get_text().split()[0]
    # rating
    try:
        rating_str = note.div.find("span", {"class": re.compile("^rating")})["class"][0]
        book.rating = re.match(r'\D+(\d+).+', rating_str).group(1)
    except Exception:
        book.rating = None
    # tags
    try:
        tag_list = note.div.find("span", {"class": "tags"}).get_text().split()[1:]
        book.tags = ' '.join(tag_list)
    except AttributeError as e:
        book.tags = None
    # comment
    try:
        if note.p.get_text() != '\n':
            book.comment = note.p.get_text()
        else:
            book.comment = None
    except AttributeError as e:
        book.comment = None
    return book


def get_book_collection(session, user_id):
    user_url = "https://book.douban.com/people/" + str(user_id)
    urls = [user_url + "/collect",
            user_url + "/do",
            user_url + "/wish"
            ]
    collection = []

    for url in urls:
        status = url.split("/")[-1]
        bs = get_bs(session, url, user_url)
        if bs is not None:
            num = bs.find("div", {"id": "wrapper"}).find("div", {"class": "info"}).h1.get_text()
            num = re.match(r'.*\((.*)\)', num).group(1)
            for i in range(int(math.ceil(int(num) / 15))):
                url_para = url
                url_referer = user_url
                if i != 0:
                    url_para = url + "?start=%s&sort=time&rating=all&filter=all&mode=grid" % str(i * 15)
                    url_referer = url + "?start=%s&sort=time&rating=all&filter=all&mode=grid" % str((i - 1) * 15)
                bs = get_bs(session, url_para, url_referer)
                if bs is not None:
                    items = bs.find("div", {"id": "content"}).find("ul", {"class": "interest-list"}).findAll("li")
                    for item in items:
                        book = generate_book(item, status)
                        collection.append(book)
    return collection


def get_span_val(tag, name):
    try:
        ret = tag.find("span", text=re.compile(name)).next_sibling.strip()
    except AttributeError:
        ret = None
    return ret


def try_except(success):
    try:
        return success()
    except AttributeError:
        return None


def get_book_info(session, collection, user_url):
    for book in collection:
        url = book.url
        bs = get_bs(session, url, user_url)
        if bs is not None:
            try:
                info = bs.find(id="info")
                author = try_except(lambda: info.find("span", text=re.compile("作者")).next_sibling.next_sibling)
                translator = try_except(lambda: info.find("span", text=re.compile("译者")).next_sibling.next_sibling)

                related_info = bs.select("#content .related_info")[0]
                summary = try_except(lambda: related_info.find("span", text=re.compile("内容简介"))
                                     .parent.next_sibling.next_sibling.select(".intro")[0].findAll("p"))
                author_intro = try_except(lambda: related_info.find("span", text=re.compile("作者简介"))
                                          .parent.next_sibling.next_sibling.select(".intro")[0].findAll("p"))

                img_loc = bs.find(id="mainpic").a["href"]
                img_id = img_loc.split("/")[-1]
                urlretrieve(img_loc, "../db/img/book/%s" % img_id)

                book.isbn13 = get_span_val(info, "ISBN")
                book.title = bs.find(id="wrapper").h1.span.get_text()
                book.origin_title = get_span_val(info, "原作名")
                book.subtitle = get_span_val(info, "副标题")
                book.author = re.sub(r'\s+', '', author.get_text()) if author is not None else None
                book.translator = re.sub(r'\s+', '', translator.get_text()) if translator is not None else None
                book.publisher = get_span_val(info, "出版社")
                book.pubdate = get_span_val(info, "出版年")
                book.pages = get_span_val(info, "页数")
                book.price = get_span_val(info, "定价")
                book.binding = get_span_val(info, "装帧")
                book.image = "img/book/%s" % img_id
                book.summary = '\n'.join(p.get_text() for p in list(summary)) if summary is not None else None
                book.catalog = try_except(lambda: related_info.find("span", text=re.compile("目录"))
                                          .parent.next_sibling.next_sibling.get_text().strip())
                book.author_intro = '\n'.join(p.get_text() for p in list(author_intro)) \
                    if author_intro is not None else None
                book.average_rating = try_except(lambda: bs.select("#interest_sectl strong[property=\"v:average\"]")[0].get_text())
                book.ratings_count = try_except(lambda: bs.select("#interest_sectl span[property=\"v:votes\"]")[0].get_text())
            except Exception as e:
                logging.warning(url)
                logging.warning(e)
    return collection


if __name__ == '__main__':
    m_tracer = Tracer()
    user_url = "https://book.douban.com/people/8270989/"
    collection_list = get_book_collection(m_tracer.session, "8270989")
    collection_data = get_book_info(m_tracer.session, collection_list, user_url)
    for item in collection_data:
        print(item.__dict__)
