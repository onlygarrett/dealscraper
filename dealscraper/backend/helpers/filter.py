import logging
from collections import namedtuple
from copy import deepcopy
from datetime import datetime
from typing import Dict, List, Optional

from dealscraper.backend.scraper import Deal
from dealscraper.backend.helpers.output import OutputGen

DuplicatedDeal = namedtuple(
    "DuplicatedDeal",
    ["original", "duplicate", "type"],
)


class DealFilter(OutputGen):
    """
    Class for filtering deals.
    This class provides methods for filtering deals based on various criteria.
    """
    def __init__(
        self,
        ignored_games: Optional[Dict[str, str]] = None,
        duplicate_games: Optional[Dict[str, str]] = None,
        scrape_date: Optional[datetime] = None,
        log_level: int = logging.INFO,
        log_file: str = None,  # pyright: ignore
    ) -> None:
        """
        Initialize DealFilter object.

        Parameters:
        ignored_games (Optional[Dict[str, str]]): A dictionary of game titles to ignore.
        duplicate_games (Optional[Dict[str, str]]): A dictionary of game titles to match for duplicates.
        scrape_date (Optional[datetime]): The scrape date for games to consider.
        log_level (int): The log level for logging messages. Default is logging.INFO.
        log_file (str): The file to log messages to. Default is None.

        Returns:
        None
        """
        super().__init__(
            log_level=log_level,
            output_file=log_file,
        )

        self.ignored_games = ignored_games or {}
        self.duplicate_games = duplicate_games or {}
        self.scrape_date = scrape_date

    # TODO: implement filter
    def apply_filter(
        self,
        deals: Dict[str, Deal],
        remove_dupes: bool = True,
    ) -> Dict[str, Deal]:

        filtered = {
            key: deal
            for key, deal in deals.items()
            if not self.can_filter(deal, dupe_check=remove_dupes)
        }

        return filtered

    def can_filter(self, deal: Deal, dupe_check: bool = True) -> bool:
        return bool(
            (deal.title in self.ignored_games)
            or (
                deal.sale_date
                and self.scrape_date
                and deal.sale_date < self.scrape_date
            )
            or (
                deal.title
                and self.duplicate_games
                and deal.title in self.duplicate_games
            )
        )

    # TODO: implement dupe checker
    def find_duplicates(
        self,
        old_games: Dict[str, Deal],
        new_games: Dict[str, Deal],
    ) -> List[DuplicatedDeal]:

        dupe_list = []
        old_games_filter = deepcopy(old_games)
        new_games_filter = {}

        for game_title, incoming_game in new_games.items():

            if game_title in old_games:
                self.logger.debug(
                    f"Identified duplicate {game_title} between incoming data "
                    "and existing data."
                )
                dupe_list.append(
                    DuplicatedDeal(
                        original=old_games[game_title],
                        duplicate=incoming_game,
                        type=0,
                    )
                )

            elif game_title in self.duplicate_games:
                self.logger.debug(
                    f"Identified existing content-matched duplicate {
                        game_title} "
                    "in incoming data."
                )
                dupe_list.append(
                    DuplicatedDeal(
                        original=None,
                        duplicate=incoming_game,
                        type=1,
                    )
                )
            else:

                new_games_filter[game_title] = deepcopy(incoming_game)

        self.duplicate_games.update(
            {
                j.duplicate.game_title: j.duplicate.as_json_entry
                for j in dupe_list
            }
        )

        return dupe_list
