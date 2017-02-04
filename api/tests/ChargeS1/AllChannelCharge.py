# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import sys
import unittest
from api.model.Charge import *
from api.model.Refund import *
from api.util import HttpUtil
from api.util import PaymaxUtil
import json,random,datetime
import requests

'''
此文件是测试所有渠道的支付下单
渠道包括:
1. 支付宝移动支付
2. 微信移动支付
3. 微信公众号
4. 微信公众号（C2B扫码）支付
5. 支付宝即时到账
6. 拉卡拉 PC 网关支付
7. 拉卡拉 PC 快捷支付
8. 拉卡拉移动 SDK 支付
9. 拉卡拉 H5 支付
'''

class ALIPAY_APP(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()              #初始化body
        self.headers = HttpUtil.setHeader()         #初始化headers

    def test_alipay_app(self):
        PaymaxUtil.echo_title(u'支付宝移动支付')
        status_code,url,text = Charge.create(self.body,headers=self.headers)
        print u'地址:' + url + '\n', json.dumps(text,ensure_ascii=False)
        PaymaxUtil.TestAssertion().charge_assertion(text=text,body=self.body)

    def tearDown(self):
        pass

class WECHAT_APP(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()
        self.body['channel'] = 'wechat_app'
        self.headers = HttpUtil.setHeader()

    def test_wechat_app(self):
        PaymaxUtil.echo_title(u'微信移动支付')
        status_code,url,text = Charge.create(self.body,headers=self.headers)
        print u'地址:' + url + '\n', json.dumps(text,ensure_ascii=False)
        PaymaxUtil.TestAssertion().charge_assertion(text=text,body=self.body)


    def tearDown(self):
        pass

class WECHAT_WAP(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()
        self.body['channel'] = 'wechat_wap'
        self.body['extra'] = {"open_id":"oH_qpuKEgf7PFhp9UKPv3Ywjz6aU"}         #振华提供的open_id
        self.headers = HttpUtil.setHeader()

    def test_wechat_wap(self):
        PaymaxUtil.echo_title(u'微信公众号')
        status_code, url, text = Charge.create(self.body, headers=self.headers)
        print u'地址:' + url + '\n', json.dumps(text,ensure_ascii=False)
        PaymaxUtil.TestAssertion().charge_assertion(text=text,body=self.body)


    def tearDown(self):
        pass

class WECHAT_CSB(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()
        self.body['channel'] = 'wechat_csb'
        self.headers = HttpUtil.setHeader()

    def test_wechat_wap(self):
        PaymaxUtil.echo_title(u'微信公众号（C2B扫码）支付')
        status_code, url, text = Charge.create(self.body, headers=self.headers)
        print u'地址:' + url + '\n', json.dumps(text,ensure_ascii=False)
        self.assertEqual(text['channel'], self.body['channel'])

    def tearDown(self):
        pass

class ALIPAY_WEB(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()
        self.body['channel'] = 'alipay_web'
        self.headers = HttpUtil.setHeader()

    def test_alipay_web(self):
        PaymaxUtil.echo_title(u'支付宝即时到账')
        status_code, url, text = Charge.create(self.body, headers=self.headers)
        print u'地址:' + url + '\n', json.dumps(text,ensure_ascii=False)
        PaymaxUtil.TestAssertion().charge_assertion(text=text,body=self.body)


    def tearDown(self):
        pass

class LAKALA_WEB(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()
        self.body['channel'] = 'lakala_web'
        self.body['extra'] = { "user_id":"123","return_url":"http://www.abc.cn/"}

        self.headers = HttpUtil.setHeader()

    def test_lakala_web(self):
        PaymaxUtil.echo_title(u'拉卡拉 PC 网关支付')
        status_code, url, text = Charge.create(self.body, headers=self.headers)
        print u'地址:' + url + '\n',json.dumps(text,ensure_ascii=False)
        PaymaxUtil.TestAssertion().charge_assertion(text=text,body=self.body)


    def tearDown(self):
        pass

class LAKALA_WEB_FAST(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()
        self.body['channel'] = 'lakala_web_fast'
        self.body['extra'] = {"user_id": "123", "return_url": "http://www.abc.cn/"}
        self.headers = HttpUtil.setHeader()

    def test_lakala_web_fast(self):
        PaymaxUtil.echo_title(u'拉卡拉 PC 快捷支付')
        status_code, url, text = Charge.create(self.body, headers=self.headers)
        print u'地址:' + url + '\n',json.dumps(text,ensure_ascii=False)
        PaymaxUtil.TestAssertion().charge_assertion(text=text,body=self.body)

    def tearDown(self):
        pass

class LAKALA_APP(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()
        self.body['channel'] = 'lakala_app'
        self.body['extra'] = {"user_id":"888888"}

        self.headers = HttpUtil.setHeader()

    def test_lakala_app(self):
        PaymaxUtil.echo_title(u'拉卡拉移动 SDK 支付')
        status_code, url, text = Charge.create(self.body, headers=self.headers)
        print u'地址:' + url + '\n',json.dumps(text,ensure_ascii=False)
        PaymaxUtil.TestAssertion().charge_assertion(text=text,body=self.body)


    def tearDown(self):
        pass

class LAKALA_H5(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()
        self.body['channel'] = 'lakala_h5'
        self.body['extra'] = {
                                "user_id":"123",
                                "return_url":"http://payright.cn",
                                "show_url":"http://payright.cn"
                                }

        self.headers = HttpUtil.setHeader()

    def test_lakala_h5(self):
        PaymaxUtil.echo_title(u'拉卡拉 H5 支付')
        status_code, url, text = Charge.create(self.body, headers=self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        PaymaxUtil.TestAssertion().charge_assertion(text=text,body=self.body)


    def tearDown(self):
        pass


class TEST(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()              #初始化body
        self.headers = HttpUtil.setHeader()         #初始化headers
        self.body['time_expire'] = "1474971022000111"

#        'time_expire': int(PaymaxUtil.generate_timestamp()) + (5 * 60 * 1000),  # 失效时间

    def test_alipay_app(self):
        PaymaxUtil.echo_title(u'支付宝移动支付')
        status_code,url,text = Charge.create(self.body,headers=self.headers)
        print u'地址:' + url + '\n', json.dumps(text,ensure_ascii=False)
        PaymaxUtil.TestAssertion().charge_assertion(text=text,body=self.body)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()