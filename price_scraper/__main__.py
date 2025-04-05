import logging
from logging.handlers import RotatingFileHandler

from price_scraper import config
from price_scraper import ScrapeManager
from price_scraper.targets import targets


def config_logger():
    logger = logging.getLogger()
    logger.setLevel(config.LOG_LEVEL)

    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.DEBUG)

    rfh = RotatingFileHandler(
        filename=config.LOG_FILE,
        maxBytes=config.MAX_LOG_SIZE,
        backupCount=config.MAX_BACKUP_LOGS,
        )

    formatter = logging.Formatter(
        fmt=config.LOG_FORMAT,
        datefmt=config.LOG_DATE_FORMAT
        )

    rfh.setFormatter(formatter)
    console_logger.setFormatter(formatter)

    # logger.addHandler(console_logger)
    logger.addHandler(rfh)

    return logger


def main():
    config_logger()

    scrape_manager = ScrapeManager(targets)
    scrape_manager.run()


if __name__ == '__main__':
    main()
