#!python

from dealscraper.backend.dealscraper import DealScraper
from dealscraper.config import build_config, get_config_handler


def main():
    config_env = build_config()
    config = get_config_handler(config_env)
    config.output_dir_gen()

    scraper = DealScraper(config)
    scraper.run()


if __name__ == "__main__":
    main()
