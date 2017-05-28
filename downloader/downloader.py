from downloader.tracer import Tracer
from downloader.getBookCollection import get_book_collection


def get_base_url(col_type, user_id):
    return 'https://%s.douban.com/people/%s/' % (col_type, user_id)


def download(user_id):
    tracer = Tracer(user_id)
    user_book_url = get_base_url('book', user_id)
    get_book_collection(tracer, user_book_url)
    for item in tracer.book_collection:
        print(item.__dict__)
