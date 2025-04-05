import logging
import os

# Scraper Config
HEADERS = {  # Optional headers to send with web requests
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"  # noqa E501
    ),
    "Accept-Language": "en-US,en;q=0.9",
}
MAX_TRIES = 60  # Maximum website request tries before price scraper gives up
MIN_TRY_TIME = 10  # Sets minimum interval between tries in seconds
MAX_TRY_TIME = 30  # Maximum interval between tries in seconds
SELENIUM_DWELL_TIME = 8  # Time selenium based scrapers will wait for javascript to load 

# Logging
LOG_LEVEL = logging.INFO  # Log level
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'  # Format for logger 
LOG_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'  # Date format for logger
DATA_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'  # Date format for saved data in CSV file
MAX_LOG_SIZE = (1024 * 1024)  # Maximum log size before it rolls over to a second file (1 megabyte)
MAX_BACKUP_LOGS = 3  # Maximum backup logs before they start getting deleted

# Files
DATA_FILE = 'data.csv'  # Path to data storing all scrapes
LOG_FILE = 'price_scraper.log'  # Path to log file
LAST_SCRAPE_FILE = 'last_scrape.pkl'  # Path to pickle file used to compare the last scrape

# Discord
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")  # Discord webhook. You can just paste the URL here if you dont want to use env variables
MAX_DISCORD_STRING = 35  # Some item titles are very long, this truncates them for readability
