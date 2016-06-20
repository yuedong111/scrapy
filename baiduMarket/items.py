# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BaidumarketItem(Item):
    # define the fields for your item here like:
    # name = Field()
    app_name = Field()
    app_keywords = Field()
    app_url = Field()
    app_icon_url = Field()
    icon_content = Field()
    app_size = Field()
    app_version = Field()
    download_times = Field()
    download_url = Field()
    app_author = Field()
    os_version = Field()
    app_description = Field()
    last_update_date = Field()
    app_class = Field()
    app_market = Field()
    market_site = Field()
    user_rate = Field()
    comments_num = Field()


