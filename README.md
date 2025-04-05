
# Price Scraper

Modular, extensible python tool for scraping and tracking product prices and stock availability.

This project was built as a learning experience in web scraping, data handling, and general python development.

It is intended for **educational and personal use only**


## Authors

- [StickySide](https://github.com/StickySide/)


## Features

- **Automated**: Scraping with retry logic and back-off to avoid rate-limiting.
- **Data Collection**: Saves scrapes to csv
- **Discord Notifications**: Rich discord notification system that alerts based on price thresholds, and historical stock and price changes.
- **Modular** Intended for python coders to plug their custom scraping code.


## Screenshots

![Alerts](https://github.com/StickySide/price-scraper/blob/main/images/alert.png)
![Stock and Price changes](https://github.com/StickySide/price-scraper/blob/main/images/Stocklisting.png)
![Data storage](https://github.com/StickySide/price-scraper/blob/main/images/excel.png)


## Roadmap

- **Graph Trends**: Plotting trends graphically
- **Web access**: Simple web server for self-hosted access to data and scraping configurations.


## Installation

```git clone https://github.com/stickyside/price-tracker.git```

```pip install requirements.txt```

```python -m price_scraper```

- If using the selenium based scraping options, you'll need firefox and geckodriver installed.


### Requirements
- Python 3, and these modules
    - discord
    - beautifulsoup4
    - pandas
    - requests
    - selenium


## Configuration

- **Scheduling**: Intended to be used with cron or another scheduler to run hourly.

- **General Configuration**: ```config.py``` contains general scraping configuration. The default values will work for most cases. You **will need to set your discord webhook** for notifications.

- **Scraping Targets**: ```targets.py``` contains a list of targets the program will target. I've left some of my settings in as an example, but stripped the URL for legal reasons. Each field is commented for set up. Add as many targets as you like.

- **Custom Code**: The ```Requester```, ```Parser```, and ```Scrape``` classes need some custom coding to scrape your desired website. You'll need some experience with scraping. I left my code in as an example.
    - ```Requester.get_html(name: str, url: str, headers=config.HEADERS)``` method takes a URL and outputs raw html in string format. Included are two examples, one using requests and one using selenium. The html is passed to the parser.
    - ```Parser.get_items(name: str, html: str)``` method is where youll have to experiment and set up your custom scraping. It takes the raw HTML and outputs a list of Item objects (see item.py) that contain all the data about the product. If the list is empty, the Scrape object will attempt to request the website and parse again untill reaching the maximum tries set in the ```config.py``` file.
    - ```Scrape``` objects and subclasses control the loop. No customization was needed to get my scrapes working but I included subclasses as an example of how they can be customised.

- **Notifications**: In Discord, navigate to a channel you own, click the gear icon to "Edit channel" and select "Integrations" then "Webhooks". Make a new webhook, name it, add an icon if you like and then "Copy webhook URL" and paste it into config.py WEBHOOK_URL. Optionally you can use environment variables as I have in the config file.

## Acknowledgements
- The awesome Python community

- GPU scalpers for the motivation to learn to code and create this script so I might snag one at a fair price...

## Disclaimer

> This project does **not come pre-configured** to scrape any real-world websites.  
> It is up to the user to ensure their use complies with the terms of service of any site they interact with.
Scraping websites without permission can violate their Terms of Service and may result in IP bans or legal consequences. Be respectful.

🛑 The example configuration and scrape types shown here are generic. 
This project does not contain any code explicitly tied to scraping live websites.
Users are expected to implement and use their own `Parser`, `Requester`, and `Scrape` logic for sites they have permission to access.

## License

[MIT](https://choosealicense.com/licenses/mit/)


