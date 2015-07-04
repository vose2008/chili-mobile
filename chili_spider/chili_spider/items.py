# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class newsListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author = scrapy.Field()
    author_link = scrapy.Field()
    title = scrapy.Field()
    title_link = scrapy.Field()
    reply = scrapy.Field()
    hits = scrapy.Field()
    lastreply_time = scrapy.Field()
    lastreply_author = scrapy.Field()
    
class newsContentItem(scrapy.Item):
    content_author = scrapy.Field()
    content_text = scrapy.Field()
