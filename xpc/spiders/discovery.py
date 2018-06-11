# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

class DiscoverySpider(scrapy.Spider):
    name = 'discovery'
    allowed_domains = ['www.xinpianchang.com']
    start_urls = ['http://www.xinpianchang.com/channel/index/sort-like']

    def parse(self, response):
        post_url = 'http://www.xinpianchang.com/a%s?from=ArticleList'
        post_list = response.xpath(
            '//ul[@class="video-list"]/li')
        for post in post_list:
            pid = post.xpath('./@data-articleid').get()
            request = Request(post_url % pid, callback=self.parse_post)
            request.meta['thumbnail'] = post.xpath('./a/img/@_src').get()
            request.meta['pid'] = pid
            request.meta['duration'] = post.xpath(
                './/span[contains(@class,"duration")]/text()').get()
            yield request
    def parse_post(self, response):
        # print(response.text)
        post = {}
        post['pid'] = response.meta['pid']
        post['thumbnail'] = response.meta['thumbnail']
        post['duration'] = response.meta['duration']
        post['video'] = response.xpath('//video[@id="xpc_video"]/@src').get()
        post['preview'] = response.xpath(
            '//div[@class="filmplay"]//img/@src').extract_first()
        post['title'] = response.xpath('//div[@class="title-wrap"]/h3/text()').extract_first()
        cates = response.xpath('//span[contains(@class,"cate")]/a/text()').extract()
        post['category'] = "-".join(cates).replace('\t', '').replace('\n', '')
        post['created_at'] = response.xpath(
            '//span[contains(@class,"update-time")]/i/text()').get()
        post['play_counts'] = response.xpath(
            '//i[contains(@class, "play-counts")]/@data-curplaycounts').get()
        post['like_counts'] = response.xpath(
            '//span[contains(@class, "like-counts")]/@data-counts').get()
        yield post

        creator_list = response.xpath(
            '//div[contains(@class,"filmplay-creator right-section")]//ul/li')
        url = 'http://www.xinpianchang.com/u%s?from=articleList'
        for creator in creator_list:
            cid = creator.xpath('./a/@data-userid').get()
            request = Request(url % cid, callback=self.parse_composer)
            request.meta['cid'] =cid
            yield request
    def parse_composer(self, response):
        composer = {}
        composer['cid'] = response.meta['cid']
        composer['banner'] = response.xpath(
            '//div[@class="banner-wrap"]/@style').get()[21: -1]
        composer['avatar'] = response.xpath('//span[@class="avator-wrap-s"]/img/@src').get()
        composer['name'] = response.xpath('//p[contains(@class, "creator-name")]/text()').get()
        composer['intro'] = response.xpath('//p[contains(@class, "creator-desc")]/text()').get()
        composer['like_counts'] = response.xpath('//span[contains(@class, "like-counts")]/text()').get()
        composer['fans_counts'] = response.xpath('//span[contains(@class, "fans-counts")]/text()').get()
        composer['follow_counts'] = response.xpath('//span[@class="fw_600 v-center"]/text()').get()
        composer['location'] = response.xpath('//span[contains(@class, "icon-location")]/following-sibling::span[1]/text()').get()
        composer['career'] = response.xpath('//span[contains(@class, "icon-career")]/following-sibling::span[1]/text()').get()
        yield composer