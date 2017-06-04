import bs4
import re
import os
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
    """Get the next sibling string's value"""
    try:
        ret = tag.find("span", text=re.compile(name)).next_sibling.strip()
    except AttributeError:
        ret = None
    return ret


def get_next_span_val(tag, name):
    """Get the next sibling span's content"""
    try:
        ret = tag.find("span", text=re.compile(name)).next_sibling.next_sibling
        if ret.name == 'span':
            return ret.get_text().strip()
        else:
            return None
    except AttributeError:
        return None


def get_list_val(tag, name):
    """Get list value from the next sibling span's content"""
    try:
        return tag.find("span", text=re.compile(name)).find_next_sibling("span", {'class': 'attrs'}).get_text()
    except AttributeError:
        return None


def get_sibling_list_val(tag, attr):
    """Get list value from the next sibling spans' content"""
    try:
        lst = tag.findAll("span", {'property': attr})
        if len(lst) > 0:
            return ' / '.join([item.get_text().strip() for item in lst])
        else:
            return None
    except AttributeError:
        return None


def get_link_list_val(tag, attr):
    """Get list value from the parent spans' link content"""
    lst = try_except(lambda: tag.find(text=re.compile(attr)).parent.findAll('a'))
    if lst is not None:
        if len(lst) > 0:
            lst = ' / '.join([item.get_text() for item in lst])
        else:
            lst = None
    return lst


def get_span_and_str(tag, name):
    try:
        tag = tag.find("span", text=re.compile(name))
    except AttributeError:
        return None
    val = ''
    ptr = tag.next_sibling
    while ptr is not None and not (hasattr(ptr, 'name') and ptr.name == 'br'):
        if type(ptr) is bs4.element.NavigableString:
            val += ptr.strip()
        elif hasattr(ptr, 'name') and ptr.name == 'span':
            val += ptr.get_text().strip()
        ptr = ptr.next_sibling
    if len(val) > 0:
        return val
    else:
        return None


def parse_my_music(item, status):
    info = item.find("div", {"class": "info"})
    note = info.ul.findAll('li')[2]
    # url
    url = info.find("li", {"class": "title"}).a["href"]
    # music_id
    music_id_lst = url.split('/')
    music_id = music_id_lst[-2] if len(music_id_lst[-1]) == 0 else music_id_lst[-1]
    music_id = int(music_id)
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
        comment = info.ul.findAll('li')[3].get_text().strip()
        if comment == '\n':
            comment = None
    except IndexError:
        comment = None
    return music_id, status, updated, rating, tags, comment


def parse_music_page(bs, url):
    content = bs.find(id='content')
    info = bs.find(id="info")

    # image
    img_loc = bs.find(id="mainpic").a["href"]
    if img_loc.find('music-default') < 0:
        img_id = img_loc.split("/")[-1]
        if not os.path.exists('../db/img/music/%s' % img_id):
            urlretrieve(img_loc, "../db/img/music/%s" % img_id)
    else:
        img_id = None

    # summary
    summary = try_except(lambda: bs.find(id='link-report').find('span', {'class': 'all'}).get_text().strip())
    if summary is None:
        summary = try_except(
            lambda: bs.find(id='link-report').find('span', {'property': 'v:summary'}).get_text().strip())

    # tracks
    track_list = try_except(lambda: content.find('div', {'class': 'track-list'}).get_text('\n').strip())

    # average_rating
    rating = try_except(lambda: bs.find(id='interest_sectl').find('strong', {'property': 'v:average'}).get_text())
    if rating is not None:
        if len(rating) == 0:
            rating = None

    # info
    music_id = url.split('/')[-2]
    title = bs.find(id="wrapper").h1.span.get_text().strip()
    aka = get_span_val(info, '又名')
    singer = get_link_list_val(info, '表演者')
    publisher = get_link_list_val(info, '出版者')
    pubdate = get_span_val(info, '发行时间')
    genres = get_span_val(info, '流派')
    durations = None  # not provided
    media = get_span_val(info, '介质')
    version = get_span_val(info, '专辑类型')
    image = "img/music/%s" % img_id if img_id is not None else None
    summary = re.sub(r'\s*?\n+\s*', '\n', summary) if summary is not None else None
    tracks = re.sub(r'\s*?\n+\s*', '\n', track_list) if track_list is not None else None
    average_rating = rating
    ratings_count = try_except(lambda: bs.find(id='interest_sectl').find('span', {'property': 'v:votes'}).get_text())

    return music_id, title, aka, url, singer, publisher, pubdate, genres, durations, media, version, image,\
        summary, tracks, average_rating, ratings_count
