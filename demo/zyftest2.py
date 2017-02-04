# -*- coding: utf-8 -*-
import random
# 调用随机生成应用名称函数
from website.util.utility import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import time
from website.util.web_util import *
import re
from selenium.webdriver.support.wait import WebDriverWait

class WebdriverDemo(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://172.30.21.22:8888/"
        self.verificationErrors = []
        self.accept_next_alert = True
        #流水账主流程
    def test_webdriver_demo(self):
        driver = self.driver
        driver.maximize_window()
        # 访问paymax地址
        driver.get(self.base_url + "/")
        self.assertEqual(driver.find_element_by_xpath(".//*[@id='unlogin']/a[2]/button").text,u'注册')
        time.sleep(1)
        # 点击登录按钮
        driver.find_element_by_xpath(".//*[@id='unlogin']/a[1]/button").click()
        # 输入用户名和密码
        driver.find_element_by_xpath("html/body/div/div/div/div[2]/div[1]/div/form/div[1]/div[1]/input").send_keys('15001179145')
        time.sleep(0.5)
        driver.find_element_by_xpath("html/body/div/div/div/div[2]/div[1]/div/form/div[1]/div[3]/input").send_keys('Feifei12345')
        time.sleep(0.5)
        # 点击登录按钮
        driver.find_element_by_xpath("html/body/div/div/div/div[2]/div[1]/div/form/div[2]/input").click()
        time.sleep(2)
        '''
        driver.find_element_by_xpath("html/body/div/div[2]/div/ul/li[2]/div/a/span").click()
        time.sleep(3)
        driver.find_element_by_xpath("html/body/div/div[2]/div/div/div/div/div[3]/button").click()
        time.sleep(2)
        driver.find_element_by_css_selector("input.btn.btnDashboard").click()
        #当session过期时需要重新输入登录密码
        driver.find_element_by_xpath("//input[@type='password']").send_keys('Feifei12345')
        time.sleep(2)
        driver.find_element_by_css_selector("input.btn.btnDashboard").click()
        #当session未过期时直接跳过
        time.sleep(3)
        '''
        # 点击创建应用
        driver.find_element_by_xpath('html/body/div/div[2]/div/ul/li[1]/div/p[1]/img').click()
        time.sleep(1)
        # 输入随机生成的应用名称
        APPNAME = UTILITY.gen_appname("WEB")
        driver.find_element_by_name("appName").send_keys(APPNAME)
        # 点击创建
        time.sleep(1)
        driver.find_element_by_css_selector("input.btn.btnDashboard").submit()
        time.sleep(2)
        # 点击新建的应用appid
        driver.find_element_by_xpath("html/body/div/div[2]/div/ul/li[2]/div/a/span").click()
        time.sleep(1)
        # 断言更新按钮元素正确
        self.assertEqual(driver.find_element_by_xpath("html/body/div/div[2]/div/div/div/div/div[1]/div[2]/div/button").text,u'更 新')
        # 输出appid
        print driver.find_element_by_xpath("html/body/div/div[2]/div/div/div/div/div[2]/div[2]/div/input").get_attribute("value")
        # 断言app名称正确
        print driver.find_element_by_xpath("/html/body/div/div[2]/div/div/div/div/div[1]/div[2]/div/div/input").get_attribute("value")
        print APPNAME
        print type(APPNAME)
        # self.assertEqual(driver.find_element_by_xpath( "/html/body/div/div[2]/div/div/div/div/div[1]/div[2]/div/div/input").get_attribute("value"),APPNAME)
        time.sleep(2)
        # 点击应用概况链接
        driver.find_element_by_link_text(u"应用概况").click()
        # 等待两秒必须
        time.sleep(2)
        # 输出“发起真实交易”文本
        print driver.find_element_by_xpath("html/body/div/div[2]/div/div[1]/div").text
        time.sleep(1)
        # 断言开通支付渠道按钮正确
        self.assertEqual(driver.find_element_by_xpath("html/body/div/div[2]/div/div[1]/ul/li[2]/div[2]/div/button").text,u"开通支付渠道")
        # 点击“订单管理”链接
        driver.find_element_by_link_text(u"订单管理").click()
        # 输出“商品订单”文本
        print driver.find_element_by_xpath("html/body/div/div[2]/div/div/div[2]/div[1]/a").text
        #  断言商品订单文本正确
        self.assertEqual(driver.find_element_by_xpath("html/body/div/div[2]/div/div/div[2]/div[1]/a").text,u"商品订单")
        driver.find_element_by_xpath("html/body/div/div[1]/a").click()
        time.sleep(2)
        self.assertEqual(driver.find_element_by_xpath("html/body/div/div[2]/div/ul/li[2]/div/p[1]/span").text,u'本应用尚未开通渠道')
        driver.find_element_by_xpath("html/body/div/div[2]/div/ul/li[2]/div/p[1]/span").click()
        time.sleep(2)
        driver.find_element_by_xpath("html/body/div/div[2]/div/div[1]/ul/li[2]/div[2]/div/button").click()
        time.sleep(1)
        driver.find_element_by_xpath("html/body/div/div[2]/div/div/div/div/div[2]/div/button").click()
        time.sleep(1)
        driver.find_element_by_link_text(u"PC网页支付").click()
        time.sleep(2)
        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div[2]/div[2]/table/tbody[4]/tr/td[1]/input").click()
        time.sleep(2)
        driver.find_element_by_xpath("html/body/div/div[3]/div[2]/div/div[1]/div[2]/div/button").click()
        time.sleep(2)
        driver.find_element_by_css_selector("input.btn.btnDashboard").click()
        time.sleep(2)
        driver.find_element_by_css_selector("button.btn.btnDashboard").click()
        time.sleep(2)
        # 删除应用列表中最后一个应用，避免应用数大于9个
        # WebUtil().delete_app(driver=driver, appname=APPNAME)
        filename1 = "D:\\002.png"
        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[1]/form/div[2]/div[1]/div[1]/div[2]/div[1]/input[2]").send_keys(filename1)
        time.sleep(2)
        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[1]/form/div[2]/div[1]/div[2]/div[2]/div[1]/input[2]").send_keys(filename1)
        time.sleep(2)
        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[1]/form/div[2]/div[1]/div[3]/div[2]/div/div/input").send_keys("http://baidu.com")
        time.sleep(1)
        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[1]/form/div[2]/div[1]/div[4]/div[2]/div/div/input").send_keys(u"京ICP000001号")
        time.sleep(1)
        driver.find_element_by_xpath( "html/body/div/div[3]/div[1]/div/div/div[1]/form/div[2]/div[1]/div[5]/div[2]/div[1]/input[2]").send_keys( filename1)
        time.sleep(1)
        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[1]/form/div[2]/div[2]").click()
        time.sleep(5)
        # driver.find_element_by_css_selector("div.popfooter > input.btn.btnDashboard").click()
        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[2]/form/div[2]/div[1]/div[1]/div[2]/div[1]/input[2]").send_keys(filename1)
        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[2]/form/div[2]/div[1]/div[2]/div[2]/div/div/input").send_keys(u"上海浦发银行")
        # self.assertEqual(driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[2]/form/div[2]/div[1]/div[3]/div[2]/div/div/input").text,u'北京顺维无限科技有限公司')
        print driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[2]/form/div[2]/div[1]/div[3]/div[2]/div/div/input").get_attribute("value")
        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[2]/form/div[2]/div[1]/div[4]/div[2]/div/div/input").send_keys("6222020200075978888")
        time.sleep(1)
        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[2]/form/div[2]/div[2]").click()
        driver.find_element_by_name("app_description").send_keys(u'app说明云云')

        time.sleep(0.5)
        elements = driver.find_elements(By.TAG_NAME,"span")
        for i in elements:
            print 'span,',i.text
            if i.text == u"选择一级行业":
                time.sleep(2)
                i.click()
                time.sleep(3)

        time.sleep(0.5)
        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[3]/form/div[2]/div[1]/div[3]/div[2]/div/div/dropdown[1]/div/ul/li[2]").click()
        time.sleep(0.5)
        driver.find_element_by_css_selector("dropdown[name=\"appChildsTypes\"] > div.selectWrap > div.selectBtn > span.ng-binding.ng-scope").click()
        time.sleep(0.5)
        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[3]/form/div[2]/div[1]/div[3]/div[2]/div/div/dropdown[2]/div/ul/li[2]").click()
        time.sleep(5)

        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[3]/form/div[2]/div[2]").click()
        driver.find_element_by_css_selector("div.popfooter > input.btn.btnDashboard").click()
        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[4]/form/div[2]/div[1]/div[1]/div[2]/div/div/input").send_keys("545869238@qq.com")
        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[4]/form/div[2]/div[1]/div[2]/div[2]/div/div/input").send_keys("545666767")
        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[4]/form/div[2]/div[1]/div[3]/div[2]/div/div/input").send_keys("http://foxmail.com")
        time.sleep(2)
        driver.find_element_by_xpath("html/body/div/div[3]/div[1]/div/div/div[4]/form/div[2]/div[2]").click()
        time.sleep(2)
        driver.find_element_by_xpath("html/body/div/div[3]/div[2]/div/div/div/button").click()
        time.sleep(2)
        # driver.find_element_by_xpath("html/body/div/div[3]/div[3]/div/div/div/button").click()
        driver.find_element_by_css_selector("html body div.ng-scope div.ng-scope div.pop_bottom_fix.in.ng-scope div.b_fix_wrap div.wrapper div.pull-right button.btn.btnDashboard").click()

    def is_element_present(self, how, what):
     try:
            self.driver.find_element(by=how, value=what)
     except NoSuchElementException, e:
        return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException, e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True
    def tearDown(self):
       self.driver.quit()
       self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
