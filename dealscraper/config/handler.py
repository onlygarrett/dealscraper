import os
from typing import List

from dealscraper.config import BoilerPlateConfig


class DealScraperConfigHandler(BoilerPlateConfig):
    """Handler that will hold all variables needed to scrape."""

    def __init__(
        self,
        current_deal_file: str,
        user_ignore_list: str,
        dupe_list: str,
        log_file: str,
        deal_palace: str
    ):
        """
        Initialize DealScraperConfigHandler with necessary file paths.

        Parameters:
        current_deal_file (str): Path to the file where current deals will be stored.
        user_ignore_list (str): Path to the file containing user's ignored games.
        dupe_list (str): Path to the file containing duplicate games.
        log_file (str): Path to the file where logs will be stored.
        deal_palace (str): Path to the deal palace.

        Returns:
        None
        """
        super().__init__()
        self.current_deal_file = current_deal_file
        self.user_ignore_list = user_ignore_list
        self.dupe_list = dupe_list
        self.log_file = log_file
        self.deal_palace = deal_palace
        
    def output_dir_gen(self) -> None:
        """
        This will create the necessary directories in the project folder
        for the output of the csv and logging if not already generated.
        """
        for pwd in [
            self.current_deal_file,
            self.log_file,
            self.dupe_list,
            self.user_ignore_list,
        ]:
            file_pwd = os.path.dirname(os.path.abspath(pwd))
            if not os.path.exists(file_pwd):
                os.makedirs(file_pwd)
