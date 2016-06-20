from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from baiduMarket.items import BaidumarketItem
import logging
class BaiduSpider(CrawlSpider):
    name = 'baidu'
    allowed_domains = ['shouji.baidu.com']
    start_urls = [
        'http://shouji.baidu.com/software/?from=as',
        'http://shouji.baidu.com/game/?from=as',
    ]     
         
    rules = (
        Rule(SgmlLinkExtractor(allow=['/(game|software)/item\?docid=\d+&.*']), callback = 'parse_item', follow = False),
        Rule(SgmlLinkExtractor(allow=['/software/list\?cid=\d+&.*']), callback = 'noapk', follow = True),
        Rule(SgmlLinkExtractor(allow=['/game/list\?cid=\d+&.*']), callback = 'noapk', follow = True),
        Rule(SgmlLinkExtractor(allow=['/(game|software)/topic\?tid=\d+&.*']), callback = 'noapk', follow = True),
    ) 
    def noapk(self, response):
        print 'no apk: ', response.url
       
    def parse_item(self, response):
        print '> there is a new apk: ',response.url
        hxs = HtmlXPathSelector(response)
        i = BaidumarketItem()
        i['app_market'] = 'Baidu_Market'    
        i['market_site'] = 'shouji.baidu.com'
        i['app_name'] = "".join(hxs.select('//div[@id="doc"]/div[2]/div/div[1]/div/div[2]/h1/span/text()').extract())
        i['app_keywords'] = "".join(hxs.select('//meta[@name="keywords"]/@content').extract())
        i['app_url'] = response.url
        print "response url:"+response.url
        i['app_icon_url'] = "".join(hxs.select('//div[@id="doc"]/div[2]/div/div[1]/div/div[1]/div/img/@src').extract())
        i['app_size'] = "".join(hxs.select('//div[@id="doc"]/div[2]/div/div[1]/div/div[2]/div[2]/span[1]/text()').extract())[3:]
        print "app_size:"+i['app_size']
        i['app_version'] = "".join(hxs.select('//div[@id="doc"]/div[2]/div/div[1]/div/div[2]/div[2]/span[2]/text()').extract())[3:]
        print "app_version:"+i['app_version']
        i['download_times'] = "".join(hxs.select('//div[@id="doc"]/div[2]/div/div[1]/div/div[2]/div[2]/span[3]/text()').extract())
        print "download_times:"+i['download_times']
        i['download_url'] = "".join(hxs.select('//div[@id="doc"]/div[2]/div/div[1]/div/div[4]/a/@href').extract())
        print "download url:"+ i['download_url']
        i['app_author'] = "".join(hxs.select('///div[@id="doc"]/div[2]/div/div[1]/div/div[2]/div[2]/div/span[2]/span[2]/text()').extract())
        i['os_version'] = "".join(hxs.select('//div[@class="com"]/div[@class="info-top"]/dl/dd[@class="info-params"]/table/tbody/tr/td/span[@class="params-platform"]/text()').extract())
        i['app_description'] = "".join(hxs.select('//div[@id="doc"]/div[2]/div/div[2]/div[3]/div[2]/div[2]/p/text()').extract())
        i['last_update_date'] = "".join(hxs.select('//div[@class="com"]/div[@class="info-top"]/dl/dd[@class="info-params"]/table/tbody/tr/td/span[@class="params-updatetime"]/text()').extract())
        i['app_class'] = "".join(hxs.select('//div[@class="content-main-border content-intro"]/div[@class="data-tabcon params-con"]/table/tbody/tr/td/span[@class="params-catename"]/text()').extract())
        i['user_rate'] = str(int(round(float("".join(response.xpath('//div[@id="doc"]/div[2]/div/div[1]/div/div[2]/div[1]/span[1]/span/@style').extract())[6:8]))/10))
        i['comments_num'] = "0"
        print i
        return i

