# Scrapy settings for Opentable project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Opentable'

SPIDER_MODULES = ['Opentable.spiders']
NEWSPIDER_MODULE = 'Opentable.spiders'


LOG_LEVEL = 'INFO'

RESTURANT_FILENAME = 'resturants.csv'  # Main output filename in csv
MENU_CSV_FILENAME = 'menus.csv'  # menu csv filename in csv
HOURS_CSV_FILENAME = 'hours.csv'  # hours csv filename in csv
MENU_FILENAME = 'more_details.json'    # Menu and hours filename in json
IMAGES_STORE = r'./images'             # Image stored path


# Resturant CSV field headers, change position if needed
RESTURANT_FIELDS = ['url', 'Resturant ID', 'Establishment Name', 'Street Address 1', 'Street Address 2 (shown)', 'City', 'State', 'Zip Code', 'Latitude', 'Longitude', 'Website URL', 'Phone', 'Image Food_1', 'Image Food_2', 'Image Food_3', 'Image Food_4', 'Image Food_5', 'Image Drinks_1', 'Image Drinks_2', 'Image Drinks_3', 'Image Drinks_4', 'Image Drinks_5', 'Image Inside_1', 'Image Inside_2', 'Image Inside_3', 'Image Inside_4', 'Image Inside_5', 'Image Outside_1', 'Image Outside_2', 'Image Outside_3', 'Image Outside_4', 'Image Outside_5', 'Hours Of Operation', 'Price Range', 'Establishment Category', 'Cuisine(s)', 'Top Tags', 'Rating', 'Food Rating', 'Service Rating', 'Ambience Rating', 'Value Rating', 'About Business', 'Neighborhood', 'Cross Streets', 'Dress Code', 'Dining Style', 'Parking Details', 'Payment Options', 'Additional']

# Menu CSV field headers, change position if needed
MENU_FIELDS = ['url', 'Resturant ID', 'Establishment Name', 'Menu Type', 'Section', 'Section Description', 'Item Title', 'Item Description', 'Item Price']

# Hours CSV field headers, change position if needed
HOURS_FIELDS = ['url', 'Resturant ID', 'Establishment Name', 'Type', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'



CONCURRENT_REQUESTS = 8
DOWNLOAD_DELAY = 0.1

ITEM_PIPELINES = {
   'Opentable.pipelines.DuplicatesPipeline': 300,
   'Opentable.pipelines.DownloadImagePipeline': 301,
   'Opentable.pipelines.SaveMoreDetailPipeline': 302
}
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Opentable.middlewares.OpentableSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'Opentable.middlewares.OpentableDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'Opentable.pipelines.OpentablePipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
