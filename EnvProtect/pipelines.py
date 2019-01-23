# -*- coding: utf-8 -*-
from openpyxl import Workbook

class EnvprotectPipeline(object):

    def __init__(self):
        # 创建excel表格保存数据
        self.workbook = Workbook()
        self.booksheet = self.workbook.active
        self.booksheet.append(['日期', '检测点位', '二氧化硫',
                          '二氧化氮', '可吸入颗粒物', '一氧化碳',
                          '臭氧', '细颗粒物', '空气质量指数',
                          '首要污染物', 'AQI指数级别', 'AQI指数类别'])

    def process_item(self, item, spider):

        DATA = [
            item['date'], item['loca'], item['SO_2'],
            item['NO_2'], item['PMIO'], item['CO_1'],
            item['O3_d'], item['PM25'], item['AQIe'],
            item['prmy'], item['AQIl'], item['AQIt']
        ]

        self.booksheet.append(DATA)
        self.workbook.save('./results.xls')
        return item
