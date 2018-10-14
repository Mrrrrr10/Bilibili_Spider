# -*- coding: utf-8 -*-

# Scrapy settings for Bilibili_Spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Bilibili_Spider'

SPIDER_MODULES = ['Bilibili_Spider.spiders']
NEWSPIDER_MODULE = 'Bilibili_Spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Scrapy_Project (+http://www.yourdomain.com)'


# 是否遵守机器人协议
ROBOTSTXT_OBEY = False


# 配置Scrapy执行的最大并发请求（默认值：16）
# CONCURRENT_REQUESTS = 32


# ------ 下载延迟设置 ------
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# ------ 是否启用cookie,默认为不启用 ------
# COOKIES_ENABLED = False


# ------ 禁用Telnet控制台（默认启用） ------
# TELNETCONSOLE_ENABLED = False


# ------ 可在特定的爬虫spider文件设置 ------
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }


# ---------- Middleware ----------
# 启用或者禁用 spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'Bilibili_Spider.middlewares.ScrapyProjectSpiderMiddleware': 543,
# }

# 启用或者禁用 downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'Bilibili_Spider.middlewares.BilibiliSpiderDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,     # 禁用scrapy原有的User-Agent
    'Bilibili_Spider.middlewares.RandomUserAgentMiddleware': 300,
    'Bilibili_Spider.middlewares.RandomProxyMiddleware': 554,        # Proxy Pool
    # 'Bilibili_Spider.middlewares.ABProxyMiddleware': 554,
    # 'Bilibili_Spider.middlewares.MoguProxyMiddleware': 554,
}

RANDOM_UA_TYPE = "random"
PROXY_POOL_URL = 'http://localhost:5555/random'     # Proxy Pool

# -------------------------------------------------
# 启用或者禁用扩展
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#    'scrapy.extensions.closespider.CloseSpider': 500
# }
# CLOSESPIDER_TIMEOUT = 84600   # 爬虫运行超过23.5小时，如果爬虫还没有结束，则自动关闭


# 配置pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'Bilibili_Spider.pipelines.TimePipeline': 300,
    'Bilibili_Spider.pipelines.Bilibili_Pipeline': 301,
    'Bilibili_Spider.pipelines.MongoPipeline': 301,
}

# MongoDB数据库配置
MONGODB_HOST = "127.0.0.1"
MONGODB_PORT = 27017
MONGODB_DBNAME = 'Bilibili'

# Redis
REDIS_URL = "redis://root:@127.0.0.1:6379"
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

# 时间处理
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M"
GMT_FORMAT = "%a %b %d %H:%M:%S +0800 %Y"

RETRY_HTTP_CODES = [401, 403, 407, 408, 414, 500, 502, 503, 504]

# ---------- 自动限速(AutoThrottle)扩展 ----------
# 启用并配置AutoThrottle扩展（默认情况下禁用）
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False


# 启用并配置HTTP缓存（默认情况下禁用）
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# HTTPERROR_ALLOWED_CODES = [429, 403]

# ---------- Scrapy_Redis ----------
# Enables scheduling storing requests queue in redis.
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER = "scrapy_redis_bloomfilter.scheduler.Scheduler"

# Ensure all spiders share same duplicates filter through redis.
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
DUPEFILTER_CLASS = "scrapy_redis_bloomfilter.dupefilter.RFPDupeFilter"

# Don't cleanup redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = True

# Number of Hash Functions to use, defaults to 6
BLOOMFILTER_HASH_NUMBER = 6

# Redis Memory Bit of Bloomfilter Usage, 30 means 2^30 = 128MB, defaults to 30
BLOOMFILTER_BIT = 30




