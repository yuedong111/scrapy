# -*- coding: UTF-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from baiduMarket.items import BaidumarketItem

import string

class SogouSpider(CrawlSpider):
    name = 'sogou'
    allowed_domains = ['app.sogou.com']

    start_urls = [
        'http://app.sogou.com/game',
        'http://app.sogou.com/soft',
    ]

    rules = (
        Rule(SgmlLinkExtractor(allow=['/detail/\d+']), callback = 'parse_item', follow = False),
        Rule(SgmlLinkExtractor(allow=['/game(/\d+)*/\d+(#golisttop)*']), callback = 'noapk', follow = True),
        Rule(SgmlLinkExtractor(allow=['/soft(/\d+)*/\d+(#golisttop)*']), callback = 'noapk', follow = True),

    )

    def noapk(self, response):
        print 'No apk: ',response.url

    def parse_item(self, response):

        print 'There is a new apk: ', response.url

        hxs = HtmlXPathSelector(response)
        i = BaidumarketItem()

        i['app_name'] = "".join(hxs.select('//em[@class="title cf"]/@title').extract())

        i['app_keywords'] = "".join(hxs.select('//meta[@name="keywords"]/@content').extract())

        i['app_url'] = response.url

        i['app_icon_url'] = "".join(hxs.select('//div[@class="pic"]/a/img/@data-original').extract())

#        icon_content = Field()
 
        i['app_size'] = "".join(hxs.select('//ul[@class="dd cf"]/li[3]/text()').extract())[3:]

        i['app_version'] = "".join(hxs.select('//ul[@class="dd cf"]/li[4]/text()').extract())[3:]

        i['download_times'] = "".join(hxs.select('//ul[@class="dd cf"]/li[1]/text()').extract())[4:]

        i['download_url'] = "".join(hxs.select(u'//div[@pbflag="wc_0_下载到电脑"]/a/@href').extract())

        i['app_author'] = "".join(hxs.select('//ul[@class="dd cf"]/li[6]/@title').extract())

        i['os_version'] = "".join(hxs.select('//ul[@class="dd cf"]/li[5]/text()').extract())[5:]

        i['app_description'] = "".join(hxs.select('//p[@id="detail_content_more"]/text()').extract())

        i['last_update_date'] = "".join(hxs.select('//ul[@class="dd cf"]/li[2]/text()').extract())[5:]

        i['app_class'] = "".join(hxs.select('//div[@class="sub_nav cf"]/a[3]/text()').extract())

        i['app_market'] = u"搜狗市场"

        i['market_site'] = "app.sogou.com"

        i['user_rate'] =  "".join(hxs.select('//div[@class="star_min"]/em/text()').extract())
        if (i['user_rate'].find('.') != -1):
            tmp = i['user_rate'].find('.')
            i['user_rate'] = i['user_rate'][:tmp]
        if (i['user_rate'].encode('utf-8') == u'暂无'.encode('utf-8')):
            i['user_rate'] = '0'

        i['comments_num'] = "".join(hxs.select('//div[@class="dianping_r"]/div[1]/label[1]/em/text()').extract())
        print i 
        return i
