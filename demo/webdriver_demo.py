# -*- coding: utf-8 -*-
import time

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import unittest


class WebdriverDemo(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://test.paymax.cc"
        self.accept_next_alert = True
    
    def test_webdriver_demo(self):
        driver = self.driver
        driver.maximize_window()
        '''访问地址'''
        driver.get(self.base_url + "/")
        self.assertEquals(1,1)

        # driver.find_element_by_id("loginStr").click()
        time.sleep(2)
        '''点击登录'''   #fafafa
        driver.find_element_by_class_name('login').click()
        driver.find_element_by_name('userName').send_keys('2547995165@qq.com')
        time.sleep(0.5)
        '''点击密码'''
        driver.find_element_by_name('password').send_keys('Aa1234')
        time.sleep(0.5)

        '''点击登录'''
        driver.find_element_by_class_name('btn-blue').click()
        time.sleep(2)

        driver.find_element_by_xpath("html/body/div/div[2]/div/ul/li[2]/h3").click()
        time.sleep(1)
        driver.find_element_by_link_text("订单管理").click()
        driver.find_element_by_id('orderExport').click()
        time.sleep(1)

        from selenium.webdriver.common.keys import Keys
        time.sleep(2)
        action = ActionChains
        action.send_keys(Keys.ENTER)

        #获取alter
        print 'alter',driver.switch_to_alert().text

        #所有的窗口
        all_handles = driver.window_handles
        #现在的窗口
        now_handle = driver.current_window_handle
        print now_handle
        all_handles.remove(now_handle)
        print 'size >> ',all_handles.size

        # for h in driver.window_handles[1:]:
        #     driver.switch_to_window(h)
        #     driver.close()
        # driver.switch_to_window(driver.window_handles[0])

        '''
        driver.get('http://test.paymax.cc/web/#/app/center?appKey=app_Q5R525k5HW9C9945')
        driver.find_element_by_link_text(u"应用信息").click()
        for i in range(60):
            try:
                if "app_Q5R525k5HW9C9945" == driver.find_element_by_css_selector(
                    "div.section > div.form-group > input.form-control").get_attribute("value"):
                    print driver.find_element_by_xpath("html/body/div/div[2]/div/div/div/div/div[2]/div[2]/div/input").get_attribute("value")

            except:
                pass
            time.sleep(1)

        #截图
        screenshot_time = time.strftime("%Y-%m-%d %H:%M:%S")
        screenshots_url = "/Users/jinlong/Desktop/Screenshots/"
        screenshots = screenshots_url + screenshot_time + u'测试截图' + '.png'
        driver.save_screenshot(screenshots)
        print u'截图成功'
        time.sleep(3)
<<<<<<< HEAD

=======
        '''
# >>>>>>> 21e6ccc6d3d8bbf959b879462a84f1a9a8170b0d

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True



    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
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
        finally: self.accept_next_alert = True

    def close_all_popups(driver):
        driver.window_handles
        for h in driver.window_handles[1:]:
            driver.switch_to_window(h)
            driver.close()
        driver.switch_to_window(driver.window_handles[0])

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
