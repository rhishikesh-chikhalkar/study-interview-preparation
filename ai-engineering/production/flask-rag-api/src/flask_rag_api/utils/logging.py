import logging
import sys


def setup_logging(level: int = logging.INFO) -> None:
    """Configures structured logging for the application."""
    log_format = "[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s"
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with specified module name."""
    return logging.getLogger(name)
