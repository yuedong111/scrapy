# -*- coding: UTF-8 -*-
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from baiduMarket.items import BaidumarketItem

class A3533Spider(CrawlSpider):
    name = 'world3533'
    allowed_domains = ['a.3533.com']

    start_urls = [
      'http://a.3533.com/youxi/',
      'http://a.3533.com/ruanjian/',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow = ['/game/\d+/']), callback = 'parse_item', follow = False),
        Rule(SgmlLinkExtractor(allow = ['/ruanjian/\d+\.htm']), callback = 'parse_item', follow = False),
        Rule(SgmlLinkExtractor(allow = ['/youxi/\d+/(\d+\.htm)*']), callback = 'noapk', follow = True),
        Rule(SgmlLinkExtractor(allow = ['/ruanjian/\d+/(\d+\.htm)*']), callback = 'noapk', follow = True), 
    )

    def noapk(self, response):
        print 'No apk: ', response.url

    def parse_item(self, response):

        print 'There is a new apk: ',response.url

        hxs = HtmlXPathSelector(response)
        i = BaidumarketItem()

        i['app_name'] = ''.join(hxs.select('/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/h1/text()').extract())

        i['app_keywords'] = 'None'

        i['app_url'] = response.url

        i['app_icon_url'] = ''.join(hxs.select('/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/img/@src').extract())

#i['icon_content'] =  
        
        i['app_size'] = ''.join(hxs.select('/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[3]/a/span[2]/text()').extract())
 
        i['app_version'] = ''.join(hxs.select('/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/p/text()').extract())

        i['download_times'] = '0'

        i['download_url'] = ''.join(hxs.select('/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[3]/a/@href').extract())  

        i['app_author'] =  ' None'

        i['os_version'] = 'None'
        i['app_description'] = ''.join(hxs.select('/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div[2]/p[2]/text()').extract())  

        i['last_update_date'] =  '1990-01-01'

        i['app_class'] = ''.join(hxs.select('//div[@class="gameinfos"]/ul[1]/li[1]/a[1]/text()').extract())  

        i['app_market'] = u'手机世界3533'

        i['market_site'] = 'a.3533.com'

        i['user_rate'] = ''.join(hxs.select('//div[@class="gameinfos"]/p[1]/img/@src').extract())[-5:][:1]
 
        i['comments_num'] = '0'

        print i
        return i

