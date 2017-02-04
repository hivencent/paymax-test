# -*- coding: utf-8 -*-
import time

from selenium import webdriver

from share import unittest123321


class WebdriverDemo(unittest123321.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://172.30.21.22:9006"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_webdriver_demo(self):
        driver = self.driver
        driver.maximize_window()

        '''访问地址'''
        driver.get(self.base_url + "/")
        # driver.find_element_by_xpath('html/body/div[2]/form/div[1]/div[1]/input').send_keys('lisi')
        driver.find_element_by_name('account').send_keys('lisi')
        driver.find_element_by_name('password').send_keys('000000')
        driver.find_element_by_class_name('reg').click()
        # driver.find_element_by_xpath(".//*[@id='sidebar']/div[2]/div[3]").click()
        # driver.find_element_by_xpath(".//*[@id='sidebar']/div[2]/div[4]/ul/li[2]/div/a").click()
        driver.find_element_by_class_name('collapsable').click()
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