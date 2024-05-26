from typing import Any, Dict

import yaml

from dealscraper.config.handler import DealScraperConfigHandler


def build_config() -> Dict[str, Any]:
    """
    This builder function is to be used to build
    the config to be used in the config handler.
    """

    config = yaml.load(
        open("./settings/base_settings.yml", "r"),
        Loader=yaml.FullLoader,
    )
    # TODO: add yaml validator
    return config


def get_config_handler(config: Dict[str, Any]) -> DealScraperConfigHandler:
    """
    This funtion grabs a handler for the built config.
    """

    deal_cfg_handler = DealScraperConfigHandler(
        current_deal_file=config["current_csv_file"],
        user_ignore_list=config["user_ignore_list"],
        duplicate_games_list=config["duplicate_games_list"],
        log_file=config["log_file"],
    )
    return deal_cfg_handler
