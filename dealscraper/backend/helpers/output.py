import logging
import sys
from typing import Optional


class OutputGen:
    """
    This class is a helper to abstract away generating the output of the scrape.
    """

    def __init__(
        self,
        output_file: str,
        log_level: Optional[int] = None,
        logger_name: Optional[str] = None,
        message_title: Optional[str] = None,
        message_format: Optional[str] = None,
    ) -> None:
        """
        Initialize the OutputGen class.

        This class is a helper to abstract away generating the output of the scrape.
        It creates a logger with the specified log level and message format,
        and adds handlers for both stdout and a specified output file.

        Parameters:
        - output_file (str): The name of the output file where logs will be written.
        - log_level (Optional[int]): The log level for the logger. If not provided, defaults to 1.
        - logger_name (Optional[str]): The name of the logger. If not provided, defaults to the class name.
        - message_title (Optional[str]): The title of the log messages. If not provided, defaults to the logger name.
        - message_format (Optional[str]): The format of the log messages. If not provided, defaults to a standard format.

        Returns:
        - None
        """

        logger_name = logger_name or self.__class__.__name__
        message_format = message_format or (
            f"[%(asctime)s] [%(levelname)s] {logger_name}: %(message)s"
        )

        self.logger = logging.getLogger(message_title)
        if log_level:
            self.logger.setLevel(log_level)
        else:
            self.logger.setLevel(1)
        format = logging.Formatter(message_format)
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(format)
        self.logger.addHandler(stdout_handler)

        file_handler = logging.FileHandler(output_file)
        file_handler.setFormatter(format)
        self.logger.addHandler(file_handler)
