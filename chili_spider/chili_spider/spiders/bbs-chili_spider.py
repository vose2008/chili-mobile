# -*- coding:utf-8 -*-
import scrapy
from chili_spider.items import newsListItem

class chiliSpider(scrapy.Spider):
    name = "bbs"
    allowed_domains = ["e658.cn"]
    start_urls = [
        "http://www.e658.cn/bbs/",
    ]

    def parse(self, response):
        handledData = response.xpath("//*[@id='main']/table/tr[2]/td[2]/table/tr")
        for sel in handledData:
            item = newsListItem()
            try:
                item['author'] = sel.xpath("td[contains(@class, 'author')]/a/text()").extract()[0]
            except IndexError:
                continue
            else:
                pass
            item['author_link'] = sel.xpath("td[contains(@class, 'author')]/a/@href").extract()[0]
            item['title'] = sel.xpath("td[contains(@class, 'title')]//a/text()").extract()[0]
            item['title_link'] = sel.xpath("td[contains(@class, 'title')]//a/@href").extract()[0]
            item['reply'] = sel.xpath("td[contains(@class, 'reply')]/text()").extract()[0]
            item['hits'] = sel.xpath("td[contains(@class, 'hits')]/text()").extract()[0]
            item['lastreply_time'] = sel.xpath("td[contains(@class, 'lastreply')]/span[1]/text()").extract()[0]
            item['lastreply_author'] = sel.xpath("td[contains(@class, 'lastreply')]/a//text()").extract()[0]
            #中文输出
            print item['title'].encode("utf-8")
            yield item
