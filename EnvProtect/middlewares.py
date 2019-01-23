# -*- coding: utf-8 -*-
import time
import scrapy
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from EnvProtect.settings import USER_AGENTS as ua

class EnvprotectDownloaderMiddleware(object):

    def __init__(self):
        """
        第一页时，不需要点击跳转；其他页面需要模拟点击跳转来获取数据
        """
        self.index = 1

    def process_request(self, request, spider):

        if request.url == 'http://hbj.wuhan.gov.cn/viewAirDarlyForestWaterInfo.jspx':

            self.driver = webdriver.Chrome()  # 实例化一个谷歌浏览器
            self.driver.get(request.url)  # 请求页面
            wait = WebDriverWait(self.driver, 30)  # 等待页面数据加载，等待30s
            try:
                # 选择城区
                wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "iframepage"))) # 等待iframe标签出现
                options = self.driver.find_element_by_xpath("//select[@id='typedictionary']/option[2]")
                options.click()

                # 选择时间
                self.driver.find_element_by_id('cdateBeginDic').send_keys('2018-11-01')
                self.driver.find_element_by_id('cdateEndDic').send_keys('2019-01-20')

                # 点击查询
                self.driver.find_element_by_xpath("//a[@href='#' and @onclick='toQuery(2);']").click()
                time.sleep(5)

                # 指定页面
                if not self.index == 1:
                    self.index += 1  # 第一个页面不用跳转，其他页面需要跳转过去
                    self.driver.find_element_by_id('goPag').send_keys(str(self.index))
                    self.driver.find_element_by_id('_goPag').click()  # 跳转到该页面
            except:
                print("Error!")
                self.driver.quit()

            # 构造返回response
            html = self.driver.page_source
            self.driver.quit()
            response = scrapy.http.HtmlResponse(url=request.url, body=html, request=request, encoding='utf-8')

            return response
