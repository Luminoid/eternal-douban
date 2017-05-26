import bs4
import re
from urllib.request import urlretrieve
from model.book import Book


def try_except(success):
    try:
        return success()
    except AttributeError:
        return None
    except IndexError:
        # TODO: Mismatching scraping can be missed here
        return None


def get_span_val(tag, name):
    try:
        ret = tag.find("span", text=re.compile(name)).next_sibling.strip()
    except AttributeError:
        ret = None
    return ret


def get_list_val(tag):
    list_val = ''
    ptr = tag.next_sibling
    while ptr is not None and not (hasattr(ptr, 'name') and ptr.name == 'br'):
        if type(ptr) is bs4.element.NavigableString:
            list_val += ptr.strip()
        elif hasattr(ptr, 'name') and ptr.name == 'a':
            list_val += ptr.get_text().strip()
        ptr = ptr.next_sibling

    list_val = re.sub(' *\n *', ' ', list_val)
    list_val = re.sub('/', ' / ', list_val)
    if list_val[0] == ':':
        list_val = list_val[1:]
    return list_val


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
    except TypeError:      # 'NoneType' object is not subscriptable
        book.rating = None
    # tags
    try:
        tag_list = note.div.find("span", {"class": "tags"}).get_text().split()[1:]
        book.tags = ' '.join(tag_list)
    except AttributeError:
        book.tags = None
    # comment
    try:
        if note.p.get_text() != '\n':
            book.comment = note.p.get_text()
        else:
            book.comment = None
    except AttributeError:
        book.comment = None
    return book


def parse_book_page(bs, book):
    info = bs.find(id="info")
    author = try_except(lambda: info.find("span", text=re.compile("作者")))
    translator = try_except(lambda: info.find("span", text=re.compile("译者")))

    related_info = bs.select("#content .related_info")[0]
    summary = try_except(lambda: related_info.find("span", text=re.compile("内容简介"))
                         .parent.next_sibling.next_sibling.find("div", {"class": "intro"}).findAll("p"))
    author_intro = try_except(lambda: related_info.find("span", text=re.compile("作者简介"))
                              .parent.next_sibling.next_sibling.find("div", {"class": "intro"}).findAll("p"))
    raw_catalog = try_except(lambda: related_info.find("span", text=re.compile("目录")).parent.
                             next_sibling.next_sibling.next_sibling.next_sibling)
    if raw_catalog is not None:
        catalog = [elem.strip() for elem in raw_catalog.contents if type(elem) is bs4.element.NavigableString]
        if catalog[-1] == ')' and catalog[-2] == '· · · · · ·     (':
            catalog = catalog[:-2]
    else:
        catalog = None

    img_loc = bs.find(id="mainpic").a["href"]
    if img_loc.find('update_image') < 0:
        img_id = img_loc.split("/")[-1]
        urlretrieve(img_loc, "../db/img/book/%s" % img_id)
    else:
        img_id = None

    book.isbn13 = get_span_val(info, "ISBN")
    book.title = bs.find(id="wrapper").h1.span.get_text()
    book.origin_title = get_span_val(info, "原作名")
    book.subtitle = get_span_val(info, "副标题")
    book.author = get_list_val(author) if author is not None else None
    book.translator = get_list_val(translator) if translator is not None else None
    book.publisher = get_span_val(info, "出版社")
    book.pubdate = get_span_val(info, "出版年")
    book.pages = get_span_val(info, "页数")
    book.price = get_span_val(info, "定价")
    book.binding = get_span_val(info, "装帧")
    book.image = "img/book/%s" % img_id if img_id is not None else None
    book.summary = '\n'.join(p.get_text() for p in list(summary)) if summary is not None else None
    book.catalog = '\n'.join(catalog) if catalog is not None else None
    book.author_intro = '\n'.join(p.get_text() for p in list(author_intro)) \
        if author_intro is not None else None
    book.average_rating = try_except(lambda: bs.select("#interest_sectl strong[property=\"v:average\"]")[0].get_text())
    book.ratings_count = try_except(lambda: bs.select("#interest_sectl span[property=\"v:votes\"]")[0].get_text())
