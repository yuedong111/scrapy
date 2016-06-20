# -*- coding:UTF-8 -*-

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from baiduMarket.items import BaidumarketItem

import string

class HiapkSpider(CrawlSpider):
    name = 'hiapk'
    allowed_domains = ['apk.hiapk.com']

    start_urls = [
        'http://apk.hiapk.com/games',
        'http://apk.hiapk.com/apps',
    ]

#    rules = (
#        Rule(SgmlLinkExtractor(allow = ['.*']), callback = 'noapk', follow = True),
#        Rule(SgmlLinkExtractor(allow = ['/appinfo/.*']), callback = 'parse_item', follow = True),

#        Rule(SgmlLinkExtractor(allow = ['/appinfo/[a-zA-Z][a-zA-Z\.]*']), callback = 'parse_item', follow = True),
#        Rule(SgmlLinkExtractor(allow = ['/appinfo/[a-zA-Z][a-zA-Z\.]*/\d+']), callback = 'parse_item', follow = True),
        #Rule(SgmlLinkExtractor(allow = ['/apps.*']), callback = 'noapk', follow = True),
        #Rule(SgmlLinkExtractor(allow = ['/games.*']), callback = 'noapk', follow = True),
#    )

    rules = (
        Rule(SgmlLinkExtractor(allow=['/appinfo/[a-zA-Z][a-zA-Z\.]*']), callback = 'parse_item', follow = True)
,
        Rule(SgmlLinkExtractor(allow=['/appinfo/[a-zA-Z][a-zA-Z\.]*/\d+']), callback = 'parse_item', follow = True),
        Rule(SgmlLinkExtractor(allow=['/apps.*']), callback = 'noapk', follow = True),
        Rule(SgmlLinkExtractor(allow=['/games.*']), callback = 'noapk', follow = True),
    )



    def noapk(self, response):
        print '> No apk url: ', response.url


    def parse_item(self, response):

        print '> there is a apk url:', response.url

        hxs = HtmlXPathSelector(response)
        i = BaidumarketItem()

        i['app_market'] = 'hiapk_Market'

        i['market_site'] = 'apk.hiapk.com'


        tmp = "".join(hxs.select('//div[@id="appSoftName"]/text()').extract())

        dirty_ch = [' ', '\n']
        for ch in dirty_ch:
            tmp = tmp.replace(ch, '')
        
        pos = tmp.find('(')
        if (pos == -1):
            i['app_name'] = tmp
            i['app_version'] = '0'
        else:
            i['app_name'] = tmp[:pos]
            i['app_version'] = tmp[pos+1:-1]

        
        i['app_keywords'] = "".join(hxs.select('//meta[@name="keywords"]/@content').extract())

        i['app_url'] = response.url

        i['app_icon_url'] = "".join(hxs.select('//div[@class="detail_content"]/div[@class="left"]/img/@src').extract())

        i['app_size'] = "".join(hxs.select('//div[@class="detail_right"]/div[@class="code_box_border"]/div[4]/span[@id="appSize"]/text()').extract())


        tmp = "".join(hxs.select('//div[@class="detail_right"]/div[@class="code_box_border"]/div[3]/span[2]/text()').extract())[:-2]

        if (tmp.find(u'小') != -1):
            tmp = tmp[2:]
       
        i['download_times'] = tmp


        tmp = "".join(hxs.select('//div[@class="detail_right"]/div[@class="code_box_border"]/div[10]/a/@href').extract())

        i['download_url'] = 'http://apk.hiapk.com' + tmp


        i['app_author'] = "".join(hxs.select('//div[@class="detail_right"]/div[@class="code_box_border"]/div[2]/span[2]/text()').extract())

        i['os_version'] = "".join(hxs.select('//div[@class="detail_right"]/div[@class="code_box_border"]/div[7]/span[2]/text()').extract())

        i['app_description'] = "".join(hxs.select('//pre[@id="softIntroduce"]/text()').extract())

        i['last_update_date'] = "".join(hxs.select('//div[@class="detail_right"]/div[@class="code_box_border"]/div[9]/span[2]/text()').extract())

        i['app_class'] = "".join(hxs.select('//div[@class="detail_right"]/div[@class="code_box_border"]/div[5]/span[2]/a/span/text()').extract())

        tmp = "".join(hxs.select('//div[@class="star_tip_div left"]/div[@class="star_num"]/text()').extract())

        for ch in dirty_ch:
            tmp = tmp.replace(ch, '')

        i['user_rate'] = str(int(round(float(tmp))))

        i['comments_num'] = "".join(hxs.select('//span[@id="startCount"]/text()').extract())
        
        return i
