# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("../../")
from api.util import PaymaxUtil
from website.util.utility import *
from website.util.web_util import *
import time
import settings
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys     #键盘操作
import unittest

REGISTER_PW = "Jinlong1990"

class VERITY_COMPANY(unittest.TestCase):


    @classmethod
    def setUpClass(self):

        profileDir = "/Users/jinlong/Library/Application Support/Firefox/Profiles/dadce4yb.default"
        profile = webdriver.FirefoxProfile(profileDir)
        self.driver = webdriver.Firefox(profile)

        self.driver.implicitly_wait(8)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.url = "https://nper.cmbc.com.cn/pweb/static/login.html"
        # self.url = "https://ebsnew.boc.cn/boc15/login.html"



    # @unittest.skip(reason=u"调试")
    def test_frontend_verity_company(self):
        driver = self.driver
        driver.set_window_size(1366,768)
        driver.get(self.url)

        # 民生
        driver.find_element(By.ID,"writeUserId").send_keys("123")
        time.sleep(5)
        # driver.find_element(By.CLASS_NAME,"ocx_style").send_keys("456")
        driver.find_element(By.CLASS_NAME,"ocx_style").click()
        driver.execute("document.getElementById('_ocx_passwordChar_login').type=text;")
        print driver.find_element(By.CLASS_NAME,"ocx_style").get_attribute("type")
        driver.find_element(By.CLASS_NAME,"ocx_style").send_keys(Keys.BACKSPACE)
        driver.find_element(By.ID,"loginButton").click()

        # driver.find_element(By.ID,"txt_username_79443").send_keys("622899999999")
        # time.sleep(1)
        # driver.executeScript("document.getElementById('div_password_79445').type=text;")
        # driver.find_element(By.ID,"div_password_79445").send_keys("123321")
        # driver.find_element(By.ID,"btn_login_79676").click()

        time.sleep(30)


    def tearDown(self):

        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def is_element_present(self, how, what):
        self.driver.implicitly_wait(3)
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e:
            return False
        return True

if __name__ == "__main__":
    unittest.main()