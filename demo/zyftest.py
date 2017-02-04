<<<<<<< HEAD
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class WebdriverDemo(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://test.paymax.cc"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_webdriver_demo(self):
        driver = self.driver
        driver.maximize_window()
        # 访问paymax地址
        driver.get(self.base_url + "/")
        self.assertEqual(driver.find_element_by_xpath(".//*[@id='unlogin']/a[2]/button").text,u'注册')
        # 等待两秒？
        time.sleep(2)
        # 点击登录
        driver.find_element_by_xpath(".//*[@id='unlogin']/a[1]/button").click()
        driver.find_element_by_xpath("html/body/div/div/div/div[2]/div[1]/div/form/div[1]/div[1]/input").send_keys('15001179145')
        time.sleep(0.5)
        # 点击密码
        driver.find_element_by_xpath("html/body/div/div/div/div[2]/div[1]/div/form/div[1]/div[3]/input").send_keys('Feifei12345')
        time.sleep(0.5)
        # 点击登录
        driver.find_element_by_xpath("html/body/div/div/div/div[2]/div[1]/div/form/div[2]/input").click()
        time.sleep(2)
        # 点击创建应用
        # driver.find_element_by_xpath('html/body/div/div[2]/div/ul/li').click()
        # 输入应用名称为20160907testapp
        # driver.find_element_by_xpath(".//*[@id='ngdialog1']/div[2]/div/form/div[1]/div/input").send_keys("20160907testapp")
        # 点击创建
        # driver.find_element_by_xpath(".//*[@id='ngdialog1']/div[2]/div/form/div[2]/input[2]").click()
        time.sleep(3)
        # 点击应用222
        driver.find_element_by_xpath("html/body/div/div[2]/div/ul/li[2]/div/a/span").click()
        self.assertEqual(driver.find_element_by_xpath(".//*[@id='ngdialog1']/div[2]/div/form/div[2]/input[2]").text,u'app_35vz4W8w7Cq4w9r0')
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
        print 'yes'
    def tearDown(self):
       self.driver.quit()
       self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
=======
>>>>>>> 21e6ccc6d3d8bbf959b879462a84f1a9a8170b0d
