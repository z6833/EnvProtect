# -*- coding: utf-8 -*-
import scrapy

class EnvprotectItem(scrapy.Item):

    # 日期
    date = scrapy.Field()
    # 点位
    loca = scrapy.Field()
    # SO2
    SO_2 = scrapy.Field()
    # NO2
    NO_2 = scrapy.Field()
    # 吸入颗粒
    PMIO = scrapy.Field()
    # CO
    CO_1 = scrapy.Field()
    # O3
    O3_d = scrapy.Field()
    # 细颗粒物
    PM25 = scrapy.Field()
    # 空气质量指数
    AQIe = scrapy.Field()
    # 首要污染物
    prmy = scrapy.Field()
    # AQI级别
    AQIl = scrapy.Field()
    # AQI类别
    AQIt = scrapy.Field()
