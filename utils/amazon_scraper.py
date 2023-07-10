
import requests
from configparser import ConfigParser

class amazonScrape:
    def __init__(self):
            config_object = ConfigParser()
            config_object.read('config.ini')
            OXYLABS = config_object["OXYLABS"]

            self.user = OXYLABS['user']
            self.password = OXYLABS['password']
            self.amazondomain = OXYLABS['amazondomain']
            self.products = list()

            instruction_object = ConfigParser()
            instruction_object.read('instructions.ini')
            GENERAL = instruction_object["GENERAL"]

            self.products_limit = GENERAL['products_limit']
            

    def get_search(self,query,start_page,pages,category):
        payload = {
            'source': 'amazon_search',
            'domain': self.amazondomain,
            'query': query,
            'start_page': start_page,
            'pages': pages,
            'parse': True,
            'context': [
                {'key': 'category_id', 'value': category}
            ],
        }


        # Get response.
        search_results = requests.request(
            'POST',
            'https://realtime.oxylabs.io/v1/queries',
            auth=(self.user, self.password),
            json=payload,
        ).json()

        self.products_json = search_results['results'][0]['content']['results']['organic']

    def get_product(self,asin):
        # Structure payload.
        payload = {
            'source': 'amazon_product',
            'domain': 'it',
            'query': asin,
            'parse': True,
            'context': [
            {
            'key': 'autoselect_variant', 'value': True
            }],
        }


        # Get response.
        product_info = requests.request(
            'POST',
            'https://realtime.oxylabs.io/v1/queries',
            auth=(self.user,self.password),
            json=payload,
        ).json()

        # Reviews
        # Structure payload.
        payload = {
            'source': 'amazon_reviews',
            'domain': 'it',
            'query': asin,
            'parse': True,
        }

        # Get response.
        reviews_list = requests.request(
            'POST',
            'https://realtime.oxylabs.io/v1/queries',
            auth=(self.user, self.password),
            json=payload,
        ).json()
        
        # Extract information from JSON
        product_name = product_info['results'][0]['content']['product_name']
        product_price = str(product_info['results'][0]['content']['price']) + str(product_info['results'][0]['content']['currency'])
        product_description = product_info ['results'][0]['content']['description']
        product_details = product_info['results'][0]['content']['product_details']
        product_image = product_info['results'][0]['content']['images'][0]
        product_url = product_info['results'][0]['content']['url']
        product_reviews = reviews_list['results'][0]['content']['reviews']

        product = amazonProduct(asin,product_name,product_description,product_price,product_details,product_image,product_url,product_reviews)

        return product
    
    def products_from_list(self):
        for index, product_json in enumerate(self.products_json):
            self.products.append(self.get_product(product_json['asin']))
            if index == self.products_limit:
                break
    
class amazonProduct:
    def __init__(self,asin,name,description,price,details,image,url,product_reviews):
        self.asin = asin
        self.name = name
        self.description = description
        self.price = price
        self.details = details
        self.image = image
        self.url = url
        self.reviews = self.read_reviews(product_reviews)
    
    def read_reviews(self,product_reviews):
        reviews_list = ''
        j = 0
        for review in product_reviews:
            j = j + 1
            reviews_list = reviews_list + "Review n. " + str(j) + " Title: "\
                + review['title'] + " - Text: " + review['content'] + "\n"
        
        return reviews_list
    
    def update_data(self,asin,name,description,price,details,image,url,product_reviews):
        if asin is not None:
            self.asin = asin
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if price is not None:
            self.price = price
        if details is not None:
            self.details = details
        if image is not None:
            self.image = image
        if url is not None:
            self.url = url
        if product_reviews is not None:
            self.reviews = self.read_reviews(product_reviews)
    
