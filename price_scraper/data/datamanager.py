import logging
import os
import pickle

import pandas as pd

from price_scraper.notifications.notifier import Notifier

logger = logging.getLogger(__name__)


class DataManager:
    """
    Manages saving and loading data

    Attributes:
    self.notifier = self.notifierLogger object class for notifications/logging
    data_file = name/location of data.csv
    last_scrape_file = pickle file storing the results of the last scrape

    Methods:
    save_to_csv(): converts data into a dataframe then saves as a CSV
    save_to_pickle(): saves input into a pickle file
    """
    def __init__(self,
                 notifier: Notifier,
                 data_file: str,
                 last_scrape_file):

        self.notifier = notifier
        self.data_file = data_file
        self.last_scrape_file = last_scrape_file

    def __repr__(self):
        return (f"DataManager(self.notifier: {self.notifier!r},\n"
                f"data_file={self.data_file!r})")

    def save_to_csv(self, name: str, data: list[dict]):
        """
        Takes a list of dictionaries with product information (mainly from
        Scrape.items_to_dict()) converts to a pandas dataframe and either
        saves a new file or appends to an existing one.
        """
        df = pd.DataFrame(data)
        try:
            if os.path.isfile(self.data_file):
                df.to_csv(self.data_file, mode='a', header=False)
                logger.debug(
                    f"[{name}] {self.data_file} appended"
                    )
            else:
                df.to_csv(self.data_file)
                logger.debug(
                    f"[{name}] {self.data_file} created"
                    )
        except Exception as e:
            logger.exception(
                f"Error saving [{name}] {self.data_file}: {e}"
                )

    def save_to_pickle(self, items, file_name):
        try:
            with open(file_name, 'wb') as file:
                pickle.dump(items, file)
        except Exception as e:
            logger.exception(f"ERROR: Unable to save {file_name}: {e}")
        logger.debug(f"DEBUG: Saved {file_name}")

    def load_from_pickle(self, file_name):
        try:
            with open(file_name, 'rb') as file:
                file_data = pickle.load(file)
                logger.debug(f"Loaded {file_name}")
                return file_data
        except Exception as e:
            logger.exception(f"Unable to load {file_name} {e}")
