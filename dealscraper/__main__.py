#!python

from dealscraper.backend.dealscraper import DealScraper
from dealscraper.config import build_config, get_config_handler


def main():
    """
    The main function orchestrates the entire application.

    This function initializes the configuration, creates a DealScraper instance,
    and runs the scraping process.

    Parameters:
    None

    Returns:
    None
    """
    config_env = build_config()  # Initialize the configuration based on environment variables
    config = get_config_handler(config_env)  # Get the appropriate configuration handler
    config.output_dir_gen()  # Generate the output directory based on the configuration

    scraper = DealScraper(config)  # Create a DealScraper instance with the configuration
    scraper.run()  # Run the scraping process


if __name__ == "__main__":
    main()
