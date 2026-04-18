from abc import ABC, abstractmethod
from typing import List

from scrapers.product_model import Product
from utils.api_client import APIClient
from utils.logger import Logger


class BaseScraper(ABC):
    """Abstract base class that defines the scraper interface."""

    def __init__(self):
        self.api_client = APIClient()
        self.logger = Logger(self.__class__.__name__)
        self._seen_ids: set = set()

    # ------------------------------------------------------------------
    # Abstract interface
    # ------------------------------------------------------------------

    @abstractmethod
    def search(self, keyword: str) -> List[dict]:
        """Fetch raw search results from the platform."""

    @abstractmethod
    def parse(self, raw_results: List[dict], keyword: str) -> List[Product]:
        """Convert raw results into Product objects."""

    @abstractmethod
    def extract_product_info(self, item: dict) -> Product | None:
        """Extract a single Product from a raw item dict."""

    # ------------------------------------------------------------------
    # Common helpers
    # ------------------------------------------------------------------

    def validate_product(self, product: Product) -> bool:
        """Return True when the product has the minimum required fields."""
        return bool(product.title and product.product_url)

    def clean_value(self, value):
        """Return None for empty / whitespace strings, otherwise the value."""
        if isinstance(value, str):
            value = value.strip()
            return value if value else None
        return value

    def deduplicate(self, products: List[Product]) -> List[Product]:
        """Filter out products whose URL was already seen in this session."""
        unique = []
        for p in products:
            key = p.product_url
            if key and key not in self._seen_ids:
                self._seen_ids.add(key)
                unique.append(p)
        return unique
