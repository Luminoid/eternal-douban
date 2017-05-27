from log.logger import initialize_logger
from log.logger import get_logger
from db_handler.initializer import initialize_db
from downloader.downloader import download


def initialize():
    initialize_logger()
    initialize_db()


def scrape(user_id):
    logger = get_logger()
    logger.info('[Start]\t Start Scraping')
    download(user_id)


if __name__ == '__main__':
    initialize()
    scrape('143956596')
