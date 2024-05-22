import csv
import json
import os
import pickle
from datetime import date, datetime, timedelta
from time import time
from typing import Dict, List

from requests import Session
from dealscraper.config.handler import DealScraperConfigHandler


class DealScraper(object):
    """Class for the scraper. This scraper is for scraping game deals"""

    def __init__(self, config: DealScraperConfigHandler):
        super(DealScraper, self).__init__()
        self.config = config
