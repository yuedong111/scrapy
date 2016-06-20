# Scrapy settings for baiduMarket project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'baiduMarket'

SPIDER_MODULES = ['baiduMarket.spiders']
NEWSPIDER_MODULE = 'baiduMarket.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'

#ITEM_PIPELINES = ['baiduMarket.pipelines.BaidumarketPipeline']
ITEM_PIPELINES = ['baiduMarket.pipelines1.BaidumarketPipeline']

#DOWNLOADER_MIDDLEWARES={
#'baiduMarket.webkitdownloader.WebkitDownloader': 555,
#}

LOG_LEVEL = 'ERROR'
LOG_FILE = 'baiduMarket.log'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'baiduMarket (+http://www.yourdomain.com)'
