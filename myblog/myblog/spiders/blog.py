# -*- coding: utf-8 -*-
import scrapy
import re
import urllib.request
from ..items import MyblogItem


class BlogSpider(scrapy.Spider):
    name = 'blog'
    allowed_domains = ['blog.hexun.com']
    # start_urls = ['http://fjrs168.blog.hexun.com/']
    # 设置要爬取用户的uid，为后续构造爬去网站准备
    uid = "19940007"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}

    def start_requests(self):
        # 首次爬取模拟浏览器进行
        yield scrapy.Request("http://" + str(self.uid) + ".blog.hexun.com/p1/default.html", headers=self.headers
                             )

    def parse(self, response):
        articles = response.xpath('//div[@id="DefaultContainer1_ArticleList_Panel1"]/div[@class="Article"]')
        # print(articles)
        temp = 0
        # 正则匹配阅读数和点击数网址
        pattern = '<script type="text/javascript" src="(http://click.tool.hexun.com/.*?)">'
        hcurl = re.compile(pattern).findall(str(response.body))[0]
        # print(hcurl)
        opener = urllib.request.build_opener()
        opener.addheaders = [("User-Agent", str(self.headers.values()))]
        # 将opener安装为全局
        urllib.request.install_opener(opener=opener)
        # 发送请求
        data = urllib.request.urlopen(hcurl).read()
        # print(data)
        # 提取文章中阅读数的正则表达式
        click_part = "click\d*?','(\d*?)'"
        hits = re.compile(click_part).findall(str(data))
        # 提取文章中评论数的正则表达式
        comment_part = "comment\d*?','(\d*?)'"
        comments = re.compile(comment_part).findall(str(data))
        # print(hits, comments)
        author = response.xpath('//head/title/text()').extract()[0].split("-")[0].strip().replace("\r\n", "")
        # 页面总数
        page_nums = int(response.xpath(
            '//*[@id="DefaultContainer1_ArticleList_Panel1"]/div[11]/div[1]/a[5]/text()').extract()[0])
        # print(page_nums)
        for data in articles:
            item = MyblogItem()
            item["name"] = data.xpath("div/span[@class='ArticleTitleText']/a/text()").extract()[0].strip().replace(
                "\r\n", "")
            item["url"] = data.xpath("div/span[@class='ArticleTitleText']/a/@href").extract()[0].strip().replace("\r\n",
                                                                                                                 "")
            # item["description"] = data.xpath("div[2]/div[1]/text()").extract()[0].strip().replace("\r\n", "")
            item["author"] = author
            item["publish"] = " ".join(
                data.xpath("div[1]/text()").extract()[0].strip().replace("\r\n", "").split(" ")[-2:]).replace("]", "")
            # print(item)
            item["readers"] = hits[temp]
            item["comments"] = comments[temp]
            temp += 1
            yield item
        if page_nums > 1:
            for num in range(2, page_nums + 1):
                next_page_url = "http://" + str(self.uid) + ".blog.hexun.com/p" + str(num) + "/default.html"
                yield scrapy.Request(url=next_page_url, callback=self.parse, headers=self.headers)

        else:
            pass
