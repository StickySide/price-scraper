from abc import abstractmethod
import datetime as dt
import logging

from bs4 import BeautifulSoup

from price_scraper.data.item import Item
from price_scraper.notifications.notifier import Notifier

logger = logging.getLogger(__name__)


class Parser:
    """
    Parses HTML into Item Objects

    Attributes:
    notifier = Notifier object
    soup = BeautifulSoup object
    item_list = list of Item class objects
    """

    def __init__(self, notifier: Notifier):
        self.notifier = notifier
        self.soup = None
        self.item_list = []

    def __repr__(self):
        return f"Parser(notifier={Notifier!r})"

    @abstractmethod
    def get_items(self, name: str, html: str) -> list[Item]:
        pass


class StandardParser(Parser):
    """
    Parses HTML into Item Objects

    Attributes:
    notifier = Notifier object
    soup = BeautifulSoup object
    item_list = list of Item class objects
    """

    def __init__(self, notifier: Notifier):
        super().__init__(notifier)

    def __repr__(self):
        return f"StandardParser(notifier={Notifier!r})"

    def get_items(self, name: str, html: str) -> list[Item]:
        """
        Takes raw html, parses with beautiful soup, and attempts to extract
        product information to build item objects. Returns a list of Items.
        """

        def _get_title(item):
            title = item.find("a", class_="item-title").text
            return title

        def _get_price(item):
            block = item.find("li", class_="price-current")
            price = int(block.find("strong").text.replace(",", ""))
            return price

        def _get_stock(item):
            return False if item.find("p", class_="item-promo") else True

        def _get_link(item):
            return item.find("a").get("href")

        current_time = dt.datetime.now().isoformat(timespec="seconds")

        # Try to parse item_cards from soup
        try:
            soup = BeautifulSoup(html, "html.parser")
            item_cards = [item for item in soup.find_all("div", class_="item-cell")]
        except ValueError:
            logger.exception("No item cards were found")
            return []

        for item in item_cards:
            try:
                # Scrape and format
                title = _get_title(item)
                price = _get_price(item)
                in_stock = _get_stock(item)
                link = _get_link(item)

                # Add object to item list
                self.item_list.append(
                    Item(
                        name, current_time, title, price, in_stock, link
                    )  # type: ignore
                )
            except Exception:
                logger.exception(f"Error parsing [{name}]")

        logger.info(
            f"[{name}] Parsing complete: " f"{len(self.item_list)} items parsed"
        )

        return self.item_list


class SeleniumParser(Parser):
    """
    Parses HTML into Item Objects

    Attributes:
    notifier = Notifier object
    soup = BeautifulSoup object
    item_list = list of Item class objects
    """

    def __init__(self, notifier: Notifier):
        super().__init__(notifier)

    def __repr__(self):
        return f"SeleniumParser(notifier={Notifier!r})"

    def get_items(
        self,
        name: str,
        html: str,
    ) -> list[Item]:

        current_time = dt.datetime.now().isoformat(timespec="seconds")

        def _get_title(item) -> str:
            return item.find("h4", class_="sku-title").text

        def _get_price(item) -> int:
            price_block = item.find("div", attrs={"data-testid": "customer-price"})
            price_unfiltered = price_block.find(
                "span", attrs={"aria-hidden": "true"}
            ).text
            price = round(
                float(
                    "".join(
                        letter
                        for letter in price_unfiltered
                        if letter not in ["$", ","]
                    )
                )
            )
            return price

        def _get_stock(item) -> bool:
            stock_tag = item.find("strong")
            if stock_tag is not None:
                stock = False if (stock_tag.string == "Sold Out") else True
                return stock
            else:
                raise ValueError('Stock tag returned "None" while parsing')

        def _get_link(item) -> str:
            return "http://www.bestbuy.com/" + str(item.find("a").get("href"))

        # Try to parse item_cards from soup, if it fails return empty list
        try:
            soup = BeautifulSoup(html, "html.parser")
            item_cards = [
                item for item in soup.find_all("div", class_="shop-sku-list-item")
            ]
            logger.info(f"[{name}] {len(item_cards)} item cards parsed")
        except ValueError:
            logger.exception(f"[{name}]No item cards were parsed")
            return []

        if item_cards:
            for item in item_cards:
                try:
                    title = _get_title(item)
                    price = _get_price(item)
                    stock = _get_stock(item)
                    link = _get_link(item)

                    self.item_list.append(
                        Item(name, current_time, title, price, stock, link)
                    )

                except Exception:
                    logger.exception(f"Error parsing [{name}]")
                    return []

        logger.info(
            f"[{name}] Parsing complete: " f"{len(self.item_list)} items parsed"
        )

        if not self.item_list:
            logger.info(f"Parsing [{name}] returned no results")

        return self.item_list


class Parsers:
    """
    Lookup table for ScrapeManager to build scrapes
    """

    lookup = {"standard": StandardParser, "selenium": SeleniumParser}
