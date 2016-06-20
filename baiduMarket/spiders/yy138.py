# -*- coding:UTF-8 -*-
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from baiduMarket.items import BaidumarketItem

class Yy138Spider(CrawlSpider):
    name = 'yy138'
    
    allowed_domains = ['www.yy138.com']
    
    start_urls = [
      'http://www.yy138.com/android/youxi/',
      'http://www.yy138.com/android/ruanjian/',
      'http://www.yy138.com/wangyou/',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow = ['/[a-zA-Z][a-zA-Z0-9]*/']), callback = 'parse_item', follow = False),
        
        Rule(SgmlLinkExtractor(allow = ['/wangyou/']), callback = 'noapk', follow = True),
        Rule(SgmlLinkExtractor(allow = ['/\d+/(\d+\.html)*']), callback = 'noapk', follow = True), 
        Rule(SgmlLinkExtractor(allow = ['/wangyou/zuixin/(\d+\.html)*']), callback = 'noapk', follow = True),
        
        Rule(SgmlLinkExtractor(allow = ['/youxi/']), callback = 'noapk', follow = True), 
        Rule(SgmlLinkExtractor(allow = ['/youxi/zuixin/(\d+\.html)*']), callback = 'noapk', follow = True),

        Rule(SgmlLinkExtractor(allow = ['/ruanjian/']), callback = 'noapk', follow = True),
        Rule(SgmlLinkExtractor(allow = ['/ruanjian/zuixin/(\d+\.html)*']), callback = 'noapk', follow = True),
    )

    def noapk(self, response):
        print 'No apk: ', response.url    
   
    def parse_item(self, response):

        print 'There is a new apk: ',response.url
        
        hxs = HtmlXPathSelector(response)
        i = BaidumarketItem()
        print 'begin:'
        try:
        #    print '.....'

            i['app_name'] = ''.join(hxs.select('//div[@class="column download"]/div[1]/h1[1]/text()').extract())

            i['app_keywords'] = ''.join(hxs.select('//div[@class="intro"]/p[3]/a/text()').extract())

 
            i['app_url'] = response.url

            i['app_icon_url'] = ''.join(hxs.select('//div[@class="icon"]/img/@src').extract())
#            print 'zhongduan'
#i['icon_content'] =  
        
            i['app_size'] = ''.join(hxs.select('//*[@id="xiazai"]/div/div[2]/div[2]/div/div/div[1]/div/a/span/text()').extract())
            if i['app_size'] =="":
                 i['app_size'] = ''.join(hxs.select('//*[@id="xiazai"]/div/div/div[2]/div/div/div[1]/div/a/span/text()').extract()) 
            i['app_version'] = ''.join(hxs.select('//*[@id="xiazai"]/div/div[2]/div[2]/div/div/div[1]/p/text()[2]').extract())[5:]
            if i['app_version'] == "":
                 i['app_version'] = ''.join(hxs.select('//*[@id="xiazai"]/div/div/div[2]/div/div/div[1]/p/text()[2]').extract())[5:]

            i['download_times'] = '0'

            i['download_url'] = ''.join(hxs.select('//*[@id="xiazai"]/div/div[2]/div[2]/div/div/div[1]/div/a/@href').extract())
            if i['download_url']=='':
                i['download_url']=''.join(hxs.select('//*[@id="xiazai"]/div/div/div[2]/div/div/div[1]/div/a/@href').extract())

            i['app_author'] =  'None'

            i['os_version'] = ''.join(hxs.select('//*[@id="xiazai"]/div/div[2]/div[2]/div/div/div[1]/p/text()[3]').extract())[5:]

            i['app_description'] = ''.join(hxs.select('//div[@class="column introduction"]/div[2]/p/text()').extract())

            if i['app_description'] == '':
                i['app_description'] = ''.join(hxs.select('//div[@class="column introduction"]/div[2]/text()').extract())

            i['last_update_date'] =  '1990-01-01'

            i['app_class'] = ''.join(hxs.select('//div[@class="intro"]/p[2]/a[2]/text()').extract())

      

            i['app_market'] = u'yy138.com'

            i['market_site'] = 'www.yy138.com'

            i['user_rate'] = ''.join(hxs.select('//div[@class="intro"]/p[1]/span[1]/span/@class').extract())[4]
 
            i['comments_num'] = '0'
            print i

            return i
      
        except Exception, e:

            print e


