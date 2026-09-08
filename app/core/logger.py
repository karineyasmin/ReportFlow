import logging
from colorama import Fore, Style, init

init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom logging formatter to inject ANSI colors based on the log level."""

    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record with colors and precise structural metadata."""
        log_color = self.COLORS.get(record.levelno, "")

        format_str = (
            f"{Fore.WHITE}[%(asctime)s]{Style.RESET_ALL} "
            f"{log_color}[%(levelname)-8s]{Style.RESET_ALL} "
            f"{Fore.BLUE}(%(filename)s:%(lineno)d){Style.RESET_ALL} -> "
            f"{log_color}%(message)s{Style.RESET_ALL}"
        )

        formatter = logging.Formatter(format_str, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logger(name: str = "ReportFlow") -> logging.Logger:
    """Configures and returns an instance of the custom colored logger."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColoredFormatter())
        logger.addHandler(console_handler)

    return logger


logger = setup_logger()
