import logging
import os
import sys

from config.settings import Config


class Logger:
    """Handles console and file logging."""

    def __init__(self, name: str):
        self._logger = logging.getLogger(name)
        if not self._logger.handlers:
            self._setup(name)

    def _setup(self, name: str):
        level = getattr(logging, Config.LOGGING_LEVEL.upper(), logging.DEBUG)
        self._logger.setLevel(level)

        formatter = logging.Formatter(Config.LOGGING_FORMAT)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

        # File handler
        log_dir = Config.LOG_DIR
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(Config.LOG_FILE_PATH, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._logger.critical(msg, *args, **kwargs)
