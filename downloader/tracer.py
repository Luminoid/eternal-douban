import requests


class Tracer:
    def __init__(self, user_id):
        self.user_id = user_id
        self.session = requests.Session()
