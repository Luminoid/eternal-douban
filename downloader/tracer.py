import requests


class Tracer:
    def __init__(self, user_id):
        self.user_id = user_id
        self.session = requests.Session()
        self.book_collection = []
        self.movie_collection = []
        self.tv_collection = []
        self.music_collection = []
        self.author_collection = []
        self.celebrity_collection = []
        self.singer_collection = []
