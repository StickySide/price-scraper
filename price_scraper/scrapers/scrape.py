import datetime as dt
from time import sleep
import logging
from random import randint

from price_scraper.notifications.alerter import Alerter
from price_scraper.data.datamanager import DataManager
from price_scraper.notifications.notifier import Notifier
from price_scraper.scrapers.parser import Parser
from price_scraper.scrapers.requester import Requester
from price_scraper.data.item import Item

logger = logging.getLogger(__name__)


class Scrape:
    """
    Represents one scrape. Will request, parse, save, alert.

    Attributes:
    name = Name for the scrape e.g. "RTX 5080"
    notifier = NotifierLogger object for notifications and alerts
    requester = Requester object for grabbing raw html and returning a soup
    parser = Parser object for parsing bautiful soup objects
    alerter = Alerter object for sending discord alerts about prices etc..
    running = bool to show if scrape is running or not
    min_retry_time = Minimum time between retries in seconds
    max_retry_time = Maximum time between retries in seconds
    max_tries = Maximum time the requester will try to grab the html
    discord_log = Flag for discord log notifications
    items = List of Item objects that have been parsed from the html
    html = html in string format
    """

    def __init__(
        self,
        name: str,
        notifier: Notifier,
        requester: Requester,
        parser: Parser,
        alerter: Alerter,
        data_manager: DataManager,
        url: str,
        min_retry_time: int,
        max_retry_time: int,
        max_tries: int,
        discord_log: bool,
    ):

        self.name = name
        self.notifier = notifier
        self.requester = requester
        self.parser = parser
        self.alerter = alerter
        self.data_manager = data_manager
        self.url = url
        self.min_retry_time = min_retry_time
        self.max_retry_time = max_retry_time
        self.max_tries = max_tries
        self.discord_log = discord_log

        self.running = False
        self.soup = None
        self.items = []
        self.html = ""

    def __repr__(self):
        return (
            f"Scrape("
            f"name={self.name!r},"
            f"notifier={self.notifier!r},"
            f"requester={self.requester!r},"
            f"parser={self.parser!r},"
            f"alerter={self.alerter!r},"
            f"datamanager={self.data_manager!r})"
            f"self.url={self.url!r},"
            f"self.min_retry_time={self.min_retry_time!r},"
            f"self.max_retry_time={self.min_retry_time!r},"
            f"self.max_tries={self.max_tries!r},"
            f"self.discord_log={self.discord_log!r})"
        )

    def __str__(self):
        return f"[{self.name}] scrape"

    def scrape_items(self):
        """
        Orchestrates Requester getting html, Parser parsing html.
        Checks if Parser returns any items and repeats the request/parse
        if needed.

        Returns list of Item objects.
        """
        # Start logging and timing
        logger.info(f"[{self.name}] scrape started...")
        self.running = True
        self.start_time = dt.datetime.now()

        # Request page with retries
        for tries in range(self.max_tries):
            self.html = self.requester.get_html(name=self.name, url=self.url)

            # Try to parse html into items
            self.items = self.parser.get_items(name=self.name, html=self.html)

            # If items were returned, scrape was successfull
            if self.items:
                logger.info(
                    f"[{self.name}] Scrape attempt: "
                    f"{tries + 1}/{self.max_tries} successful!"
                )
                # Parse items to dict for pandas to save
                dict_list = self.items_to_dict(self.name, self.items)

                # Save data to csv
                self.data_manager.save_to_csv(self.name, dict_list)

                # Return the item list!
                return self.items

            # If list is empy, wait and retry
            elif not self.items:
                wait_time = randint(self.min_retry_time, self.max_retry_time)
                logger.info(
                    f"[{self.name}] Scrape attempt: "
                    f"{tries + 1}/{self.max_tries}, no items scraped, "
                    f"retry in {wait_time} seconds..."
                )
                sleep(wait_time)

        # Loop exits if scrape failed from max attemps
        logger.warning(
            f"[{self.name}] Scrape Failed, {self.max_tries} " f"attemps reached..."
        )

        # Stop logging and timing
        self.running = False
        self.end_time = dt.datetime.now()
        self.time_delta = self.end_time - self.start_time
        logger.info(
            f"[{self.name}] scrape finished in " f"{self.time_delta.seconds} seconds"
        )

    def items_to_dict(self, name, items: list[Item]) -> list[dict]:
        """
        Helper function to return a list of dicts.
        """
        if items:
            return [item.as_dict() for item in items]
        else:
            logger.error(f"[{name}] no items in item_list to parse to dict.")
            return []


class StandardScrape(Scrape):
    """
    Scrape Subclass specific to standard scrapes.
    Base class works so this is just a place holder.
    """

    def __init__(
        self,
        name: str,
        notifier: Notifier,
        requester: Requester,
        parser: Parser,
        alerter: Alerter,
        data_manager: DataManager,
        url: str,
        min_retry_time: int,
        max_retry_time: int,
        max_tries: int,
        discord_log: bool,
    ):
        super().__init__(
            name,
            notifier,
            requester,
            parser,
            alerter,
            data_manager,
            url,
            min_retry_time,
            max_retry_time,
            max_tries,
            discord_log,
        )

    def __repr__(self):
        return (
            f"StandardScrape("
            f"name={self.name!r},"
            f"notifier={self.notifier!r},"
            f"requester={self.requester!r},"
            f"parser={self.parser!r},"
            f"alerter={self.alerter!r},"
            f"datamanager={self.data_manager!r})"
            f"self.url={self.url!r},"
            f"self.min_retry_time={self.min_retry_time!r},"
            f"self.max_retry_time={self.min_retry_time!r},"
            f"self.max_tries={self.max_tries!r},"
            f"self.discord_log={self.discord_log!r})"
        )


class SeleniumScrape(Scrape):
    """
    Scrape Subclass specific to selenium.
    Base class works so this is just a place holder.
    """

    def __init__(
        self,
        name: str,
        notifier: Notifier,
        requester: Requester,
        parser: Parser,
        alerter: Alerter,
        data_manager: DataManager,
        url: str,
        min_retry_time: int,
        max_retry_time: int,
        max_tries: int,
        discord_log: bool,
    ):
        super().__init__(
            name,
            notifier,
            requester,
            parser,
            alerter,
            data_manager,
            url,
            min_retry_time,
            max_retry_time,
            max_tries,
            discord_log,
        )

    def __repr__(self):
        return (
            f"SeleniumScrape("
            f"name={self.name!r},"
            f"notifier={self.notifier!r},"
            f"requester={self.requester!r},"
            f"parser={self.parser!r},"
            f"alerter={self.alerter!r},"
            f"datamanager={self.data_manager!r})"
            f"self.url={self.url!r},"
            f"self.min_retry_time={self.min_retry_time!r},"
            f"self.max_retry_time={self.min_retry_time!r},"
            f"self.max_tries={self.max_tries!r},"
            f"self.discord_log={self.discord_log!r})"
        )


class Scrapers:
    """
    Scraper lookup table
    """

    lookup = {"standard": StandardScrape, "selenium": SeleniumScrape}
