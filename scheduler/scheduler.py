from util.logger import initialize_logger
from util.logger import get_logger
from db_handler.initializer import initialize_path
from db_handler.initializer import initialize_collection
from db_handler.initializer import initialize_user
from downloader.downloader import download


def initialize():
    initialize_logger()
    initialize_path()
    initialize_collection()


def scrape(user_id):
    logger = get_logger()
    logger.info('[Start]    Start Scraping')
    initialize_user(user_id)
    download(user_id)


if __name__ == '__main__':
    initialize()
    scrape('162041699')
