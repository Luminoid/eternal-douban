import logging
import sys


logger = logging.getLogger('eternal-douban')


def initialize_logger():
    formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)-8s - %(message)s",
                                  datefmt='%Y-%m-%d %H:%M:%S')
    file_handler = logging.FileHandler("../util/collection.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


def get_logger():
    return logger


if __name__ == '__main__':
    initialize_logger()
    logger = get_logger()
    logger.debug('[Test]     Test logger.py: DEBUG message')
    logger.info('[Test]     Test logger.py: INFO message')
    logger.warning('[Test]     Test logger.py: WARNING message')
    logger.error('[Test]     Test logger.py: ERROR message')
    logger.critical('[Test]     Test logger.py: CRITICAL message')
