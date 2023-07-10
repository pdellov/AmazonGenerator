# Amazon Scraper to WordPress Publisher

This is an automated system that does the following:
1. Scrapes product data and reviews from Amazon based on a defined search.
2. Collects product information and reviews.
3. Uses ChatGPT to write an article for each product.
4. Publishes each article to a WordPress site.

The system uses Oxylabs for scraping, OpenAI's GPT-4 for generating the articles, and WordPress's REST API for publishing the articles.

## Setup and Launch

To set up and launch the system:

1. Fill out the `config_sample.ini` file with the appropriate details, then rename it to `config.ini`.
2. Fill out the `instructions.ini` file with the desired parameters.
3. Run the `main.py` file.

Detailed explanations for `config.ini` and `instructions.ini` are provided below.

### config.ini

This file contains the configuration for the Oxylabs, OpenAI, and WordPress settings:

```ini
[OXYLABS]
user = HERE YOUR USERNAME
password = HERE YOUR PASSWORD
amazondomain = it

[OPENAI]
apikey = YOUR API KEY HERE
lang = italiano

[WORDPRESS]
admin = YOUR WORDPRESS USER
password = YOUR WORDPRESS APPLICATION PASSWORD
url = https://www.yoursite.com
category_id = 1
```

OXYLABS: Enter your Oxylabs username and password. amazondomain is the Amazon website to scrape from (in this case, it for Amazon Italy).
OPENAI: Enter your OpenAI API key. The lang field is the language for the GPT-4 generated articles.
WORDPRESS: Enter your WordPress username and application password. url is your WordPress site URL. category_id is the WordPress category where the articles will be published.


### instructions.ini
This file contains the instructions for the Amazon scraping:

```ini
[GENERAL]
query = zaini da trail
start_page = 1
pages = 2
category = 3102251031
products_limit = 3
```

query: This is the search term that will be used on Amazon.
start_page: This is the starting page for the Amazon search results.
pages: This is the number of search result pages to scrape from Amazon.
category: This is the Amazon node to scrape.
products_limit: This is the maximum number of products to scrape.
After completing these setup steps, run main.py to start the scraping, article generation, and publication process.