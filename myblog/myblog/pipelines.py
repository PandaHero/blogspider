# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class MyblogPipeline(object):
    def __init__(self):
        self.client = pymysql.Connect(
            host="127.0.0.1",
            user="root",
            passwd="root",
            db="test1"
        )
        self.cur = self.client.cursor()

    def process_item(self, item, spider):
        sql = "insert into myblog(name,url,author,publish,readers,comments) values(%s,%s,%s,%s,%s,%s)"
        data = (item["name"], item["url"], item["author"], item["publish"], item["readers"], item["comments"],)
        self.cur.execute(sql, data)
        self.client.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.client.close()
