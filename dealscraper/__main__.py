#!python

import os
import sys
from dealscraper.backend import dealscraper


if __name__ == "__main__":
    dealscraper.DealScraper().scrape()