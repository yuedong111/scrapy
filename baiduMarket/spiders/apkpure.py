# -*- coding:UTF-8 -*-
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from baiduMarket.items import BaidumarketItem
import logging
class BaiduSpider(CrawlSpider):
    name='apkpure'
    download_delay=20
    allowed_domains=['apkpure.com']
    start_urls = [
        'https://apkpure.com/app',
        'https://apkpure.com/game',
        ]
        

    rules=(
        Rule(SgmlLinkExtractor(allow=['/.*?/(io|com|free|org).*']), callback = 'parse_item', follow = False),
        Rule(SgmlLinkExtractor(allow=['/app\?hl=en&page=\d+']), callback = 'noapk', follow = True),
        Rule(SgmlLinkExtractor(allow=['/game\?page=\d+']), callback = 'noapk', follow = True),
     
    )
    def noapk(self, response):
        print 'no apk: ', response.url
       
    def parse_item(self, response):
        print '> there is a new apk: ',response.url
        hxs = HtmlXPathSelector(response)
        i = BaidumarketItem()
        i['app_market'] = 'apkpure'    
        i['market_site'] = 'apkpure.com'
        i['app_name'] = "".join(hxs.select('/html/body/div[2]/div[2]/div[1]/dl/dd/div[1]/h1/text()').extract())
        i['app_keywords'] = "None"
        i['app_url'] = response.url
        print "response url:"+response.url
        i['app_icon_url'] = "".join(hxs.select('/html/body/div[2]/div[2]/div[1]/dl/dt/div/img/@src').extract())
        i['app_size'] = "".join(hxs.select('/html/body/div[2]/div[2]/div[1]/div[2]/a[1]/span[2]/text()').extract())
        print "app_size:"+i['app_size']
        i['app_version'] = "".join(hxs.select('/html/body/div[2]/div[2]/div[1]/dl/dd/ul/li[2]/p[2]/text()').extract())[3:]
        print "app_version:"+i['app_version']
        i['download_times'] = "".join(hxs.select('//div[@id="doc"]/div[2]/div/div[1]/div/div[2]/div[2]/span[3]/text()').extract())
        print "download_times:"+i['download_times']
        i['download_url'] = "".join(hxs.select('/html/body/div[2]/div[2]/div[1]/div[2]/a[1]/@href').extract())
        print "download url:"+ i['download_url']
        i['app_author'] = "".join(hxs.select('/html/body/div[2]/div[2]/div[1]/dl/dd/ul/li[1]/p[2]/a/span/text()').extract())
        i['os_version'] = "".join(hxs.select('/html/body/div[2]/div[2]/div[1]/div[7]/ul/li[3]/p[2]/text()').extract())
        i['app_description'] = "".join(hxs.select('//*[@id="describe"]/div/div[1]/text()[1]/text()').extract())
        i['app_class'] = "".join(hxs.select('/html/body/div[2]/div[2]/div[1]/div[1]/a[2]/text()').extract())
        i['user_rate'] = str(int(round(float("".join(response.xpath('/html/body/div[2]/div[2]/div[1]/dl/dd/div[3]/div[1]/span/@style').extract())[6:8]))/10))
        i['comments_num'] = "0"
        print i
        return i
