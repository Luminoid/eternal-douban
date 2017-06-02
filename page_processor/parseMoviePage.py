import bs4
import re
import os
import sys
from urllib.request import urlretrieve


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


def parse_my_movie(item, status):
    info = item.find("div", {"class": "info"})
    note = info.ul.findAll('li')[2]
    # url
    url = info.find("li", {"class": "title"}).a["href"]
    # title
    title = info.find("li", {"class": "title"}).a.em.get_text()
    # movie_id
    movie_id_lst = url.split('/')
    movie_id = movie_id_lst[-2] if len(movie_id_lst[-1]) == 0 else movie_id_lst[-1]
    movie_id = int(movie_id)
    # status
    status = status
    # updated
    updated = note.find("span", {"class": "date"}).get_text()
    # rating
    try:
        rating_str = note.find("span", {"class": re.compile("^rating")})["class"][0]
        rating = re.match(r'\D+(\d+).+', rating_str).group(1)
    except TypeError:      # 'NoneType' object is not subscriptable
        rating = None
    # tags
    try:
        tag_list = note.find("span", {"class": "tags"}).get_text().split()[1:]
        tags = ' '.join(tag_list)
    except AttributeError:
        tags = None
    # comment
    try:
        comment = info.find('span', {'class': 'comment'}).get_text().strip()
        if comment == '\n':
            comment = None
    except AttributeError:
        comment = None
    return title, movie_id, status, updated, rating, tags, comment


def parse_movie_page(bs, url, title):
    info = bs.find(id="info")
    related_info = bs.select("#content .related-info")[0]
    # title
    titles = title.split(' / ')
    former_title = titles[0]
    latter_title = titles[1] if len(titles) > 1 else None

    # # author
    # author = try_except(lambda: info.find("span", text=re.compile("作者")))
    # # translator
    # translator = try_except(lambda: info.find("span", text=re.compile("译者")))
    # # summary
    # summary = try_except(lambda: related_info.find("span", text=re.compile("内容简介"))
    #                      .parent.next_sibling.next_sibling.findAll("div", {"class": "intro"})[-1].findAll("p"))
    # # author intro
    # author_intro = try_except(lambda: related_info.find("span", text=re.compile("作者简介"))
    #                           .parent.next_sibling.next_sibling.findAll("div", {"class": "intro"})[-1].findAll("p"))
    # # catalog
    # raw_catalog = try_except(lambda: related_info.find("span", text=re.compile(
    #     "目录")).parent.next_sibling.next_sibling.next_sibling.next_sibling)
    # if raw_catalog is not None:
    #     catalog = [elem.strip() if type(elem) is bs4.element.NavigableString else elem.get_text() for elem in
    #                raw_catalog.contents]
    #     catalog = '\n'.join(catalog)
    #     catalog = re.sub(r' *\n+ *', '\n', catalog)
    #     catalog = catalog.split('\n')
    #     catalog = '\n'.join(catalog)
    #     btn_index = catalog.find('· · · · · ·')
    #     if btn_index > 0:
    #         catalog = catalog[:btn_index]
    #     if catalog[-1] == '\n':
    #         catalog = catalog[:-1]
    # else:
    #     catalog = None
    # # image
    # img_loc = bs.find(id="mainpic").a["href"]
    # if img_loc.find('update_image') < 0:
    #     img_id = img_loc.split("/")[-1]
    #     if not os.path.exists('../db/img/movie/%s' % img_id):
    #         urlretrieve(img_loc, "../db/img/movie/%s" % img_id)
    # else:
    #     img_id = None
    # # average_rating
    # rating = try_except(lambda: bs.select("#interest_sectl strong[property=\"v:average\"]")[0].get_text().strip())
    # if rating is not None:
    #     if len(rating) == 0:
    #         rating = None
    #
    # info
    movie_id = url.split('/')[-2]
    imdb = try_except(lambda: info.find("span", text=re.compile('IMDb')).find_next_sibling("a").get_text().strip())
    title = former_title
    origin_title = latter_title
    aka = info.find("span", text=re.compile('又名')).next_sibling.strip()
    print(movie_id)
    print(imdb)
    print(title)
    print(origin_title)
    print(aka)
    sys.exit(0)
    # url = url
    # directors =
    # writers
    # casts
    # pubdate
    # genres
    # durations
    # countries
    # languages

    # origin_title = get_span_val(info, "原作名")
    # subtitle = get_span_val(info, "副标题")
    # author = get_list_val(author) if author is not None else None
    # translator = get_list_val(translator) if translator is not None else None
    # publisher = get_span_val(info, "出版社")
    # pubdate = get_span_val(info, "出版年")
    # pages = get_span_val(info, "页数")
    # price = get_span_val(info, "定价")
    # binding = get_span_val(info, "装帧")
    # image = "img/movie/%s" % img_id if img_id is not None else None
    # summary = '\n'.join(p.get_text() for p in list(summary)) if summary is not None else None
    # catalog = catalog
    # author_intro = '\n'.join(p.get_text() for p in list(author_intro)) \
    #     if author_intro is not None else None
    # average_rating = rating
    # ratings_count = try_except(lambda: bs.select("#interest_sectl span[property=\"v:votes\"]")[0].get_text())

    # return movie_id, isbn13, title, origin_title, subtitle, url, author, translator, publisher, pubdate, pages, \
    #     price, binding, image, summary, catalog, author_intro, average_rating, ratings_count
