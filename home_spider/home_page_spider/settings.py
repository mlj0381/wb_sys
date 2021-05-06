# Scrapy settings for home_page_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import redis

BOT_NAME = 'home_page_spider'

SPIDER_MODULES = ['home_page_spider.spiders']
NEWSPIDER_MODULE = 'home_page_spider.spiders'


ITEM_PIPELINES = {
   'scrapy_redis.pipelines.RedisPipeline': 300,
   'home_page_spider.pipelines.HomePageSpiderPipeline': 300,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'home_page_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
#不遵循爬虫协议
ROBOTSTXT_OBEY = False

#使用自定义cookies
COOKIES_ENABLED = False

#设置下载间隔时间
DOWNLOAD_DELAY = 1

#设置Mongodb数据库
MONGO_URL='mongodb://ch_sys_mongo:27017'

MONGO_DATABASE = 'spider'


REDIS_HOST = 'ch_sys_redis'
REDIS_PORT = 6379


#激活 管道
DOWNLOADER_MIDDLEWARES = {
    'home_page_spider.middlewares.UserAgentMiddlerware': 200

}

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#队列持久化
SCHEDULER_PERSIST = True
# Configure maximum concurrent requests performed by Scrapy (default: 16)
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"



#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
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
#    'home_page_spider.middlewares.HomePageSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'home_page_spider.middlewares.HomePageSpiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html

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
