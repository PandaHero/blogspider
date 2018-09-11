# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyblogItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 文件名
    url = scrapy.Field()  # 链接
    # description = scrapy.Field()  # 简介
    author = scrapy.Field()  # 作者
    publish = scrapy.Field()  # 发布时间
    readers = scrapy.Field()  # 阅读数
    comments = scrapy.Field()  # 评论数
