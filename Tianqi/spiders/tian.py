# -*- coding: utf-8 -*-
import scrapy
from Tianqi.items import TianqiItem
import time
# 改造爬虫导包
from scrapy_redis.spiders import RedisSpider

# class TianSpider(scrapy.Spider):    修改继承类
class TianSpider(RedisSpider):
    name = 'tian'
    # 注销允许的域和qishideurl
    # allowed_domains = ['tianqi.com']
    # start_urls = ['http://lishi.tianqi.com/']

    # 动态获取允许的域
    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None,domain.split(',')))
        super(TianSpider, self).__init__(*args, **kwargs)

     # redis_key
    redis_key = 'tianqi'

    def parse(self, response):
        # 获取地区节点列表
        # node_list = response.xpath('//ul[@class="bcity"]/li/a[@target="_blank"]')
        node_list = response.xpath('//ul[@class="bcity"]/li/a[@target="_blank"]')
        print('********/---------', node_list)

        # 遍历节点列表
        for node in node_list[10:11]:
            url = node.xpath('./@href').extract_first()
            area = node.xpath('./text()').extract_first()

            yield scrapy.Request(url, callback=self.parse_area, meta={'meta_1': area})

    def parse_area(self, response):
        area = response.meta['meta_1']

        # 获取url列表
        url_list = response.xpath('//*[@id="tool_site"]/div[2]/ul/li/a/@href').extract()
        # 遍历url列表
        for url in url_list[10:11]:
            yield scrapy.Request(url, callback=self.parse_data, meta={'meta_2': area})

    def parse_data(self, response):
        area = response.meta['meta_2']

        # 获取数据节点列表
        node_list = response.xpath('//*[@id="tool_site"]/div[@class="tqtongji2"]/ul')

        # 遍历节点列表
        for node in node_list[1:5]:
            # 创建对象
            item = TianqiItem()
            # 抽取数据存在item中
            item['area'] = area
            item['crawl_time'] = time.time()
            item['url'] = response.url

            item['datetime'] = node.xpath('./li[1]/a/text()').extract_first()
            item['max_t'] = node.xpath('./li[2]/text()').extract_first()
            item['min_t'] = node.xpath('./li[3]/text()').extract_first()
            item['weather'] = node.xpath('./li[4]/text()').extract_first()
            item['wind_direction'] = node.xpath('./li[5]/text()').extract_first()
            item['wind_power'] = node.xpath('./li[6]/text()').extract_first()

            # print (item)
            # 返回数据
            yield item
        # pass













