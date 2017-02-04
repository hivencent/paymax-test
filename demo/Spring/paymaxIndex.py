# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class WebdriverProject(object):

  @classmethod
  def openPaymax(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://test.paymax.cc"
        self.verificationErrors = []
        self.accept_next_alert = True
        global driver
        driver = self.driver
        driver.maximize_window()
        '''访问地址'''
        driver.get(self.base_url + "/")
        time.sleep(3)
        '''点击登录'''  # fafafa
        driver.find_element_by_class_name('login').click()
        driver.find_element_by_name('userName').send_keys('15110079051')
        time.sleep(0.5)
        '''点击密码'''
        driver.find_element_by_name('password').send_keys('1234Qwer')
        time.sleep(0.5)

        # driver.find_element_by_xpath('html/body/div/div/div/div[2]/div[1]/div/form/div[2]/input').click()
        '''点击登录'''

        driver.find_element_by_class_name('btn-blue').click()
        time.sleep(2)

        '''点击app_test2 '''
        driver.find_element_by_xpath('html/body/div/div[2]/div/ul/li[2]/h3').click()
        time.sleep(2)


        '''判断是否跳转到 '''
        welcome=driver.find_element_by_class_name('td_title').text
        if welcome==u'欢迎使用 Paymax123':
           print '成功跳转到了应用详情页'
        else:
           self.getScreenshots()
        '''订单管理 '''
        driver.find_element_by_xpath('html/body/div/div[2]/ul/li[2]/a').click()
        time.sleep(2)
        txt=driver.find_element_by_xpath('html/body/div/div[2]/div/div/div[2]/div[1]/a')
        if txt==u'商品订单':
            print '成功跳转到了订单管理'
        '''支付渠道 '''
        driver.find_element_by_xpath('html/body/div/div[2]/ul/li[3]/a').click()
        btn=driver.find_element_by_xpath('html/body/div/div[2]/div/div/div/div/div[2]/div/button').text
        if btn==u'申请渠道参数':
           print '成功跳转到了支付渠道'
        '''应用信息 '''
        driver.find_element_by_xpath('html/body/div/div[2]/ul/li[4]/a').click()
        h4=driver.find_element_by_xpath('html/body/div/div[2]/div/div/div/div/div[1]/div[1]/h4').text
        if h4==u'应用名称':
           print '成功跳转到了应用信息'
        '''webhooks '''
        driver.find_element_by_xpath('html/body/div/div[2]/ul/li[5]/a').click()
        divText=driver.find_element_by_xpath('html/body/div/div[2]/div/div/div/div/div/div[1]').text
        if divText=='Webhooks':
           print '成功跳转到了Webhooks'
        '''应用概况 '''
        driver.find_element_by_xpath('html/body/div/div[2]/ul/li[1]/a').click()

  @classmethod
  def getScreenshots(self):
        '''截图'''
        screenshot_time = time.strftime("%Y-%m-%d %H:%M:%S")
        screenshots_url = "/Users/Spring/Desktop/Screenshots/"
        screenshots = screenshots_url + screenshot_time + u'' + '.png'
        driver.save_screenshot(screenshots)
        print u'截图成功'
        time.sleep(3)


if __name__ == "__main__":
    WebdriverProject.openPaymax()


