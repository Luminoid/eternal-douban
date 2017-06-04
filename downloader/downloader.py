from downloader.tracer import Tracer
from downloader.getBookCollection import get_book_collection
from downloader.getMovieCollection import get_movie_collection
from downloader.getMusicCollection import get_music_collection


def download(user_id):
    tracer = Tracer(user_id)
    get_book_collection(tracer)
    get_movie_collection(tracer)
    get_music_collection(tracer)
