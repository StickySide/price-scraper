import logging

from price_scraper import config
from price_scraper.notifications.alerter import Alerter
from price_scraper.notifications.notifier import Notifier
from price_scraper.data.datamanager import DataManager
from price_scraper.scrapers.parser import Parsers
from price_scraper.scrapers.requester import Requesters
from price_scraper.scrapers.scrape import Scrapers

logger = logging.getLogger(__name__)


class ScrapeManager:
    """
    Manages creating scrapes based on a target file.
    Initializes notifier, alerter, and datamanager.
    Uses a dictionary lookup table to assign appropriate requesters
    and parsers to a scrape.

    Attributes:
    targets = list of dicts with target information. Format:
        targets = [
        {
            "name": "Example scrape",
            "scrape_type": "standard",
            "url": "https://www.example.com/"
            "discord_log": True,
            "price threshold": 100,
            "in_stock_alert": True
        }
    """

    def __init__(self,
                 targets: list[dict]):

        self.targets = targets
        self.current_scrape = {}

        # Init Notifier
        logger.debug("Initializing notifier")
        self.notifier = Notifier(webhook_url=config.WEBHOOK_URL)

        logger.debug("Initializing alerter")
        # Init alerter
        self.alerter = Alerter(
            notifier=self.notifier,
            max_discord_string=config.MAX_DISCORD_STRING
            )

        logger.debug("Initializing data manager")
        # Init DataManager
        self.data_manager = DataManager(
            notifier=self.notifier,
            data_file=config.DATA_FILE,
            last_scrape_file=config.LAST_SCRAPE_FILE
            )

        logger.debug("ScrapeManager initialized")

    def run(self):
        """
        Begin the scrape loop. Will loop through all targets set in the target
        list. Uses dict lookup for Scrape, Parser, and Requester objects to
        build the scrape.

        When the scrape completes it adds the Item list to
        a dict current_scrape, alerts via alerter of any items below the set
        price threshold.

        Once all scrapes are complete if there is a last_scrape file, it will
        load that and alert to any stock or price changes.

        Finally,
        """
        logger.debug("ScrapeManager started")

        for target in self.targets:
            # Select the appropriate scrape class
            scrape = Scrapers.lookup[target["scrape_type"]](
                name=target["name"],
                notifier=self.notifier,
                requester=(
                    Requesters.lookup[target["scrape_type"]](notifier=self.notifier)),  # noqa
                parser=Parsers.lookup[target["scrape_type"]](self.notifier),
                alerter=self.alerter,
                data_manager=self.data_manager,
                url=target["url"],
                min_retry_time=config.MIN_TRY_TIME,
                max_retry_time=config.MAX_TRY_TIME,
                max_tries=config.MAX_TRIES,
                discord_log=target["discord_log"]
            )
            # Scrape! Add items to current scrape list
            self.current_scrape[scrape.name] = scrape.scrape_items()

            # Price stock alert
            self.alerter.price_stock_alert(
                name=target["name"],
                item_list=scrape.items,
                threshold=target["price threshold"],
                in_stock=target["in_stock_alert"]
                )

        # Load last scrape for change alerts
        self.last_scrape = self.data_manager.load_from_pickle(
            file_name=config.LAST_SCRAPE_FILE
            )

        # If there are items in the last scrape file, check and alert
        if self.last_scrape:
            self.alerter.compare_alert(
                new_scrape=self.current_scrape,
                last_scrape=self.last_scrape)

        # Save scrape as last scrape data
        self.data_manager.save_to_pickle(items=self.current_scrape,
                                         file_name=config.LAST_SCRAPE_FILE)
