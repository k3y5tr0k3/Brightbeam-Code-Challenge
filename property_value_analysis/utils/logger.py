"""Custom logging configuration.

Classes:
    Logger:
        Handles the creation and custom configuration of a `logging.Logger`.
"""

import logging
import logging.config

from property_value_analysis.utils.config import Config


class Logger:
    """Custom logging configuration class.

    Attributes:
        LOGGING_CONFIG (dict):
            Custom logger configuration parameters.

    Methods:
        get_logger():
            Create and returns an instance of `logging.Logger` with a custom
            configuration.
    """

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] - %(message)s"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": "logs/app.log",
                "maxBytes": 10485760,
                "backupCount": 5,
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console", "file"],
            },
        },
    }

    @staticmethod
    def get_logger() -> logging.Logger:
        """Return an instance of `logging.Logger` with our custom configuration.

        Returns:
            logging.Logger:
                An instance of a logger with custom configuration.
        """
        logging.config.dictConfig(Logger.LOGGING_CONFIG)

        log_level: str
        try:
            log_level = Config.get_value("logging.level")
        except KeyError or ValueError:
            # default behavior
            log_level = "INFO"

        logger = logging.getLogger(__name__)
        logger.setLevel(log_level)
        return logger
