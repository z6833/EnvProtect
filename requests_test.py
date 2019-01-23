import time
import math

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from openpyxl import Workbook
from lxml import etree


def save_data(item_dicts):

    workbook = Workbook()
    booksheet = workbook.active
    booksheet.append(['日期', '检测点位', '二氧化硫',
                      '二氧化氮', '可吸入颗粒物','一氧化碳',
                      '臭氧', '细颗粒物', '空气质量指数',
                      '首要污染物', 'AQI指数级别', 'AQI指数类别'])
    for item in item_dicts:
        DATA = [
            item['date'], item['loca'], item['SO_2'],
            item['NO_2'], item['PMIO'], item['CO_1'],
            item['O3_d'], item['PM25'], item['AQIe'],
            item['prmy'], item['AQIl'], item['AQIt']
        ]

        booksheet.append(DATA)
        workbook.save('./EnvProtext.xls')


def parse_html(html):

    item=dict();item_list=[]
    e = etree.HTML(html)
    node_list = e.xpath('//*[@id="tableForm"]/div/div[3]/table/tbody/tr')[1:]
    for node in node_list:
        item['date'] = node.xpath("./td[1]/text()")[0]
        item['loca'] = node.xpath("./td[2]/text()")[0]
        item['SO_2'] = node.xpath("./td[3]/text()")[0]
        item['NO_2'] = node.xpath("./td[4]/text()")[0]
        item['PMIO'] = node.xpath("./td[5]/text()")[0]
        item['CO_1'] = node.xpath("./td[6]/text()")[0]
        item['O3_d'] = node.xpath("./td[7]/text()")[0]
        item['PM25'] = node.xpath("./td[8]/text()")[0]
        item['AQIe'] = node.xpath("./td[9]/text()")[0]
        item['prmy'] = node.xpath("./td[10]/text()")[0]
        item['AQIl'] = node.xpath("./td[11]/text()")[0]
        item['AQIt'] = node.xpath("./td[12]/text()")[0]

    return item_list

def main():

    workbook = Workbook()
    booksheet = workbook.active
    booksheet.append(['日期', '检测点位', '二氧化硫',
                      '二氧化氮', '可吸入颗粒物', '一氧化碳',
                      '臭氧', '细颗粒物', '空气质量指数',
                      '首要污染物', 'AQI指数级别', 'AQI指数类别'])

    # 目标url
    url = 'http://hbj.wuhan.gov.cn/viewAirDarlyForestWaterInfo.jspx'

    driver = webdriver.Chrome()
    driver.get(url)  # 访问目标url
    wait = WebDriverWait(driver, 30)  # 等待页面加载
    try:
        # 等待表格出现
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "iframepage")))
        # 选择检测点
        driver.find_element_by_xpath("//select[@id='typedictionary']/option[2]").click()
        # 开始(结束)时间
        driver.find_element_by_id('cdateBeginDic').send_keys('2019-01-01')
        driver.find_element_by_id('cdateEndDic').send_keys('2019-01-20')
        # 点击查询
        driver.find_element_by_xpath("//a[@href='#' and @onclick='toQuery(2);']").click()
        time.sleep(5)
    except:
        print("Error!!")
        driver.close()
        quit()

    # 匹配数据总条数
    pages_num = driver.find_element_by_xpath("//div[@class='serviceitempage fr']/span[@class='fl']").text
    pages_num = math.ceil(int(pages_num.split(' ')[0]) / 22)

    page=1; item_lists=[]
    while page <= pages_num:
        driver.find_element_by_id('goPag').send_keys(str(page))
        driver.find_element_by_id('_goPag').click()  # 跳转到下一页

        html = driver.page_source  # 获取源码
        # 解析数据
        e = etree.HTML(html)
        node_list = e.xpath('//*[@id="tableForm"]/div/div[3]/table/tbody/tr')[1:]
        for node in node_list:
            item=dict()
            item['date'] = node.xpath("./td[1]/text()")[0]
            item['loca'] = node.xpath("./td[2]/text()")[0]
            item['SO_2'] = node.xpath("./td[3]/text()")[0]
            item['NO_2'] = node.xpath("./td[4]/text()")[0]
            item['PMIO'] = node.xpath("./td[5]/text()")[0]
            item['CO_1'] = node.xpath("./td[6]/text()")[0]
            item['O3_d'] = node.xpath("./td[7]/text()")[0]
            item['PM25'] = node.xpath("./td[8]/text()")[0]
            item['AQIe'] = node.xpath("./td[9]/text()")[0]
            item['prmy'] = node.xpath("./td[10]/text()")[0]
            item['AQIl'] = node.xpath("./td[11]/text()")[0]
            item['AQIt'] = node.xpath("./td[12]/text()")[0]

            # 保存数据
            DATA = [
                item['date'], item['loca'], item['SO_2'],
                item['NO_2'], item['PMIO'], item['CO_1'],
                item['O3_d'], item['PM25'], item['AQIe'],
                item['prmy'], item['AQIl'], item['AQIt']
            ]
            booksheet.append(DATA)
        workbook.save('./EnvProtext.xls')

        page += 1
    driver.quit()

if __name__ == '__main__':
    main()
