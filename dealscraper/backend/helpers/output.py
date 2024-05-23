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
        output_folder: Optional[str] = None,
        logger_name: Optional[str] = None,
        message_title: Optional[str] = None,
        message_format: Optional[str] = None,
    ) -> None:
        
        logger_name = logger_name or self.__class__.__name__
        message_format = message_format or (
            f"%(asctime)s - 1 - %(logger_name)s: - %(message)"
        )

        self.logger = logging.getLogger(message_title)
        self.logger.setLevel(1)
        format = logging.Formatter(message_format)
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(format)
        self.logger.addHandler(stdout_handler)

        file_handler = logging.FileHandler(output_folder)
        file_handler.setFormatter(format)
        self.logger.addHandler(file_handler)
