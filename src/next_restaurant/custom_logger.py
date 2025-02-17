import logging
from typing import Optional


class CustomLogger:
    def __init__(
        self,
        name: str,
        log_level: str = "DEBUG",
        log_dir: Optional[str] = None,
        verbose: bool = False,
    ):
        """
        Initialize a custom logger.

        :param name: Name of the logger.
        :param log_level: Logging level (e.g., DEBUG, INFO, WARNING, ERROR).
        :param log_dir: Directory for log files.
        :param verbose: Whether to log to console.
        """
        self.name = name
        self.log_level = log_level
        self.log_dir = log_dir
        self.verbose = verbose

        # Set up the logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))

        # Create formatters
        self.console_formatter = logging.Formatter("%(message)s")
        self.file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Add handlers
        if self.verbose:
            self.add_console_handler()
        if self.log_dir:
            self.add_file_handler()

    def add_console_handler(self) -> None:
        """Add a console handler."""
        ch = logging.StreamHandler()
        ch.setLevel(getattr(logging, self.log_level.upper()))
        ch.setFormatter(self.console_formatter)
        self.logger.addHandler(ch)
        return

    def add_file_handler(self) -> None:
        """Add a file handler."""
        fh = logging.FileHandler(f"{self.log_dir}/{self.name}.log")
        fh.setLevel(getattr(logging, self.log_level.upper()))
        fh.setFormatter(self.file_formatter)
        self.logger.addHandler(fh)
        return

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)
        return

    def info(self, msg: str) -> None:
        self.logger.info(msg)
        return

    def warning(self, msg: str) -> None:
        self.logger.warning(msg)
        return

    def error(self, msg: str) -> None:
        self.logger.error(msg)
        return

    def critical(self, msg: str) -> None:
        self.logger.critical(msg)
        return


# defining logger
APP_LOGGER: CustomLogger = CustomLogger(name="next_restaurant", log_level="INFO")

# Example usage:
if __name__ == "__main__":
    # Create a logger for system logs
    system_logger = CustomLogger(
        "system", log_level="INFO", log_dir="./logs", verbose=True
    )
    system_logger.info("System is running.")

    # Create a logger for database logs
    db_logger = CustomLogger("database", log_level="DEBUG", log_dir="./logs")
    db_logger.debug("Database query executed.")
