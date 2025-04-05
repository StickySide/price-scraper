from abc import abstractmethod
import logging
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

from price_scraper import config
from price_scraper.notifications.notifier import Notifier

logger = logging.getLogger(__name__)
logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class Requester:
    """
    Responsible for requesting a website and returning raw html string.

    Attributes:
    notifier = instance of Notifier for discord messaging
    discord = Enable discord notifications. Not fully implimented.
    """

    def __init__(
        self,
        notifier: Notifier,
        discord: bool = True
    ):

        self.notifier = notifier
        self.discord = discord

    def __repr__(self):
        return (
            f"notifier={self.notifier!r}"
            f"self.discord={self.discord!r}")

    @abstractmethod
    def get_html(
            self,
            name,
            url: str,
            headers=config.HEADERS
    ) -> str:
        pass


class StandardRequester(Requester):
    """
    Responsible for requesting a website and returning raw html string.
    Uses requests library.

    Attributes:
    notifier = instance of Notifier for discord messaging
    discord = Enable discord notifications. Not fully implimented.
    """

    def __init__(
        self,
        notifier: Notifier,
        discord: bool = True
    ):
        super().__init__(
            notifier,
            discord
            )

    def __repr__(self):
        return (super().__repr__())

    def get_html(
        self,
        name,
        url: str,
        headers=config.HEADERS
    ) -> str:

        try:
            page = requests.get(url, headers)
            return page.text

        except Exception:
            logger.exception(f"[{name}] problem requesting URL {url}")
            raise Exception


class SeleniumRequester(Requester):
    """
    Responsible for requesting a website and returning raw html string.
    Uses selenium.

    Attributes:
    notifier = instance of Notifier for discord messaging
    discord = Enable discord notifications. Not fully implimented.
    """

    def __init__(
        self,
        notifier: Notifier,
        discord: bool = True
    ):
        super().__init__(
            notifier,
            discord)

    def __repr__(self):
        return (
            f"notifier={self.notifier!r}"
            f"self.discord={self.discord!r}")

    # Selenium get html...
    def get_html(
        self,
        name,
        url: str,
        headers=config.HEADERS
    ) -> str:

        """
        Uses selenium to open a firefox browser
        """

        # Logging options so selenium doesnt flood the log...
        options = Options()
        options.log.level = "fatal"  # type: ignore
        driver = webdriver.Firefox(options=options)

        # Try to get the html...
        try:
            # Open the page
            driver.get(url)

            # Scroll down the page
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

            # Wait while stuff loads
            time.sleep(config.SELENIUM_DWELL_TIME)

            # Save the html
            html = driver.page_source
            return html

        # If something fails, return an empty string
        except Exception:
            logger.exception(
                f"[{name}] error requesting URL with selenium: {url}"
                )
            return ""

        finally:
            driver.quit()


class Requesters:
    lookup = {
        "standard": StandardRequester,
        "selenium": SeleniumRequester
    }
