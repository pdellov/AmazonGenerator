from utils.amazon_scraper import amazonScrape,amazonProduct
from utils.article_writer import articleWriter
from configparser import ConfigParser
config_object = ConfigParser()
config_object.read('instructions.ini')
GENERAL = config_object["GENERAL"]

scrape = amazonScrape()
scrape.get_search(GENERAL['query'],GENERAL['start_page'],GENERAL['pages'],GENERAL['category'])
scrape.products_from_list()

for product in scrape.products:
    article = articleWriter()
    article.write_fromproduct(product)
    article.eeatize()
    article.generate_title()
    article.wordpress_publish(product.image)








