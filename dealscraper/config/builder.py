from typing import Any, Dict, List

import argparse
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
        dupe_list=config["dupe_list"],
        log_file=config["log_file"],
        deal_palace=config["deal_palace"]
    )
    return deal_cfg_handler


# TODO: IMPLEMENT
def cli_input(args: List[str]) -> Dict[str, Any]:
    """
    Parse the command line arguments into a dictionary.

    This function uses argparse module to parse command line arguments. It creates a base parser and a subparser for 
    'load' and 'inline' options. The 'inline' option is used to pass arguments by CLI.

    Parameters:
    args (List[str]): A list of command line arguments.

    Returns:
    Dict[str, Any]: A dictionary containing the parsed command line arguments.

    Raises:
    argparse.ArgumentError: If the command line arguments are not provided or are invalid.

    """
    base_parser = argparse.ArgumentParser()

    base_subparsers = base_parser.add_subparsers(
        dest='load | inline',
        help='Pass load with a YAML config or inline to pass args by CLI.',
        required=True,
    )

    # We are using CLI for all arguments.
    cli_parser = base_subparsers.add_parser(
        'inline',
        help='Configure search query and data providers via CLI.',
    )
    return vars(base_parser.parse_args(args))