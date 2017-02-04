# -*- coding: utf-8 -*-
import time

from selenium import webdriver

from share import unittest123321


class WebdriverDemo(unittest123321.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://test.paymax.cc"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_webdriver_demo(self):
        driver = self.driver
        driver.maximize_window()

        '''访问地址'''
        driver.get(self.base_url + "/")
        #通过CSS路径定位:
        # driver.find_element_by_css_selector("a[class='button blue cta']").click()
        #通过XPATH路径定位
        # driver.find_element_by_xpath(".//*[@id='bgstylec']/div[2]/div/p/a").click()
        # driver.find_element_by_css_selector("button[class='btn btn-primary none']").click()   #登录
        driver.find_element_by_css_selector("button[class='btn btn-success']").click()

        time.sleep(3)

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
    unittest123321.main()