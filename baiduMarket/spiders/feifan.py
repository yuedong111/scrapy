from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from baiduMarket.items import BaidumarketItem
import time
class FeifanSpider(CrawlSpider):
    name = 'feifan'
    allowed_domains = ['android.crsky.com']
    start_urls = ['http://android.crsky.com/app/','http://android.crsky.com/game/']

    rules = (

    Rule(SgmlLinkExtractor(allow=['android.crsky.com/app/index_\d+.html']), follow = True),
        Rule(SgmlLinkExtractor(allow=['android.crsky.com/game/index_\d+.html']), follow = True),
        Rule(SgmlLinkExtractor(allow=['android.crsky.com/soft/\d+.html']),callback='parse_item', follow = True),
    
    )


    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        i = BaidumarketItem()
        
        i['app_market'] = u'feifan'
        i['market_site'] = 'android.crsky.com'
        i['app_name']="".join(hxs.select("//div[@class='left']/div[@class='s_line'][1]/p/span/text()").extract())
        i['app_keywords'] = "".join(hxs.select('//meta[@name="Keywords"]/@content').extract())
        i['last_update_date']= "".join(hxs.select("//div[@class='s_line'][3]/p[3]/span/text()").extract())
        i['app_url'] = response.url
        i['app_icon_url'] = "".join(hxs.select("//div[@class='logo_ico']/div[@class='logo']/img/@src").extract())
        i['app_size']  = "".join(hxs.select("//div[@class='left']/div[@class='s_line'][2]/p[2]/span/text()").extract())
        i['app_version']  = "none"
        i['download_times']  = "".join(hxs.select("//div[@class='s_line'][3]/p[2]/span[@id='showtj']/text()").extract())
        i['download_url']  = "".join(hxs.select("//div[@class='down']/div[@class='btns']/ul[2]/li[1]/a/@href").extract())
        i['app_author'] = "".join(hxs.select("//div[@class='s_line'][2]/p[1]/span/a/span/text()").extract())
        i['os_version'] = "".join(hxs.select("//div[@class='left']/div[@class='s_line'][4]/p/text()").extract())
        i['app_description'] = "".join(hxs.select("//div[@id='conText']/div[@id='rom_des']/text()").extract())
        i['app_class'] = "".join(hxs.select("//div[@class='s_line'][3]/p[1]/span/a/text()").extract())
        i['comments_num'] = "0"
        i['user_rate'] = "0"
        try:
            i['os_version']=i['os_version'][5:]
        except Exception,e:
            i['os_version']=""
        try:
            i['app_description']=i['app_description'].strip()
        except Exception,e:
            i['app_description']=""
        print i
        return i

