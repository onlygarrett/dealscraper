import os

from dealscraper.config import BoilerPlateConfig


class DealScraperConfigHandler(BoilerPlateConfig):
    """Handler that will hold all variables needed to scrape."""

    def __init__(
        self,
        current_deal_file: str,
        user_ignore_list: str,
        duplicate_games_list: str,
        log_file: str,
    ):
        """
        Initialize DealScraperConfigHandler with necessary file paths.

        Parameters:
        current_deal_file (str): Path to the file where current deals will be stored.
        user_ignore_list (str): Path to the file containing user's ignored games.
        duplicate_games_list (str): Path to the file containing duplicate games.
        log_file (str): Path to the file where logs will be stored.

        Returns:
        None
        """
        super().__init__()
        self.current_deal_file = current_deal_file
        self.user_ignore_list = user_ignore_list
        self.duplicate_games_list = duplicate_games_list
        self.log_file = log_file

    def output_dir_gen(self) -> None:
        """
        This will create the necessary directories in the project folder
        for the output of the csv and logging if not already generated.
        """
        for pwd in [
            self.current_deal_file,
            self.log_file,
            self.duplicate_games_list,
            self.user_ignore_list,
        ]:
            file_pwd = os.path.dirname(os.path.abspath(pwd))
            if not os.path.exists(file_pwd):
                os.makedirs(file_pwd)
