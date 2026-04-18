# settings.py

import os

class Config:
    # Mercado Libre API settings
    MERCADO_LIBRE_API_URL = 'https://api.mercadolibre.com'
    MERCADO_LIBRE_CLIENT_ID = os.getenv('MERCADO_LIBRE_CLIENT_ID')
    MERCADO_LIBRE_CLIENT_SECRET = os.getenv('MERCADO_LIBRE_CLIENT_SECRET')
    
    # Logging configuration
    LOGGING_LEVEL = 'DEBUG'
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Data output paths
    OUTPUT_PATH = './output/'
    LOG_FILE_PATH = os.path.join(OUTPUT_PATH, 'app.log')

    # Scheduler configuration
    SCHEDULER_INTERVAL_MINUTES = 15  # Schedule each run every 15 minutes

    # Search keywords
    SEARCH_KEYWORDS = ['laptop', 'smartphone', 'tablet']

    # API request settings
    API_REQUEST_TIMEOUT = 10  # seconds

    # Site configuration
    SITE_COUNTRY = 'MX'
    SITE_CURRENCY = 'MXN'

    # Data field definitions
    DATA_FIELDS = {
        'title': 'item.title',
        'price': 'item.price',
        'seller_id': 'item.seller.id',
        'condition': 'item.condition',
        'shipping': 'item.shipping'
    }  

