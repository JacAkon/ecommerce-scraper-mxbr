# Product Data Model

class Product:
    def __init__(self, title, original_price, price, sold_quantity, rating, reviews_count, seller_name, seller_followers, product_url, main_image_url, channel_type, country):
        self.title = title
        self.original_price = original_price
        self.price = price
        self.sold_quantity = sold_quantity
        self.rating = rating
        self.reviews_count = reviews_count
        self.seller_name = seller_name
        self.seller_followers = seller_followers
        self.product_url = product_url
        self.main_image_url = main_image_url
        self.channel_type = channel_type # 'cross_border' or 'local'
        self.country = country # 'MX' or 'BR'