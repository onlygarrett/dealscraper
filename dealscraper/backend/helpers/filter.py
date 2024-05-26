import logging
from collections import namedtuple
from copy import deepcopy
from datetime import datetime
from typing import Dict, List, Optional

from dealscraper.backend.deal import Deal
from dealscraper.backend.helpers.output import OutputGen

DuplicatedDeal = namedtuple(
    "DuplicatedDeal",
    ["original", "duplicate", "type"],
)


class DealFilter(OutputGen):

    def __init__(
        self,
        user_ignore_dict: Optional[Dict[str, str]] = None,
        duplicate_games_dict: Optional[Dict[str, str]] = None,
        max_release_date: Optional[datetime] = None,
        log_level: int = logging.INFO,
        log_file: str = None,  # pyright: ignore
    ) -> None:
        super().__init__(
            log_level=log_level,
            output_file=log_file,
        )

        self.user_ignore_dict = user_ignore_dict or {}
        self.duplicate_games_dict = duplicate_games_dict or {}
        self.max_release_date = max_release_date

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
            (deal.title in self.user_ignore_dict)
            or (
                deal.sale_date
                and self.max_release_date
                and deal.sale_date < self.max_release_date
            )
            or (
                deal.title
                and self.duplicate_games_dict
                and deal.title in self.duplicate_games_dict
            )
        )

    def find_duplicates(
        self,
        existing_game_dict: Dict[str, Deal],
        incoming_game_dict: Dict[str, Deal],
    ) -> List[DuplicatedDeal]:

        duplicate_games_list = []
        filt_existing_game_dict = deepcopy(existing_game_dict)
        filt_incoming_game_dict = {}

        for game_title, incoming_game in incoming_game_dict.items():

            if game_title in existing_game_dict:
                self.logger.debug(
                    f"Identified duplicate {game_title} between incoming data "
                    "and existing data."
                )
                duplicate_games_list.append(
                    DuplicatedDeal(
                        original=existing_game_dict[game_title],
                        duplicate=incoming_game,
                        type=0,
                    )
                )

            elif game_title in self.duplicate_games_dict:
                self.logger.debug(
                    f"Identified existing content-matched duplicate {game_title} "
                    "in incoming data."
                )
                duplicate_games_list.append(
                    DuplicatedDeal(
                        original=None,
                        duplicate=incoming_game,
                        type=1,
                    )
                )
            else:

                filt_incoming_game_dict[game_title] = deepcopy(incoming_game)

        self.duplicate_games_dict.update(
            {
                j.duplicate.game_title: j.duplicate.as_json_entry
                for j in duplicate_games_list
            }
        )

        return duplicate_games_list
