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
    # subtype
    type_str = try_except(lambda: bs.find(id='subject-others-interests').h2.get_text())
    # title
    titles = title.split(' / ')
    former_title = titles[0]
    latter_title = titles[1] if len(titles) > 1 else None
    # duration
    movie_duration = get_span_and_str(info, '片长')
    episode_duration = get_span_val(info, '单集片长')
    # seasons
    seasons = try_except(lambda: bs.find(id="season"))

    # image
    img_loc = bs.find(id="mainpic").a.img['src']
    img_loc = img_loc.replace('webp', 'jpg')
    if img_loc.find('movie_default_large') < 0:
        img_id = img_loc.split('/')[-1]
        if not os.path.exists('../db/img/movie/%s' % img_id):
            urlretrieve(img_loc, "../db/img/movie/%s" % img_id)
    else:
        img_id = None

    # summary
    summary = try_except(lambda: bs.find(id='link-report').find('span', {'class': 'all'}).get_text().strip())
    if summary is None:
        summary = try_except(
            lambda: bs.find(id='link-report').find('span', {'property': 'v:summary'}).get_text().strip())

    # average_rating
    rating = try_except(lambda: bs.find(id='interest_sectl').find('strong', {'property': 'v:average'}).get_text())
    if rating is not None:
        if len(rating) == 0:
            rating = None

    # info
    movie_id = url.split('/')[-2]
    subtype = 'tv' if type_str is not None and '电视剧' in type_str else 'movie'
    imdb = try_except(lambda: info.find("span", text=re.compile('IMDb')).find_next_sibling("a").get_text().strip())
    title = former_title
    origin_title = latter_title
    aka = try_except(lambda: info.find("span", text=re.compile('又名')).next_sibling.strip())
    directors = get_list_val(info, '导演')
    writers = get_list_val(info, '编剧')
    casts = get_list_val(info, '主演')
    pubdate = get_sibling_list_val(info, 'v:initialReleaseDate')
    genres = get_sibling_list_val(info, 'v:genre')
    durations = movie_duration if movie_duration is not None else episode_duration
    countries = get_span_val(info, '制片国家')
    languages = get_span_val(info, '语言')
    seasons_count = seasons.findAll('option')[-1].get_text() if seasons is not None else None
    current_season = seasons.find('option', {'selected': 'selected'}).get_text() if seasons is not None else None
    episodes_count = get_span_val(info, '集数')
    image = 'img/movie/%s' % img_id if img_id is not None else None
    summary = re.sub(r' *\n+ *', '\n', summary) if summary is not None else None
    photos = None
    average_rating = rating
    ratings_count = try_except(lambda: bs.find(id='interest_sectl').find('span', {'property': 'v:votes'}).get_text())

    return movie_id, subtype, imdb, title, origin_title, aka, url, directors, writers, casts, pubdate, genres, durations,\
        countries, languages, seasons_count, current_season, episodes_count, image, summary, photos, average_rating, \
        ratings_count
