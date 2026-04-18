from typing import List

from config.settings import Config
from scrapers.base_scraper import BaseScraper
from scrapers.product_model import Product


class MercadoLibreScraper(BaseScraper):
    """Scraper for Mercado Libre (MLM = Mexico, MLB = Brazil)."""

    def __init__(self, site_id: str):
        super().__init__()
        if site_id not in Config.MERCADO_LIBRE_SITES:
            raise ValueError(
                f"Unsupported site_id '{site_id}'. Choose from {list(Config.MERCADO_LIBRE_SITES)}"
            )
        self.site_id = site_id
        self.site_info = Config.MERCADO_LIBRE_SITES[site_id]

    # ------------------------------------------------------------------
    # BaseScraper interface
    # ------------------------------------------------------------------

    def search(self, keyword: str) -> List[dict]:
        """Call the Mercado Libre public search API and return raw results."""
        path = Config.MERCADO_LIBRE_SEARCH_PATH.format(site_id=self.site_id)
        url = Config.MERCADO_LIBRE_API_URL + path
        params = {'q': keyword, 'limit': Config.MERCADO_LIBRE_RESULTS_LIMIT}

        self.logger.info("Searching site=%s keyword='%s'", self.site_id, keyword)
        data = self.api_client.get(url, params=params)
        if not data:
            self.logger.warning("No data returned for keyword='%s'", keyword)
            return []

        results = data.get('results', [])
        self.logger.info("Received %d results for keyword='%s'", len(results), keyword)
        return results

    def parse(self, raw_results: List[dict], keyword: str) -> List[Product]:
        """Parse raw API results into Product objects."""
        products = []
        for item in raw_results:
            try:
                product = self.extract_product_info(item)
                if product and self.validate_product(product):
                    products.append(product)
            except Exception as exc:
                self.logger.error("Failed to parse item %s: %s", item.get('id'), exc)
        return self.deduplicate(products)

    def extract_product_info(self, item: dict) -> Product | None:
        """Map a single raw API result to a Product."""
        try:
            # Prices
            price = item.get('price')
            original_price = item.get('original_price') or price

            # Seller info
            seller = item.get('seller', {})
            seller_name = self.clean_value(seller.get('nickname'))
            seller_followers = seller.get('seller_reputation', {}).get('transactions', {}).get(
                'total'
            )

            # Ratings / reviews
            review_data = item.get('reviews', {})
            rating = review_data.get('rating_average')
            reviews_count = review_data.get('total')

            # Image
            thumbnail = self.clean_value(item.get('thumbnail'))

            # Channel type: items with international shipping are cross-border
            shipping = item.get('shipping', {})
            is_cross_border = shipping.get('tags') and 'fulfillment' in shipping.get('tags', [])
            channel_type = 'cross_border' if is_cross_border else 'local'

            return Product(
                title=self.clean_value(item.get('title')),
                original_price=original_price,
                price=price,
                sold_quantity=item.get('sold_quantity'),
                rating=rating,
                reviews_count=reviews_count,
                seller_name=seller_name,
                seller_followers=seller_followers,
                product_url=self.clean_value(item.get('permalink')),
                main_image_url=thumbnail,
                channel_type=channel_type,
                country=self.site_info['country_code'],
            )
        except Exception as exc:
            self.logger.error("extract_product_info error: %s", exc)
            return None
