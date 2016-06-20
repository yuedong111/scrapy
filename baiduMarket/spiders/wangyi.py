# -*- coding: UTF-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from baiduMarket.items import BaidumarketItem

class WangyiSpider(CrawlSpider):
    name = 'wangyi'
    allowed_domains = ['m.163.com']
    start_urls = [
        'http://m.163.com/android/game/allgame/index.html',
        'http://m.163.com/android/category/allapp/index.html',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=['/android/software/[a-zA-Z0-9]+.html']),callback='parse_item',follow=False),
        Rule(SgmlLinkExtractor(allow=['/android/game/[a-zA-Z0-9]+/index.html']), callback='noapk', follow=True),
        Rule(SgmlLinkExtractor(allow=['/android/category/[a-zA-Z0-9]+/index.html']),callback='noapk',follow=True),
    )

    def noapk(self, response):
        print 'No apk: ', response.url

    def parse_item(self, response):

        print 'There is a new apk: ', response.url

        hxs = HtmlXPathSelector(response)
        i = BaidumarketItem()

        i['app_name'] = "".join(hxs.select('//span[@class="f-h1"]/text()').extract())

        i['app_keywords'] = "".join(hxs.select('//meta[@name="Keywords"]/@content').extract())

        i['app_url'] = response.url

        i['app_icon_url'] = "".join(hxs.select('//div[@class="t-c p-t20"]/span/img/@src').extract())

#       i['icon_context'] = "".join(hxs.select().extract())

        i['app_size'] = "".join(hxs.select('//table[@class="table-appinfo"]/tr[2]/td[1]/text()').extract())

        i['app_version'] = "".join(hxs.select('//table[@class="table-appinfo"]/tr[3]/td/text()').extract()) 

        i['app_author'] = "".join(hxs.select('//table[@class="table-appinfo"]/tr[4]/td/text()').extract())

        i['download_times'] = "0"

        i['download_url'] = "".join(hxs.select('//div[@class="t-c p-t20"]/p[1]/a/@href').extract())

        tmp = "".join(hxs.select('//div[@class="crumb"]/a[1]/text()').extract()) 
        i['os_version'] = tmp.strip()[:-2]

        i['app_description'] = "".join(hxs.select('//div[@class="f14px download-app-desc"]/text()').extract())

        i['last_update_date'] = '1990-01-01'

        i['app_class'] = "".join(hxs.select('//a[@class="a-s2"]/text()').extract())

        i['app_market'] =  u'网易应用中心'   

        i['market_site'] = 'm.163.com'        

        tmp = "".join(hxs.select('//div[@class="fl-l m-r15"]/span[1]/i/@style').extract())[6:-1]
        i['user_rate'] = str(float(tmp)/10)       

        i['comments_num'] = "".join(hxs.select('//div[@class="m-t5 clearfix"]/div[2]/span[2]/text()').extract())[1:-1]

        return i
