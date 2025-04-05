from collections import defaultdict
import logging

from .notifier import Notifier
from ..data.item import Item

logger = logging.getLogger(__name__)


class Alerter:
    """
    Manages alerting functions such as price and stock notifications.

    Attributes:
    notifier = NotifierLogger class instance for notification handling
    max_discord_string = Truncates long titles for readability

    Methods:
    price_stock_alert() = Send discord alerts for items below a set
    price and stock threshold.
    compare() = compares two scrapes (dict of lists containing Item Objects)
    and returns a dict{dict} where the key=Changed Item and dict=Changes with
    keys 'price' and 'stock'.
    """
    def __init__(self, notifier, max_discord_string):
        self.notifier: Notifier = notifier
        self.max_discord_string = max_discord_string

    def __repr__(self):
        return f"Alerter(notifier={self.notifier!r})"

    def price_stock_alert(
            self,
            name: str,
            item_list: list[Item],
            threshold: int,
            in_stock=True
            ):
        """
        Checks items against a price threshold and sends discord notifications
        for items that are in stock and below that threshold.
        """

        if alert_items := [item for item in item_list
                           if item.price <= threshold
                           and item.stock is in_stock]:

            messages = [
                f"[{item.search}]\n"
                f"• {item.item[:self.max_discord_string]}...\n"
                f"Stock {'✅' if item.stock is True else '❌'}\n"
                f"${item.price}\n"
                f"🔗 {item.mdlink}\n"
                for item in alert_items
            ]

            logger.info(f"[{name}] Price alert: {len(alert_items)} "
                        f"item(s) below configured price threshold.")

            self.notifier.discord_message(
                f"\n⚠️⚠️**PRICE/STOCK ALERT**⚠️⚠️\n"
                f"Search Name: [{name}]\n"
                f"{len(alert_items)} items(s) are below your "
                f"configured price threshold of __${threshold}__")

            for message in messages:
                self.notifier.discord_message(message)

        else:
            logger.info(f"[{name}] No items below price threshold")

    def compare(self, 
                new_scrape: dict[str, list],
                last_scrape: dict[str, list]) -> dict:

        """
        Takes two dicts that have key = search name, values = list of Items
        and compares each new search to the old search for differences in
        price and stock.

        Returns a dict where
        key = Item Object,
        values = 'stock': bool, if the stock has changed
                 'listing' bool, if the listing was added or removed
                 'price': int, for the change in price
        """

        alert_items = defaultdict(dict)
        new_items = {}
        last_items = {}

        # If new scrape exists in last scrape
        for scrape_key, item in new_scrape.items():
            if scrape_key in last_scrape:

                # Make item dicts
                new_items = {item.item: item for item
                             in new_scrape[scrape_key]}
                last_items = {item.item: item for item
                              in last_scrape[scrape_key]}

                # Use sets to determine if there are new and removed listings
                new_listings_keys = set(new_items) - set(last_items)
                removed_listings_keys = set(last_items) - set(new_items)

                # Store listing info
                new_listings = [new_items[key] for key
                                in new_listings_keys]
                removed_listings = [last_items[key] for key
                                    in removed_listings_keys]

                # Add the listing to alert_items dict to return later
                for item in new_listings:
                    alert_items[item]['listing'] = True
                for item in removed_listings:
                    alert_items[item]['listing'] = False

            # For each new item
            for key, new_item in new_items.items():
                # If there is also a old item
                if key in last_items:
                    # Compare the items price
                    if (price_delta := new_item.price
                       - last_items[key].price) != 0:
                        alert_items[new_item]['price'] = price_delta
                    if (new_item.stock != last_items[key].stock):
                        alert_items[new_item]['stock'] = new_item.stock

        return alert_items

    def compare_alert(self,
                      new_scrape: dict[str, list[Item]],
                      last_scrape: dict[str, list[Item]]):

        """
        Grabs the alert_items dict from compare() and reads each item entry.
        For any changes it finds it sends a discord alert. Takes scrape info
        for two scrapes (new and last) in the form of a dict where the key is
        the search name and the values are a list of item objects.
        """
        alert_items = self.compare(new_scrape, last_scrape)

        if alert_items:
            for item, changes in alert_items.items():
                if 'price' in changes:
                    self.notifier.discord_message(
                        "⚠️Price change⚠\n"
                        f"[{item.search}]\n"
                        f"{item.item[:self.max_discord_string]}...\n"
                        f"Price: {'⬇️' if changes['price'] < 0 else '⬆️'} "
                        f"from ${item.price - changes['price']} by "
                        f"${abs(changes['price'])} to:\n "
                        f"--> **${item.price}** <--\n"
                        f"Stock: {'✅' if item.stock is True else '❌'}\n"
                        f"🔗{item.mdlink}"
                        )
                if 'stock' in changes:
                    self.notifier.discord_message(
                        "⚠️Stock changed⚠\n"
                        f"[{item.search}]\n"
                        f"{item.item[:self.max_discord_string]}...\n"
                        f"Stock is now: "
                        f"--> {'✅' if changes['stock'] is True else '❌'} <--\n"
                        f"${item.price}\n"
                        f"🔗{item.mdlink}"
                        )
                if 'listing' in changes:
                    n = changes['listing']
                    self.notifier.discord_message(
                       "⚠️Listing changed⚠\n"
                       f"[{item.search}]\n"
                       f"{item.item[:self.max_discord_string]}...\n"
                       f"{'**NEW Listing**' if n else '**REMOVED Listing**'}\n"
                       f"Stock: {'✅' if item.stock is True else '❌'}\n"
                       f"${item.price}\n"
                       f"🔗{item.mdlink}"
                       )
        else:
            logger.debug("No stock/price/listing changes")
