import csv
import json
import os
import re
from datetime import date, datetime, timedelta
from time import time
from typing import Dict

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

from dealscraper.backend.deal import Deal
from dealscraper.backend.helpers import DealFilter, OutputGen
from dealscraper.config.handler import DealScraperConfigHandler
from dealscraper.data import DEAL_PALACE


class DealScraper(OutputGen):
    """Class for the scraper. This scraper is for scraping game deals"""

    def __init__(self, config: DealScraperConfigHandler) -> None:
        # config.validate()

        # Initialize the output file
        super().__init__(output_file=config.log_file)
        self.config = config
        self.__date_string = date.today().strftime("%Y-%m-%d")
        # dictionary to store the current deals
        self.current_deal_dict = {}

        # no use right now, will use in future
        self.session = requests.Session()

        # TODO: implement ignorelist
        user_ignore_dict = {}
        if os.path.isfile(self.config.user_ignore_list):
            user_ignore_dict = json.load(
                open(self.config.user_ignore_list, "r"))

        # TODO: implement duplocate games list
        duplicate_games_dict = {}  # type: Dict[str, str]
        if os.path.isfile(self.config.duplicate_games_list):
            duplicate_games_dict = json.load(
                open(self.config.duplicate_games_list, "r")
            )

        # Initialize our job filter
        self.job_filter = DealFilter(
            user_ignore_dict=user_ignore_dict,
            duplicate_games_dict=duplicate_games_dict,
            max_release_date=datetime.today()
            - timedelta(days=14),  # self.config.search_config.max_listing_days
            log_level=1,  # maybe make this a setting?
            log_file=self.config.log_file,
        )

        # Chromedrive blows but whatever
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        with Chrome(options=chrome_options) as browser:
            browser.get(DEAL_PALACE)
            self.page = browser.page_source

    def read_current_csv(self) -> Dict[str, Deal]:
        """
        Reads from the up-to-date csv containing scraped deals

        Returns:
            Dict[str, Deal]: Deal ojects
        """
        deals_dict = {}
        with open(
            self.config.current_deal_file, "r", encoding="utf8", errors="ignore"
        ) as deal_file:
            for row in csv.DictReader(deal_file):

                # checking cells
                if "Vendor" in row:
                    vendor = row["Vendor"]
                else:
                    vendor = ""
                sale_date = datetime.strptime(row["Date"], "%Y-%m-%d")

                if "Discount" in row:
                    discount = row["Discount"]
                else:
                    # TODO: can prob add a calculator here :thinking:
                    discount = "0"

                if "Original" in row:
                    og_price = row["Original"]
                else:
                    og_price = "0"

                if "Bundle" in row:
                    bundle = row["Bundle"]
                else:
                    bundle = "No bundle"

                deal = Deal(
                    id=int(row[""]),
                    title=row["Title"],
                    sale_price=row["Price"],
                    sale_date=sale_date,
                    vendor=vendor,
                    discount=discount,
                    original_price=og_price,
                    bundle_name=bundle,
                )
                # deal.validate()
                deals_dict[deal.id] = deal
        return deals_dict

    def run(self) -> None:
        """
        Main runner function
        """
        # TODO: read current deal dict from current csv and then compare
        if os.path.isfile(self.config.current_deal_file):
            self.current_deal_dict = self.read_current_csv()

        # TODO: read current deal dict from current csv nad update duplicate list
        # TODO: compare deals we just scraped with ignore and duplicates

        scraped_deals = self.scrape()
        # update current deal csv and output
        if not scraped_deals.empty:
            self.write_to_current_deals_csv(scraped_deals)
            self.logger.info(
                "Done. View your current deals in %s", self.config.current_deal_file
            )

    def write_to_current_deals_csv(self, deals: pd.DataFrame) -> None:
        """
        This function writes the scraped deals to the the current csv file
        """
        deals.to_csv(self.config.current_deal_file, encoding="utf8")
        self.logger.debug(
            "Wrote %d deals to %s", len(deals), self.config.current_deal_file
        )

    def scrape(self) -> pd.DataFrame:
        """
        Scrape deals from isthereanydeal.

        This function uses BeautifulSoup to parse the HTML content of the webpage,
        extracts relevant information about the deals, and returns a pandas DataFrame
        containing the scraped data.

        Returns:
            pd.DataFrame: A DataFrame containing the scraped deals. The DataFrame has the following columns:
                - Title: The title of the game.
                - Price: The sale price of the game.
                - Original: The original price of the game.
                - Discount: The discount percentage on the game.
                - Vendor: The vendor offering the deal.
                - Bundle: The name of the bundle (currently not implemented).
                - Date: The date of the deal.

        Raises:
            Exception: If any error occurs during the scraping process.
        """
        self.logger.info("Starting scrape of isthereanydeal")
        data = []
        start = time()
        soup = BeautifulSoup(self.page, "html.parser")

        games = soup.find_all(class_=re.compile("game svelte"))
        for game in games:
            name = game.find(class_=re.compile(
                "title svelte")).find("span").text
            deals = game.find(class_=re.compile("deal svelte"))

            sale_price = deals.find(class_=("ptag__price")).text
            old_price = deals.find(class_=("deal__old"))
            percent = deals.find(class_=("ptag__cutv"))
            vendor = deals.find(class_=("show svelte"))
            bundle_name = (
                ""  # TODO: bundles are currently setup diff; need to find a way
            )
            sale_date = self.__date_string

            # TODO: check for duplicates
            data.append(
                [
                    name,
                    sale_price,
                    "" if not old_price else old_price.text,
                    "" if not percent else percent.text,
                    "" if not vendor else vendor.text,
                    bundle_name,
                    sale_date,
                ]
            )
        df = pd.DataFrame(
            data,
            columns=[
                "Title",
                "Price",
                "Original",
                "Discount",
                "Vendor",
                "Bundle",  # pyright: ignore
                "Date",
            ],
        )
        end = time()
        self.logger.info(
            "Scraped %d deals from isthereanydeal, this took %.3fs",
            len(data),
            (end - start),
        )
        return df
