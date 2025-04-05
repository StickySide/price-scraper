class Item():
    """
    Represents item scraped from website.

    Attributes:
    search (str) = The name of the search that produced item
    time (str) = Time the item was scraped
    item (str) = Title of the item from the website
    price (int) = Item price
    stock (bool) = bool for in stock or not
    link (str) = URL

    Methods:
    as_dict(): returns attributes in dict format
    """
    def __init__(
        self,
        search: str,
        time: str,
        item: str,
        price: int,
        stock: bool,
        link: str
    ):

        self.search = search
        self.time = time
        self.item = item
        self.price = price
        self.stock = stock
        self.link = link

    def __repr__(self) -> str:
        return (
            f"Item(search={self.search!r}, "
            f"time={self.time!r}, "
            f"item={self.item!r}, "
            f"price={self.price!r}, "
            f"stock={self.stock!r}, "
            f"link={self.link!r})"
            )

    def __str__(self) -> str:
        # if len(self.item) >= 30:
        #     name = self.item[:30]
        # else:
        #     name = self.item
        return (
            f"{self.item[:30] + '...' if len(self.item) > 30 else self.item}"
            f", Stock: {self.stock}, ${self.price}")

    def __eq__(self, other) -> bool:
        return (self.item == other.item and
                self.price == other.price and
                self.stock == other.stock)

    def __hash__(self):
        return hash((self.item, self.price, self.stock))

    def __bool__(self) -> bool:
        return self.stock

    def as_dict(self) -> dict:
        """
        Returns item attributes as dict
        """
        return {
            "time": self.time,
            "item": self.item,
            "price": self.price,
            "stock": self.stock,
            "link": self.link
        }

    @property
    def mdlink(self) -> str:
        """
        Returns the link in markdown format for discord.
        """
        link = f'[Link]({self.link})'
        return link
