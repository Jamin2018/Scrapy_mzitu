# -*- coding: utf-8 -*-
import scrapy
import json
from meizituSpider.items import MeizituspiderItem

class ZhihuComSpider(scrapy.Spider):
    name = "meizitu"
    allowed_domains = ["meizitu.com",'mzitu.com']
    start_urls = (
        'http://www.mzitu.com/all/',
    )

    def parse(self, response):
        print '开始解析'
        datas = response.xpath(".//*[@class='all']")
        div = datas.xpath("div[@class='year']")
        for i in div:
            year =  i.xpath("text()").extract()[0]
            ps = i.xpath("following-sibling::ul[1]").xpath(".//li")
            for p in ps:
                month =  p.xpath(".//*[@class='month']/em/text()").extract()[0]
                urls =  p.xpath(".//*[@class='url']/a")
                for url in urls:
                    image_urls =  url.xpath("@href").extract()[0]
                    title = url.xpath('text()').extract()[0]
                    item = MeizituspiderItem(year = year, month = month, title = title, urls=image_urls)
                    request = scrapy.Request(url=image_urls, callback=self.parse_body)
                    request.meta['item'] = item
                    # yield item
                    yield request


    def parse_body(self, response):
        item = response.meta['item']
        body = response.xpath(".//*[@class='main-image']")
        try:
            l = item['image_urls']
            l.append(body.xpath('.//img//@src').extract()[0])
        except:
            item['image_urls'] = body.xpath('.//img//@src').extract()

        next_img = scrapy.Selector(response).re(u'<a href="(\S*)"><span>下一页»</span></a>')
        if next_img:
            request = scrapy.Request(url=next_img[0], callback=self.parse_body)
            request.meta['item'] = item
            yield request
        else:
            yield item
