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
    # This is where the cli parsing abstraction will happen.
    # args = parse_cli(sys.argv[1:])

    # Initialize the configuration based on environment variables
    config_env = build_config()
    # Get the appropriate configuration handler
    config = get_config_handler(config_env)
    config.output_dir_gen()  # Generate the output directory based on the configuration

    # Create a DealScraper instance with the configuration
    scraper = DealScraper(config)
    scraper.run()  # Run the scraping process


if __name__ == "__main__":
    main()
