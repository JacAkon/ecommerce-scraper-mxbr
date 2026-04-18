# settings.py

import os

class Config:
    # Mercado Libre API settings
    MERCADO_LIBRE_API_URL = 'https://api.mercadolibre.com'
    MERCADO_LIBRE_SEARCH_PATH = '/sites/{site_id}/search'
    MERCADO_LIBRE_RESULTS_LIMIT = 50

    # Supported sites: MLM = Mexico, MLB = Brazil
    MERCADO_LIBRE_SITES = {
        'MLM': {'country': 'Mexico', 'country_code': 'MX'},
        'MLB': {'country': 'Brazil', 'country_code': 'BR'},
    }

    # Logging configuration
    LOGGING_LEVEL = 'DEBUG'
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Data output paths
    OUTPUT_PATH = './output/'
    LOG_DIR = './logs/'
    LOG_FILE_PATH = os.path.join(LOG_DIR, 'app.log')

    # Scheduler configuration
    SCHEDULER_INTERVAL_MINUTES = 15

    # Search keywords
    SEARCH_KEYWORDS = ['Xiaomi', 'MIJIA', 'REALME', '美克多']

    # API request settings
    API_REQUEST_TIMEOUT = 10  # seconds
    API_MAX_RETRIES = 3

    # Data field definitions
    DATA_FIELDS = [
        'title',
        'original_price',
        'price',
        'sold_quantity',
        'rating',
        'reviews_count',
        'seller_name',
        'seller_followers',
        'product_url',
        'main_image_url',
        'channel_type',
        'country',
        'keyword',
        'scraped_at',
    ]

