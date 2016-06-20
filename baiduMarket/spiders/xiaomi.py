# -*- coding: UTF-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from baiduMarket.items import BaidumarketItem

class XiaomiSpider(CrawlSpider):
    name = 'xiaomi'
    allowed_domains = ['app.mi.com']
    
    start_urls = [
        'http://app.mi.com'
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow = ['/detail/\d+']), callback='parse_item', follow= False),
        Rule(SgmlLinkExtractor(allow = ['/category/\d+']), callback = 'noapk', follow = True),
    )

    def noapk(self, response):
        print 'No apk: ', response.url


    def parse_item(self, response):

        print 'There is a new apk: ',response.url

        hxs = HtmlXPathSelector(response)
        i = BaidumarketItem()

        i['app_name'] = "".join(hxs.select('/html/body/div[3]/div[1]/div[2]/div[1]/div/h3/text()').extract())

        i['app_keywords'] = "".join(hxs.select('//meta[@name="keywords"]/@content').extract())
   
        i['app_url'] = response.url

        i['app_icon_url'] = "".join(hxs.select('/html/body/div[3]/div[1]/div[2]/div[1]/img/@src').extract())

#       icon_content = Field()
    
        i['app_size'] = "".join(hxs.select('/html/body/div[3]/div[1]/div[2]/div[2]/div/ul[1]/li[2]/text()').extract())

        i['app_version'] = "".join(hxs.select('/html/body/div[3]/div[1]/div[2]/div[2]/div/ul[1]/li[4]/text()').extract())
    
        i['download_times'] = '0'

        i['download_url'] = "http://app.mi.com" + "".join(hxs.select('/html/body/div[3]/div[1]/div[2]/div[1]/div/div[2]/a/@href').extract())
  
        i['app_author'] = "".join(hxs.select('/html/body/div[3]/div[1]/div[2]/div[1]/div/p[1]/text()').extract())

        i['os_version'] = "None"

        i['app_description'] = "".join(hxs.select('/html/body/div[3]/div[1]/div[4]/p/text()').extract())
        i['last_update_date'] = "".join(hxs.select('/html/body/div[3]/div[1]/div[2]/div[2]/div/ul[1]/li[6]/text()').extract())
   
        i['app_class'] = "".join(hxs.select('/html/body/div[3]/div[1]/div[2]/div[1]/div/p[2]/text()[1]').extract())

        i['app_market'] = u'小米应用商店'

        i['market_site'] = 'app.mi.com'

        i['user_rate'] = "".join(hxs.select('/html/body/div[3]/div[1]/div[2]/div[1]/div/div[1]/div/@class').extract())[18]

        i['comments_num'] = "".join(hxs.select('/html/body/div[3]/div[1]/div[2]/div[1]/div/span/text()').extract())[2:-5]
        print i
        return i
