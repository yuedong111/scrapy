from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from baiduMarket.items import BaidumarketItem

class Mobile1Spider(CrawlSpider):
    name = 'mobile1'

    allowed_domains = ['www.1mobile.com']

    start_urls = [
        'http://www.1mobile.com/downloads/',
        'http://www.1mobile.com/pick/',
        'http://www.1mobile.com/update/',
        'http://www.1mobile.com/apps/',
        'http://www.1mobile.com/games/',
    ]
    
    rules = (
        Rule(SgmlLinkExtractor(allow = ['/[a-zA-Z-\.]*\d+.html']), callback = 'parse_item', follow = True),
        Rule(SgmlLinkExtractor(allow = ['/downloads/[a-zA-Z_]*/*[a-zA-Z_]*/*(\d+\.html)*']), callback = 'noapk', follow = True),
        Rule(SgmlLinkExtractor(allow = ['/pick/[a-zA-Z_]*/*(\d+\.html)*']), callback = 'noapk', follow = True),
        Rule(SgmlLinkExtractor(allow = ['/apps/[a-zA-Z_]*/*(\d+\.html)*']), callback = 'noapk', follow = True),
        Rule(SgmlLinkExtractor(allow = ['/games/[a-zA-Z_]*/*(\d+\.html)*']), callback = 'noapk', follow = True),
    )

    def noapk(self, response):
        print 'Not apk url: ', response.url


    def parse_item(self, response):

        print 'There is a apk url: ', response.url

        hxs = HtmlXPathSelector(response)
        i = BaidumarketItem()
        
        i['app_name'] = "".join(hxs.select('//div[@class="detailitem mb10"]/h1/text()').extract())

        i['app_keywords'] = "".join(hxs.select('//meta[@name="keywords"]/@content').extract())

        i['app_url'] = response.url

        i['app_icon_url'] = "".join(hxs.select('//div[@class="appdown"]/div[1]/img/@src').extract())

#       i['icon_content'] = "".join(hxs.select().extract())

        i['app_size'] = "".join(hxs.select('//div[@class="appinfo"]/dl/dd[4]/text()').extract())

        i['app_version'] = "".join(hxs.select('//div[@class="appinfo"]/dl/dd[3]/text()').extract())

        i['download_times'] = "".join(hxs.select('//div[@class="appinfo"]/dl/dd[6]/text()').extract())

        tmp = "".join(hxs.select('//span[@class="downbtnbox"]/a[1]/@onclick').extract())[13:-21]
        i['download_url'] = 'http://package.1mobile.com/d.php?pkg=' + tmp + '&channel=304'
        print '> special download_url: ', i['download_url']

        i['app_author'] = 'chenyi_say_None'

        i['os_version'] = "".join(hxs.select('//div[@class="appinfo"]/dl/dd[5]/text()').extract())

        i['app_description'] = "".join(hxs.select('//div[@class="allinfo"]/text()').extract())

        i['last_update_date'] = "".join(hxs.select('//div[@class="appinfo"]/dl/dd[2]/text()').extract())

        i['app_class'] = "".join(hxs.select('//div[@class="appinfo"]/dl/dd[1]/a/text()').extract())
        
        i['app_market'] = '1mobile'

        i['market_site'] = 'www.1mobile.com'

        i['user_rate'] = '0'

        i['comments_num'] = '0'

        return i
