import time

import requests

from config.settings import Config
from utils.logger import Logger


class APIClient:
    """HTTP client with retry logic (exponential back-off)."""

    def __init__(self, timeout: int = None, headers: dict = None):
        self.timeout = timeout or Config.API_REQUEST_TIMEOUT
        self.max_retries = Config.API_MAX_RETRIES
        self.headers = headers or {}
        self.logger = Logger(__name__)

    def get(self, url: str, params: dict = None) -> dict | None:
        """Send a GET request with retry on failure.

        Returns the parsed JSON response or None on permanent failure.
        """
        for attempt in range(1, self.max_retries + 1):
            try:
                self.logger.debug(
                    "GET %s params=%s (attempt %d/%d)", url, params, attempt, self.max_retries
                )
                response = requests.get(
                    url, params=params, headers=self.headers, timeout=self.timeout
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as exc:
                self.logger.error("HTTP error for %s: %s", url, exc)
                # Do not retry on client-side errors (4xx)
                if exc.response is not None and exc.response.status_code < 500:
                    return None
            except requests.exceptions.RequestException as exc:
                self.logger.error("Request error for %s: %s", url, exc)

            if attempt < self.max_retries:
                wait = 2 ** attempt
                self.logger.info("Retrying in %s seconds...", wait)
                time.sleep(wait)

        self.logger.error("All %d attempts failed for %s", self.max_retries, url)
        return None
