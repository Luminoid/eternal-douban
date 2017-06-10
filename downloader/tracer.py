import requests


class Tracer:
    def __init__(self, user_id):
        self.user_id = user_id
        self.session = requests.Session()
        self.book_collection = set()      # {}
        self.movie_collection = set()     # {(), ...}
        self.tv_collection = set()        # {(), ...}
        self.music_collection = set()
        self.author_collection = set()
        self.celebrity_collection = set()
        self.singer_collection = set()

    def reconnect(self):
        self.session = requests.Session()
