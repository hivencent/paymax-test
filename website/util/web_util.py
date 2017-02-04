# -*- coding: utf-8 -*-
__author__ = 'jinlong'
from selenium.webdriver.support import expected_conditions as EC
from website.config import WebConfig
from selenium.webdriver.support.ui import WebDriverWait         #等待某个条件出发后再继续执行代码
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import unittest
import time
import settings
from api.util import PaymaxUtil
import os



class FrontEndWebUtil(unittest.TestCase):

    def __init__(self):
        self.url = WebConfig.HOST.FRONTEND_TEST_HOST


    def register(self,driver,phone):

        driver.get(self.url)
        driver.find_element(By.LINK_TEXT, u"注册").click()
        # self.assertIn(u"用户注册",driver.title)
        driver.find_element(By.NAME, "phone").send_keys(phone)
        driver.find_element(By.NAME, "password").send_keys(WebConfig.REGISTER_PW)
        driver.find_element(By.NAME, "repassword").send_keys(WebConfig.REGISTER_PW)

        # 获取验证码
        Wait.wait_until_clickable(driver=driver, by=By.XPATH, values=u"//input[@value='获取验证码']")  # 等待获取验证码按钮可点击
        driver.find_element(By.XPATH, u"//input[@value='获取验证码']").click()
        print u"\n点击发送验证码,从数据库获取验证码......"
        time.sleep(2)
        sql = "select * from t_sms_record where send_mobile = %s" % phone
        res = list(settings.db_config(db="message").query(sql))[0].send_content
        print res

        ##筛选内容中验证码
        sms_code = ''
        for i in res:
            if i.isdigit():
                sms_code = sms_code + i

        driver.find_element(By.NAME, "code").send_keys(sms_code)
        driver.find_element(By.NAME, "checkbox").click()
        Wait.wait_until_clickable(driver=driver, by=By.CSS_SELECTOR, values="input.btn-blue")  # 等待完成按钮可点击

        driver.find_element(By.CSS_SELECTOR, "input.btn-blue").click()
        Wait.wait_until_visibility(driver=driver, by=By.CLASS_NAME, values="popbox")  # 等待注册成功弹层显示
        register_result = driver.find_element(By.CLASS_NAME, "popbox").text
        self.assertIn(u"注册成功", register_result)
        PaymaxUtil.echo_title(u"注册成功-即将跳转到登录页")
        print u'注册成功弹层返回>>', register_result

    #前台登录
    def web_login(self, driver, username, password):
        driver.get(self.url)
        '''登录'''
        driver.find_element_by_link_text(u"登录").click()
        driver.find_element_by_name("userName").send_keys(username)
        driver.find_element_by_name("password").send_keys(password)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-blue"))
        )
        driver.find_element_by_class_name("btn-blue").click()
        return True

    #前台退出
    def web_logout(self,driver):
        driver.find_element_by_css_selector("img.head.ng-scope").click()
        driver.find_element_by_link_text(u"登出").click()
        driver.find_element_by_css_selector("input.btn.btnDashboard").click()

    #创建应用
    def create_app(self,driver,appname):
        print u"创建应用名: %s" % appname
        index = 1           #重试次数
        driver.get(WebConfig.HOST.FRONTEND_TEST_HOST + "/web/")
        Wait.wait_until_clickable(driver=driver,by=By.XPATH,values="html/body/div/div[2]/div/ul/li[1]/div")
        driver.find_element_by_xpath("html/body/div/div[2]/div/ul/li[1]/div").click()
        driver.find_element_by_name("appName").send_keys(appname)
        Wait.wait_until_clickable(driver=driver,by=By.CSS_SELECTOR,values="input.btn.btnDashboard")
        #check"创建"按钮是否可点击,如果可以,则click
        driver.find_element_by_css_selector("input.btn.btnDashboard").click()
        time.sleep(2)
        elements = driver.find_elements_by_tag_name("h3")
        appnames = []
        for i in range(0, index, 1):
            for i in elements:
                appnames.append(i.text)
            if appname in appnames:
                print u"创建应用成功! %s" % appname
                break
            else:
                print u"未找到应用 %s" % appnames
                continue
        # print u"已经创建的应用名字们>>", appnames

    def find_app(self,driver,appname):
        driver.get(WebConfig.HOST.FRONTEND_TEST_HOST + "/web/")
        # driver.get("http://test.paymax.cc/web/#/app/list")
        elements = driver.find_elements_by_tag_name("h3")
        for i in elements:
            if i.text == appname:
                print u'找到应用 %s:进入应用详情' % appname
                i.click()
                #TODO 断言应用信息
                break
            else:
                print u"未找到应用：",appname
                RuntimeError(u"未找到应用：",appname)

    def delete_app(self,driver,appname,password):
        FrontEndWebUtil().find_app(driver=driver, appname=appname)  # 找到创建的应用，点进去
        driver.find_element_by_link_text(u"应用信息").click()
        driver.find_element_by_css_selector("div.row > button.btn.btnDashboard").click()  # 点击删除应用
        time.sleep(1)
        driver.find_element_by_css_selector("input.btn.btnDashboard").click()  # 点击确认删除

        if self.is_element_present(driver=driver,how=By.XPATH, what="//input[@type='password']") == True:  # 如果密码输入框存在
            driver.find_element_by_xpath("//input[@type='password']").clear()
            driver.find_element_by_xpath("//input[@type='password']").send_keys(password)  # 输入密码
            time.sleep(1)
            driver.find_element_by_xpath("//input[@ng-disabled='inputPwdForm.$invalid'][@type='submit']").click()
        print u"删除应用成功,应用名：%s" % appname

    #是否存在元素，True：存在  False：不存在
    def is_element_present(self,driver, how, what):
        driver.implicitly_wait(8)
        try:
            driver.find_element(by=how, value=what)
        except NoSuchElementException, e:
            return False
        return True

    #上传文件或图片
    #参数：by：定位器，value：值，up_file：上传文件绝对路径
    def upload(self,driver,by,value,up_file):

        # driver.find_element(by=by,value=value).clear()
        driver.find_element(by=by, value=value).send_keys(up_file)
        print u"上传%s图片：%s" % (value,up_file)

    #封装send_keys
    #参数：
    # how：定位方式，如By.ID
    # what：定位的元素值
    # value：要输入的值
    def send_keys(self,driver,how,what,values):
        time.sleep(0.3)             #放慢速度
        print u"填写：%s" % what
        driver.find_element(how, what).send_keys(values)

    def get(self,driver,url):
        #TODO
        index = 3           #重试次数
        for i in range(0,index,1):
            pass

    #截图方法
    #参数：driver，截图存放位置，图片命名（带格式.jpg or .png）
    def screenshots(self,driver,picname):
        if os.path.exists("/tmp/Screenshots/") == False:
            os.system("mkdir -p /tmp/Screenshots/")
        screenshots_url = "/tmp/Screenshots/"
        print screenshots_url
        screenshots = screenshots_url + picname
        driver.save_screenshot(screenshots)
        print u'截图成功'


    #查询企业审核通过，且应用小于9个的测试的商户，用于测试渠道审核
    #查询的注册手机号字段：174%
    @classmethod
    def query_merchant(cls):
        sql = "select t.merchant_id,t.phone,t.company_name,count(*) as count from (select a.phone,c.merchant_id,b.company_name from merchant.t_member as a,merchant.t_merchant_company as b,merchant.t_app as c where a.phone like '174%' and a.merchant_id = b.merchant_id and b.status = 'SUCCESS' and c.merchant_id = b.merchant_id) as t group by t.merchant_id having count <9"
        res = list(settings.db_config(db="merchant").query(sql))
        print u'174%字段，商户审核通过的个数：',len(res)
        if len(res) > 0:
            print u'商户注册手机号：', res[0].phone
            return res[0].phone,res[0].company_name        #返回第一个商户注册手机号
        else:
            #TODO 如果没有，重新走注册商户-企业认证流程（VerityCompany.py流程）
            print u"没有企业通过的商商户..."
            RuntimeError(u"没有企业认证通过的商户了.")                   #目前直接失败

    #从elements元素对象中筛选想要的元素，然后。
    #参数：elementsObj：元素对象list   例如：elementsObj = driver.find_elements(By.TAG_NAME, "span")
    def findElements(self,elementsObj,filtration):
        for i in elementsObj:
            if i.text == filtration:
                print u"选择：%s" % i.text
                time.sleep(0.5)
                i.click()

    #控制滚动条，使某元素滚动到页面最上方，使元素可见（可操作）
    #参数：element：元素对象  例如：element = driver.find_element(By.NAME, "company_department_and_job")
    def scroll_to_element(self,driver,element):
        print u"滚动滚动条到元素：",element.text
        driver.execute_script("arguments[0].scrollIntoView(true);", element)

    #渠道申请上方的导航状态,在申请过程中使用，判断上一步是否已经完成
    #注意需要等待页面彻底加载完才能使用，否则元素状态可能还是上一步的状态
    #参数：itemText：阶段的名字，如：填写申请材料
    def channel_apply_status(self,driver,itemText):
        # 渠道申请导航状态，通过class的值判断
        # done：完成  active：申请中，都没有：还没开始
        elements = driver.find_elements(By.XPATH, "//div[@ng-class='getClsByStatus(item.status, $index)']")     #申请支付渠道上方导航的元素集合
        for i in elements:
            if i.text == itemText:
                status = i.get_attribute("class")
                #如果class值有done，则完成
                self.assertIn("done",status,u"申请渠道'%s'阶段未完成，状态：%s" % (i.text, status))
                print u"申请渠道'%s'阶段完成，状态：%s" % (i.text, status)





class BackendUtil(unittest.TestCase):

    def __init__(self):
        self.url = WebConfig.HOST.BACKEND_TEST_HOST

    #后台登录方法
    def bankend_login(self,driver,username,password):
        driver.get(self.url)
        driver.find_element(By.NAME, "account").clear()
        driver.find_element(By.NAME,"account").send_keys(username)
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME,"password").send_keys(password)
        driver.find_element(By.CLASS_NAME,"reg").click()
        print u"\n\n后台登录成功：账号 %s   密码%s" % (username,password)
        time.sleep(0.5)

    #后台点击一级菜单方法
    #参数：menuname，菜单名字
    def level_1_menu(self,driver,menuname):
        elements = driver.find_elements(By.CLASS_NAME,"accordionHeader")
        for i in elements:
            if menuname in i.text:
                i.click()
                print u'\n点击一级菜单：%s' % i.text

    def level_2_menu(self,driver,menuname):
        elements = driver.find_elements(By.TAG_NAME, "a")
        for i in elements:
            if menuname in i.text:
                print u'\n点击二级菜单：%s' % i.text
                i.click()

    def level_2_menu_v2(self, driver, menuname):

        level2Menu_map = {
            u"商户基本信息" : "basic_info",
            u"支付渠道费率调整" : "rate_list",
            u"支付渠道开通审批" : "apply_audit_list",
            u"订单列表" :  "order_list",
            u"支付渠道申请订单" :  "apply_list",
            u"发票管理" :  "invoice_management",
            u"通道分润" :  "share_profit",
            u"商户资金管理" :  "capital_management",
            u"用户反馈" :  "user_feedback",
            u"线下门店列表" :  "store_list",
            u"线上商户列表" :  "online_merchant_list",
            u"销售信息列表" :  "sale_manager_list",
            u"支付二维码"  :  "PAYMENT_QRCODE",
            u"渠道管理"  :  "sale_channel",
            u"销售管理员列表"  :  "sale_administrator_list",
            u"商户列表" :  "face_merchant_list"
        }
        try:
            value = level2Menu_map[menuname]
            Wait.wait_until_clickable(driver=driver,by=By.XPATH,values="//a[@rel='%s']" % value)
            driver.find_element(By.XPATH,"//a[@rel='%s']" % value).click()
            print u'\n点击二级菜单：%s' % menuname
        except KeyError as e:
            print e
            self.fail(u"没有找到搜索字段：%s" % menuname)


    #后台搜索框输入封装
    #searchName，要搜索的字段名（需传unicode类型）
    #searchValue，要搜索的内容。
    def search_input(self,driver,searchField,searchSendKeys):

        #所有input类型的字段名对应的name属性值
        search_map = {
            u"交易管理的-商户号":"merchantNo",
            u"商户号" : "merchantId",
            u"公司名称" : "companyName",
            u"手机号码" : "phone",
            u"订单号" : "orderNo",
            u"应用名称" : "appName",
            u"门店名称" : "storeName",
            u"推广人姓名" : "recommender",
            u"销售ID" : "memberId",
            u"姓名" : "name",
            u"渠道" : "combox"
        }
        try:

            value = search_map[searchField]
            time.sleep(0.3)
            driver.find_element_by_css_selector("td > input[name=\"%s\"]" % value).send_keys("%s" % searchSendKeys)
            print u"\n搜索框：%s，%s" % (searchField,searchSendKeys)
        except KeyError as e:
            print e
            self.fail(u"没有找到搜索字段：%s" % searchField)


    #后台搜索下拉列表封装
    #searchField，要查询的字段
    #searchSelect，要选择的下拉列表值
    #PS：不能选择下拉列表第一个值，否则会报错，如果想查询第一个值，则不选，直接查询即可。
    #example： BackendUtil().search_select(driver=driver,searchField=u"状态",searchSelect=u"已通过")
    def search_select(self,driver,searchField,searchSelect):

        #所有搜索的下拉列表类型字段名对应的name属性值
        search_map = {
            u"状态":"status",
            u"商户类别":"type",
            u"结算类别":"settlementCategory",
            u"申请/交易渠道":"channelCode",
            u"基本资料状态":"baseStatus",
            u"补充资料状态":"additionalStatus",
            u"推广人类别":"partnerSource",
        }

        value = search_map[searchField]
        driver.find_element(By.XPATH, "//a[@name='%s']" % value).click()
        elements = driver.find_elements(By.TAG_NAME, 'a')
        for i in elements:
            if searchSelect == i.text:
                i.click()
        print u"\n搜索下拉列表：%s，%s" % (searchField,searchSelect)

    #后台如果存在报错alter,则停止测试
    def alter_error(self,driver):

        exists = FrontEndWebUtil().is_element_present(driver=driver,how=By.CLASS_NAME,what="alter")
        if exists == True:
            alter = driver.find_element(By.CLASS_NAME, "alert")
            return alter.text

        else:
            return None


class Wait(object):


    #等待某元素可点击
    @classmethod
    def wait_until_clickable(cls,driver,by,values):
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((by, values))
        )

    #等待某元素显示,切高宽大于0
    @classmethod
    def wait_until_visibility(cls,driver,by,values):
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((by, values))
        )

    #等待一个元素存在，并不意味着元素是可见的
    @classmethod
    def wait_until_presence(cls,driver,by,values):
        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((by, values))
        )

    #等待一个元素不显示（消失） 如渐变的JS弹出框
    @classmethod
    def wait_until_not_presence(cls,driver,by,values):
        WebDriverWait(driver, 10).until_not(
            EC.presence_of_element_located((by, values))
        )

    @classmethod
    def wait_test(cls,driver,values):
        wait = WebDriverWait(driver,10).until(lambda x: x.find_element_by_class_name(values))
        print wait.text