# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("../../")
import os
import unittest
import time
from website.util.utility import *
from website.util.web_util import *
from api.util import PaymaxUtil
import settings
from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys     #键盘操作


#test
class VERITY_CHANNEL(unittest.TestCase):


    @classmethod
    def setUpClass(self):

        self.driver = webdriver.PhantomJS("%s/phantomjs-2.1.1/bin/phantomjs" % WebConfig.PHANTOMJS)  #webdriver.Firefox()
        # self.driver = webdriver.Firefox()


        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.url = WebConfig.HOST.FRONTEND_TEST_HOST
        self.appname = UTILITY.gen_appname("WEB")
        self.screenshots_url = "/tmp/Screenshots/"

        self.uploadFile = WebConfig.ABSPATH + "VerityCompanyUpload.jpg"
        self.uploadIcon = WebConfig.ABSPATH + "icon.png"


    # @unittest.skip(reason=u"调试")
    def test_verity_channel(self):

        driver = self.driver
        driver.set_window_size(1366,768)                 #设置浏览器大小

        #申请开通渠道需要商户企业认证通过
        #先查询数据库是否有企业认证通过的商户，如果有，直接用该数据
        #如果没有，重新走注册商户-企业认证流程（VerityCompany.py流程）
        (self.phone,self.company_name) = FrontEndWebUtil.query_merchant()
        print u"公司名：",self.company_name

        #登录
        PaymaxUtil.echo_title(u"Paymax前台登录")
        result = FrontEndWebUtil().web_login(driver=driver,username=self.phone,password=WebConfig.REGISTER_PW)
        #断言登录成功
        self.assertTrue(result)
        search_value = driver.find_element_by_xpath("//input[@type='text'][@ng-model='searchValue']").get_attribute('placeholder')
        self.assertEqual(search_value,u"搜索商户订单号/订单ID")  # 断言登录成功后,搜索框
        print u'登录的账号 %s 密码 %s :' % (self.phone, WebConfig.REGISTER_PW)

        #创建应用
        PaymaxUtil.echo_title(u"创建应用")
        FrontEndWebUtil().create_app(driver=driver,appname=self.appname)
        # driver.refresh()
        #查找应用，进入详情
        PaymaxUtil.echo_title(u"查找应用，进入详情")
        FrontEndWebUtil().find_app(driver=driver, appname=self.appname)     #找到创建的应用，点进去

        #点击"支付渠道"
        purchase_ele = driver.find_element(By.LINK_TEXT,u"支付渠道")
        purchase_ele.click()
        self.assertEqual(driver.find_element(By.XPATH,"//button[@ng-click='toApplyChannel()']").text,u"申请渠道参数")             #断言右上方有"申请渠道参数"按钮


        #点击"申请渠道参数"
        PaymaxUtil.echo_title(u"点击'申请渠道参数'")
        time.sleep(0.3)
        Wait.wait_until_clickable(driver=driver,by=By.XPATH,values="//button[@ng-click='toApplyChannel()']")
        time.sleep(0.3)
        try:
            print u"点击'申请渠道参数'按钮，成功。。。"
            toApplyChannel = driver.find_element(By.XPATH,"//button[@ng-click='toApplyChannel()']")
            toApplyChannel.click()
        except:
            print u"点击'申请渠道参数'失败，重试。。。"
            driver.refresh()
            toApplyChannel = driver.find_element(By.XPATH, "//button[@ng-click='toApplyChannel()']").click()
        FrontEndWebUtil().screenshots(driver=driver,picname="guiyi.jpg")
        if self.is_element_present(By.CLASS_NAME,"poptitle"):                   #尝试弹窗捕获，偶尔会有弹窗导致失败，还不确定原因
            print driver.find_element(By.CLASS_NAME,"poptitle").text

        #申请开通所有渠道
        PaymaxUtil.echo_title(u"选择支付渠道-所有")
        LINK_TEXT = [u"移动APP支付",u"PC网页支付",u"移动网页支付",u"扫码支付"]
        for i in LINK_TEXT:
            Wait.wait_until_clickable(driver=driver,by=By.LINK_TEXT,values=i)
            driver.find_element(By.LINK_TEXT,i).click()
            check_elements = driver.find_elements(By.XPATH,"//input[@type='checkbox'][@ng-model='channel.choosed']")
            print u"开通'%s' 下支付渠道" % i
            for i in check_elements:
                if i.is_selected() == True:         #如果checkbox是选中状态，则跳出循环
                    continue
                i.click()
                if self.is_element_present(By.CSS_SELECTOR, "h2.poptitle > div"):
                    Wait.wait_until_clickable(driver=driver,by=By.CSS_SELECTOR,values="input.btn.btnDashboard")
                    driver.find_element_by_css_selector("input.btn.btnDashboard").click()
                    time.sleep(0.5)

        #等待下一步可点击，点击"下一步"
        confirm = driver.find_element(By.XPATH,"//button[@ng-click='confirmChoose()']")
        print u"点击：",confirm.text
        Wait.wait_until_clickable(driver=driver,by=By.XPATH,values="//button[@ng-click='confirmChoose()']")
        driver.find_element(By.XPATH,"//button[@ng-click='confirmChoose()']").click()

        #弹出确认框，点击确定
        poptitle = driver.find_element(By.CLASS_NAME,"poptitle").text
        print u"确认信息",poptitle
        btnDashboard = driver.find_element_by_css_selector("input.btn.btnDashboard")
        print u"点击：",btnDashboard.get_attribute("value")
        Wait.wait_until_clickable(driver=driver,by=By.CSS_SELECTOR,values="input.btn.btnDashboard")
        driver.find_element_by_css_selector("input.btn.btnDashboard").click()
        #等待确认框不显示(消失)
        Wait.wait_until_not_presence(driver=driver,by=By.CLASS_NAME,values="poptitle")

        PaymaxUtil.echo_title(u"付款")
        #点击去支付
        print u"点击：",driver.find_element(By.CSS_SELECTOR,"button.btn.btnDashboard").text
        Wait.wait_until_clickable(driver=driver,by=By.CSS_SELECTOR,values="button.btn.btnDashboard")
        driver.find_element(By.CSS_SELECTOR,"button.btn.btnDashboard").click()

        #尝试捕获"系统异常"，如果5S后还没有，则继续进行
        #PS：不能直接判断，因为点击"去支付"时，有时需要很长时间才会弹出系统异常，所以需要循环判断
        for i in range(5):
            try:
                if u"系统异常" == driver.find_element_by_css_selector("h2.poptitle.ng-binding").text:
                    print u"捕获到：", driver.find_element(By.CSS_SELECTOR, "h2.poptitle.ng-binding").text
                    Wait.wait_until_clickable(driver=driver, by=By.CSS_SELECTOR,values="input.btn.btnDashboard")  # 等待弹出框确定可点击
                    time.sleep(0.5)
                    # TODO 经常没有成功点击"确定"
                    driver.find_element_by_css_selector("input.btn.btnDashboard").click()  # 点击确定
                    Wait.wait_until_not_presence(driver=driver, by=By.CSS_SELECTOR,values="input.btn.btnDashboard")  # 等待确认按钮不显示
                    time.sleep(0.5)
                    Wait.wait_until_clickable(driver=driver, by=By.CSS_SELECTOR,values="button.btn.btnDashboard")  # 等待去支付可点击
                    driver.find_element(By.CSS_SELECTOR, "button.btn.btnDashboard").click()  # 再次点击去支付
                    break
            except Exception as e:
                print u"没有捕获到系统异常元素"
                time.sleep(1)

        #等待页面左上角"公司信息"元素存在，表示页面加载完成
        Wait.wait_until_presence(driver=driver,by=By.CLASS_NAME,values="current")
        print u"等待页面左上角'公司信息'元素存在，表示页面加载完成"
        FrontEndWebUtil().channel_apply_status(driver=driver,itemText=u"付款")

        '''
        #判断等待加载from title
        for i in range(1, 3, 1):
            print self.is_element_present(how=By.CLASS_NAME,what="current")
            if self.is_element_present(how=By.CLASS_NAME,what="current") == True:
                break
            time.sleep(1)
            continue
        '''


        PaymaxUtil.echo_title(u"填写申请材料-%s" % driver.find_element(By.CLASS_NAME,"current").text)
        ##法人身份证正面
        FrontEndWebUtil().upload(driver=driver,by=By.NAME,value="file01",up_file=self.uploadFile)
        ##法人身份证反面
        FrontEndWebUtil().upload(driver=driver,by=By.NAME,value="file02",up_file=self.uploadFile)
        ##经办人身份证正面
        FrontEndWebUtil().upload(driver=driver,by=By.NAME,value="file05",up_file=self.uploadFile)
        ##经办人身份证背面
        FrontEndWebUtil().upload(driver=driver,by=By.NAME,value="file06",up_file=self.uploadFile)
        ##商户简称
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="company_merchant_short_name",values=u"商户简称")
        # driver.find_element(By.NAME,"company_merchant_short_name").send_keys(u"自动化测试商户简称")
        ##需接入支付的网站地址
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="company_app_website",values="http://www.baidu.com")
        # driver.find_element(By.NAME,"company_app_website").send_keys("http://www.baidu.com")
        ##ICP 备案号
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="company_website_icp",values=u"京ICP备0000001号")
        # driver.find_element(By.NAME,"company_website_icp").send_keys(u"京ICP备0000001号")
        ##座机电话
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="company_telephone",values="010-88888888")
        # driver.find_element(By.NAME,"company_telephone").send_keys("010-88888888")
        ##部门与职位
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="company_department_and_job",values=u"部门与职位")
        # driver.find_element(By.NAME,"company_department_and_job").send_keys(u"自动化测试工程师")
        ##滚动滚动条
        # print u"滚动滚动条"
        # driver.execute_script("arguments[0].scrollIntoView(true);",element)
        element = driver.find_element(By.NAME, "company_department_and_job")
        FrontEndWebUtil().scroll_to_element(driver=driver,element=element)
        ##商户类型
        elementsObj = driver.find_elements(By.TAG_NAME, "span")
        FrontEndWebUtil().findElements(elementsObj=elementsObj,filtration=u"选择类型")
        elementsObj = driver.find_elements(By.TAG_NAME,"li")
        FrontEndWebUtil().findElements(elementsObj=elementsObj,filtration=u"一般企业")
        print u"选择商户类型：一般企业"
        ##申请公函
        FrontEndWebUtil().upload(driver=driver,by=By.NAME,value="companyOfficalLetterImg",up_file=self.uploadFile)
        ##其它补充材料（选填）
        FrontEndWebUtil().upload(driver=driver,by=By.NAME,value="otherFile",up_file=self.uploadFile)
        ##点击公司信息保存
        companySave = driver.find_element(By.XPATH,"//input[@type='submit'][@value='保存'][@ng-disabled='companyForm.$invalid']")
        time.sleep(1)
        Wait.wait_until_clickable(driver=driver,by=By.XPATH,values="//input[@type='submit'][@value='保存'][@ng-disabled='companyForm.$invalid']")      #等待保存点击
        print u"点击银行信息：%s按钮" % driver.find_element(By.XPATH,"//input[@type='submit'][@value='保存'][@ng-disabled='companyForm.$invalid']").get_attribute("value")
        companySave.click()                         #点击保存
        Wait.wait_until_not_presence(driver=driver,by=By.CLASS_NAME,values="poptitle")              ##等待弹出框不显示


        #填写申请材料-银行信息
        PaymaxUtil.echo_title(u"填写申请材料-银行信息")
        #上传开户许可证
        FrontEndWebUtil().upload(driver=driver,by=By.NAME,value="account_licence",up_file=self.uploadFile)
        #填写银行卡所在支行
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="account_subbranch",values=u"银行卡所在支行")
        #填写银行对公账号
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="account_no",values="99999999999")
        #将页面滚动到保存位置
        FrontEndWebUtil().scroll_to_element(driver=driver,element=driver.find_element(By.XPATH,"html/body/div/div[3]/div[1]/div/div/div[4]/form/div[1]/h3"))
        #点击银行信息保存
        bankSave = driver.find_element(By.XPATH, "//input[@type='submit'][@value='保存'][@ng-disabled='bankForm.$invalid']")
        Wait.wait_until_clickable(driver=driver,by=By.XPATH,values="//input[@type='submit'][@value='保存'][@ng-disabled='bankForm.$invalid']")
        print u'点击银行信息：%s按钮' % bankSave.get_attribute("value")
        bankSave.click()
        Wait.wait_until_not_presence(driver=driver,by=By.CLASS_NAME,values="poptitle")              ##等待弹出框不显示


        #填写申请材料-APP信息
        PaymaxUtil.echo_title(u"填写申请材料-APP信息")
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="app_description",values=u"APP介绍")
        #选择一级行业
        elementsObj = driver.find_elements(By.TAG_NAME,"span")
        FrontEndWebUtil().findElements(elementsObj=elementsObj,filtration=u"选择一级行业")
        elementsObj = driver.find_elements(By.TAG_NAME,"li")
        FrontEndWebUtil().findElements(elementsObj=elementsObj,filtration=u"电商/团购")
        time.sleep(0.3)
        #选择二级行业
        elementsObj = driver.find_elements(By.TAG_NAME,"span")
        FrontEndWebUtil().findElements(elementsObj=elementsObj,filtration=u"选择二级行业")
        elementsObj = driver.find_elements(By.TAG_NAME,"li")
        FrontEndWebUtil().findElements(elementsObj=elementsObj,filtration=u"团购")
        #填写微信公众号主体信息
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="wechat_company_name",values=u"微信公众号主体信息")
        #APP ID
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="app_id",values="wx5269eef08886e3d5")
        #支付授权目录（选填）
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="auth_dir",values="http://www.auth_dir.com/auth_dir")
        #上传APP图标
        FrontEndWebUtil().upload(driver=driver,by=By.NAME,value="file08_28",up_file=self.uploadIcon)
        FrontEndWebUtil().upload(driver=driver,by=By.NAME,value="file08_128",up_file=self.uploadIcon)
        #选择APP平台
        ios_platform = driver.find_element(By.NAME, "ios_platform")
        Wait.wait_until_clickable(driver=driver,by=By.NAME,values="ios_platform")
        self.assertEqual(ios_platform.is_selected(),False,u"APP平台：ios已经是选中状态")
        ios_platform.click()
        print u"选择APP平台：",ios_platform.text
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="ios_appstore_url",values="http://www.baidu.com")
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="ios_bundle_id",values="automationtest")
        #APP首页截图
        FrontEndWebUtil().upload(driver=driver, by=By.NAME, value="file09", up_file=self.uploadFile)
        #APP商品类目页截图
        FrontEndWebUtil().upload(driver=driver,by=By.NAME,value="file10",up_file=self.uploadFile)
        #APP商品详情页截图
        FrontEndWebUtil().upload(driver=driver,by=By.NAME,value="file12",up_file=self.uploadFile)
        #APP商品支付页截图
        FrontEndWebUtil().upload(driver=driver,by=By.NAME,value="file13",up_file=self.uploadFile)
        #APP尾页截图
        FrontEndWebUtil().upload(driver=driver,by=By.NAME,value="file14",up_file=self.uploadFile)
        #点击APP信息保存
        bankSave = driver.find_element(By.XPATH,"//input[@type='submit'][@value='保存'][@ng-disabled='appInfoForm.$invalid']")
        Wait.wait_until_clickable(driver=driver, by=By.XPATH,values="//input[@type='submit'][@value='保存'][@ng-disabled='appInfoForm.$invalid']")
        print u'点击APP信息：%s按钮' % bankSave.get_attribute("value")
        bankSave.click()
        Wait.wait_until_not_presence(driver=driver, by=By.CLASS_NAME, values="poptitle")  ##等待弹出框不显示


        #填写申请材料-渠道申请专用邮箱信息
        PaymaxUtil.echo_title(u"填写申请材料-渠道申请专用邮箱信息")
        #邮箱账号
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="email_account",values="email_account@126.com")
        #邮箱密码
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="email_password",values="email_password")
        #邮箱登录地址
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="email_login_url",values="http://mail.126.com")
        #风险联系人
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="emergency_contact_name",values=u"金龙")
        #风险联系人手机号码
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="emergency_contact_mobile",values="18910505634")
        #风险联系人邮箱地址
        FrontEndWebUtil().send_keys(driver=driver,how=By.NAME,what="emergency_contact_email",values="277954117@qq.com")
        #点击邮箱信息"保存"
        emailInfoSave = driver.find_element(By.XPATH,"//input[@type='submit'][@value='保存'][@ng-disabled='emailInfoForm.$invalid']")
        Wait.wait_until_clickable(driver=driver, by=By.XPATH,values="//input[@type='submit'][@value='保存'][@ng-disabled='emailInfoForm.$invalid']")
        print u'点击邮箱信息：%s按钮' % emailInfoSave.get_attribute("value")


        emailInfoSave.click()
        Wait.wait_until_not_presence(driver=driver, by=By.CLASS_NAME, values="poptitle")  ##等待弹出框不显示

        #点击提交
        submitButton = driver.find_element(By.XPATH,"//button[@ng-click='submitApply()'][@ng-disabled='disableScheduleInfo()']")
        Wait.wait_until_clickable(driver=driver,by=By.XPATH,values="//button[@ng-click='submitApply()'][@ng-disabled='disableScheduleInfo()']")     #等到提交可点击
        submitButton.click()                #点击提交按钮

        #断言"填写申请材料"阶段已经完成
        Wait.wait_until_clickable(driver=driver,by=By.XPATH,values="//button[@ng-click='goToChannelCenterPage()']")         #等待当前页"知道了"按钮可点击，证明页面已经加载完成
        FrontEndWebUtil().channel_apply_status(driver=driver,itemText=u"填写申请材料")
        PaymaxUtil.echo_title(u"提交申请材料完成-申请中")

        #断言申请的渠道数是10个
        channels = driver.find_elements(By.XPATH,"//td[@class='channel ng-binding']")
        print u"申请的渠道数：",len(channels)
        self.assertEqual(len(channels),10)
        for i in channels:
            print u"已经申请的渠道：",i.text

        #点击"知道了"
        print u"确认材料已经提交完成，点击：%s" % driver.find_element(By.XPATH,"//button[@ng-click='goToChannelCenterPage()']").text
        driver.find_element(By.XPATH,"//button[@ng-click='goToChannelCenterPage()']").click()

        time.sleep(7)


    def tearDown(self):

        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def is_element_present(self, how, what):
        self.driver.implicitly_wait(1.5)
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e:
            return False
        return True

if __name__ == "__main__":
    unittest.main()