import csv
import json
import os
import pickle
from datetime import date, datetime, timedelta
import re
from time import time
import pandas as pd
import numpy as np
from typing import Dict, List
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

import requests
from dealscraper.config.handler import DealScraperConfigHandler
from dealscraper.backend.helpers import Logger
from dealscraper.backend.helpers import DealFilter

class DealScraper(Logger):
    """Class for the scraper. This scraper is for scraping game deals"""
    
    
    def __init__(self):
        
        self.__date_string = date.today().strftime("%Y-%m-%d")
        self.new_deals = {}
        
        self.session = requests.Session()
        if self.config.proxy_config:
            self.session.proxies = {
                self.config.proxy_config.protocol: self.config.proxy_config.url
            }

        user_ignore_dict = {}
        if os.path.isfile(self.config.user_ignore_list):
            user_ignore_dict = json.load(
                open(self.config.user_ignore_list, 'r')
            )
            
        duplicate_games_dict = {}  # type: Dict[str, str]
        if os.path.isfile(self.config.duplicates_list_file):
            duplicate_games_dict = json.load(
                open(self.config.duplicates_list_file, 'r')
            )
            
        # Initialize our job filter
        self.job_filter = DealFilter(
            user_ignore_dict,
            duplicate_games_dict,
            datetime.datetime.today() - timedelta(days=self.config.search_config.max_listing_days),
            log_level=self.config.log_level,
            log_file=self.config.log_file,
        )
        
        URL = "https://isthereanydeal.com/deals/"
        chrome_options = Options()  
        chrome_options.add_argument("--headless")
        with Chrome(options=chrome_options) as browser:
            browser.get(URL)
            self.page = browser.page_source
        
        
        
        

    def scrape(self):
        data = []
        soup = BeautifulSoup(self.page,"html.parser")
        
        games = soup.find_all(class_=re.compile("game svelte"))
        for game in games:
            name = game.find(class_=re.compile("title svelte"))
            deals = game.find(class_=re.compile("deal svelte"))

            discount = deals.find(class_=("ptag__price"))
            old_price = deals.find(class_=("deal__old"))
            percent = deals.find(class_=("ptag__cutv"))

            data.append([name, discount, old_price, percent])
            df = pd.DataFrame(data, columns=['Game Title', 'Sale Price', 'Original Price', 'Discount'])
        print(df)