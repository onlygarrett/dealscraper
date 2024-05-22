import logging
import re
import sys

from datetime import date, datetime, timedelta
from typing import Optional


class OutputGen:
    """
    This class is a helper to abstract away generating the output of the scrape.
    """

    def __init__(
        self,
        output_folder: str,
        message_title: Optional[str] = None,
        message: Optional[str] = None,
    ) -> None:

        self.logger = logging.getLogger(message_title)
        self.logger.setLevel(1)
        format = logging.Formatter(message)
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(format)
        self.logger.addHandler(stdout_handler)

        file_handler = logging.FileHandler(output_folder)
        file_handler.setFormatter(format)
        self.logger.addHandler(file_handler)
