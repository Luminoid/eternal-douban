from downloader.tracer import Tracer
from downloader.getBookCollection import get_book_collection
from downloader.getBookCollection import get_book_info


def get_base_url(col_type, user_id):
    return 'https://%s.douban.com/people/%s/' % (col_type, user_id)


def download(user_id):
    m_tracer = Tracer(user_id)
    user_book_url = get_base_url('book', user_id)
    collection_book_list = get_book_collection(m_tracer.session, user_book_url)
    collection_book_data = get_book_info(m_tracer.session, collection_book_list, user_book_url)
    for item in collection_book_data:
        print(item.__dict__)
