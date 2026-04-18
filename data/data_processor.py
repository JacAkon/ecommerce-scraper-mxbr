from datetime import datetime, timezone
from typing import List

from scrapers.product_model import Product
from utils.logger import Logger


class DataProcessor:
    """Handles data cleaning, normalisation, and validation."""

    def __init__(self):
        self.logger = Logger(__name__)

    def clean_data(self, products: List[dict]) -> List[dict]:
        """Remove records that have no title or product_url, and deduplicate."""
        seen_urls: set = set()
        cleaned = []
        for record in products:
            url = record.get('product_url')
            if not record.get('title') or not url:
                continue
            if url in seen_urls:
                continue
            seen_urls.add(url)
            cleaned.append(record)
        self.logger.info("clean_data: %d -> %d records", len(products), len(cleaned))
        return cleaned

    def normalize_data(self, products: List[dict]) -> List[dict]:
        """Normalise and format individual fields."""
        normalized = []
        for record in products:
            record = dict(record)
            # Numeric fields: replace None with 0
            for field in ('price', 'original_price', 'sold_quantity', 'reviews_count',
                          'seller_followers'):
                if record.get(field) is None:
                    record[field] = 0
            # Numeric fields: float precision
            for field in ('price', 'original_price', 'rating'):
                if record.get(field) is not None:
                    try:
                        record[field] = round(float(record[field]), 2)
                    except (TypeError, ValueError):
                        record[field] = 0.0
            # String fields: strip whitespace
            for field in ('title', 'seller_name', 'channel_type', 'country'):
                if isinstance(record.get(field), str):
                    record[field] = record[field].strip()
            normalized.append(record)
        return normalized

    def add_timestamp(self, products: List[dict], keyword: str = '') -> List[dict]:
        """Add scraped_at timestamp and search keyword to every record."""
        ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        for record in products:
            record['scraped_at'] = ts
            record['keyword'] = keyword
        return products

    def validate_product(self, product: dict) -> bool:
        """Return True when the record contains the minimum required fields."""
        return bool(product.get('title') and product.get('product_url'))

    def product_to_dict(self, product: Product) -> dict:
        """Convert a Product object to a plain dict."""
        return {
            'title': product.title,
            'original_price': product.original_price,
            'price': product.price,
            'sold_quantity': product.sold_quantity,
            'rating': product.rating,
            'reviews_count': product.reviews_count,
            'seller_name': product.seller_name,
            'seller_followers': product.seller_followers,
            'product_url': product.product_url,
            'main_image_url': product.main_image_url,
            'channel_type': product.channel_type,
            'country': product.country,
        }
