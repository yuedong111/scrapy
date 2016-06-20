#-*- coding: UTF-8 -*-
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from baiduMarket.items import BaidumarketItem

class HuaweiSpider(CrawlSpider):
    name = 'huawei'
    allowed_domains = ['appstore.huawei.com']
    start_urls = ['http://appstore.huawei.com/soft/list',
                  'http://appstore.huawei.com/game/list',
                 ]

    rules = (
        Rule(SgmlLinkExtractor(allow=['app/C\d+[?a-z=&]*']), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(allow=['soft/list.*']), callback='noapk', follow=True),
        Rule(SgmlLinkExtractor(allow=['game/list.*']), callback='noapk', follow=True),
    )
   
    def noapk(self,response):
        print "> No apk url:",response.url

    def parse_item(self, response):
        print "There is a new apk:",response.url
        hxs = HtmlXPathSelector(response)
        i = BaidumarketItem()
        i["app_name"] = "".join(hxs.select('//div[@class="app-info flt"]/ul[1]/li[2]/p[1]/span[1]/text()').extract())
        i["app_keywords"] = "".join(hxs.select('//meta[@name="keywords"]/@content').extract())
        i['app_url'] = response.url
        i['app_icon_url'] = "".join(hxs.select('//div[@class="app-info flt"]/ul[@class="app-info-ul nofloat"]/li[@class="img"]/img/@src').extract())
        i['app_size'] = "".join(hxs.select('//div[@class="app-info flt"]/ul[2]/li[1]/span/text()').extract())
        i['app_version'] ="".join( hxs.select('//div[@class="app-info flt"]/ul[2]/li[4]/span/text()').extract())
        i['download_times'] ="".join(hxs.select('//div[@class="app-info flt"]/ul[1]/li[2]/p[1]/span[2]/text()').extract()[2:])
        i['download_url'] = "".join(hxs.select('//div[@class="app-function nofloat"]/a[@class="mkapp-btn mab-install"]/@dlurl').extract())
        print '> special download_url: ', i['download_url']
        i['app_author'] ="".join(hxs.select('//div[@class="app-info flt"]/ul[2]/li[3]/span/@title').extract())
        i['os_version'] = u"支持固件：2.3以上"
        i['app_description'] ="".join(hxs.select('//div[@class="content"]/div[@id="app_strdesc"]/text()').extract())
        i['last_update_date'] ="".join(hxs.select('//div[@class="app-info flt"]/ul[2]/li[2]/span/text()').extract())
        i['app_class'] = hxs.select('//div[@class="unit-locate"]/a/text()').extract()
        i['app_market'] =  u"华为应用市场"
        i['market_site'] = 'appstore.huawei.com'
        temp = "".join(hxs.select('//div[@class="app-info flt"]/ul[@class="app-info-ul nofloat"]/li[2]/p[2]/span/@class').extract())[6:]
    	i['user_rate']=float(temp)/2
        try:
            comments = "".join(hxs.select('//h4[@class="sub nofloat"]/span/text()').extract())
            i['comments_num'] = comments.replace(" ","")[-8:-1]
        except:
            i['comments_num'] = "0"
    	print i
        return i
