import logging
import os
from typing import List, Optional


class DealScraperConfigHandler(object):
    """Handler that will hold all variables needed to scrape."""

    def __init__(self, arg):
        super(DealScraperConfigHandler, self).__init__()
        self.arg = arg
