from downloader.tracer import Tracer
from downloader.getBookCollection import get_book_collection


def download(user_id):
    tracer = Tracer(user_id)
    get_book_collection(tracer)
