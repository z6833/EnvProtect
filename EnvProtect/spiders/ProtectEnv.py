# -*- coding: utf-8 -*-
import math
import scrapy
from EnvProtect.items import EnvprotectItem

class ProtectenvSpider(scrapy.Spider):
    name = 'ProtectEnv'
    # allowed_domains = ['hbj.wuhan.gov.cn']
    # start_urls = ['http://hbj.wuhan.gov.cn/']
    page=1
    pages=1

    # 目标url
    base_url = 'http://hbj.wuhan.gov.cn/viewAirDarlyForestWaterInfo.jspx'

    def start_requests(self):

        yield scrapy.Request(
            url=self.base_url,
            callback=self.parse,
            dont_filter=True, # 设置不过滤重复请求，scrapy默认过滤重复请求
            meta={'index':1}  # 该参数判断是否为第一次请求
        )

    def parse(self, response):

        """
        第一次请求返回结果中解析出，指定时间段（在middlewares.py文件中指定，后续介绍）内一共有多少条数据；
        由于一直是对同一个页面进行爬取（翻页时url没变，数据变了），数据共多少条（页）确定一次就够了
        :param response:
        :return:
        """
        if response.meta['index']:
            counts = response.xpath("//div[@class='serviceitempage fr']/span[@class='fl']/text()").extract_first()
            counts = int(counts.split(' ')[0])
            self.pages = math.ceil(counts / 22)  # 确定一共多少个页面

        # 解析数据
        node_list = response.xpath('//*[@id="tableForm"]/div/div[3]/table/tbody/tr')[1:]
        for node in node_list:
            item = EnvprotectItem()
            item['date'] = node.xpath("./td[1]/text()").extract_first()
            item['loca'] = node.xpath("./td[2]/text()").extract_first()
            item['SO_2'] = node.xpath("./td[3]/text()").extract_first()
            item['NO_2'] = node.xpath("./td[4]/text()").extract_first()
            item['PMIO'] = node.xpath("./td[5]/text()").extract_first()
            item['CO_1'] = node.xpath("./td[6]/text()").extract_first()
            item['O3_d'] = node.xpath("./td[7]/text()").extract_first()
            item['PM25'] = node.xpath("./td[8]/text()").extract_first()
            item['AQIe'] = node.xpath("./td[9]/text()").extract_first()
            item['prmy'] = node.xpath("./td[10]/text()").extract_first()
            item['AQIl'] = node.xpath("./td[11]/text()").extract_first()
            item['AQIt'] = node.xpath("./td[12]/text()").extract_first()
            yield item

        # 编写爬虫停止运行逻辑
        if self.page < self.pages:
            self.page += 1
            yield scrapy.Request(
                url = self.base_url,
                callback=self.parse,
                dont_filter=True,  # 不过滤重复请求，scrapy默认过滤重复请求
                meta={'index':0}
            )
