targets = [
    {
        "name": "RTX 5080",  # Name to tag this search
        "scrape_type": "standard",        # Scraper class to use. Reference Scrapers/Requesters/Parsers classes for lookup tables.
        "url": "https://www.example.com/products.html",  # Example html
        "discord_log": True,        # Send log type messages to discord. Not implimented.
        "price threshold": 1500,    # Price threshold for alerter
        "in_stock_alert": False     # True = Alert only to in stock items
    },
    {
        "name": "RTX 5080",
        "scrape_type": "selenium",
        "url": "https://www.example.com/products.html",  # Example html
        "discord_log": True,
        "price threshold": 1500,
        "in_stock_alert": False
    },
]
