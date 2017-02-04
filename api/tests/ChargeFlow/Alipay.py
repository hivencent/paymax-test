# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import unittest
from api.model.Charge import *
from api.util import HttpUtil
from api.util import PaymaxUtil
import json
import requests

'''
此文件是测试【支付宝即时到账、支付宝移动支付】的支付流程
'''

class ALIPAY_WEB(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()              #初始化body
        self.body['channel'] = 'alipay_web'
        self.headers = HttpUtil.setHeader()         #初始化headers
        self.callback_url = 'http://172.30.21.22:8888/webservice/alipay_web'


    def test_alipay_web(self):
        #下单
        PaymaxUtil.echo_title(u'支付宝即时到账流程')
        status_code,url,text = Charge.create(self.body,headers=self.headers)
        print u'地址:' + url + '\n', json.dumps(text,ensure_ascii=False)
        PaymaxUtil.TestAssertion().charge_assertion(text=text,body=self.body)       #封装的支付断言

        print u"\n下单成功,订单号:%s" % text['id']

        print u'\n准备支付回调 订单号:%s' % text['id']
        #模拟支付回调
        param = {"buyer_id":"2088702215837421",
                 "trade_no":"%s" % PaymaxUtil.trade_no,
                 "body":"测试001",
                 "notify_time":"2016-09-09 17:47",
                 "use_coupon":"N",
                 "subject":"测试001",
                 "sign_type":"MD5",
                 "is_total_fee_adjust":"N",
                 "notify_type":"trade_status_sync",
                 "gmt_close":"2016-09-09 17:47:33",
                 "out_trade_no":"%s" % text['id'],
                 "trade_status":"TRADE_FINISHED",
                 "gmt_payment":"%s" % PaymaxUtil.gen_now(str="%Y-%m-%d %H:%M:%S"),
                 "discount":"0.00",
                 "sign":"d6610596790d19569c4222fc2e5865b3",
                 "buyer_email":"18521568091",
                 "gmt_create":"%s" % PaymaxUtil.gen_now(str="%Y-%m-%d %H:%M:%S"),
                 "price":self.body['amount'],           #全部退款
                 "total_fee":self.body['amount'],
                 "quantity":"1",
                 "seller_id":"2088911369891184",
                 "seller_email":"18601088140@163.com",
                 "notify_id":"f19fe6cb69d5aa49f0e9b703376feafj8q",
                 "payment_type":"1"
                 }

        # print param
        r = requests.post(url=self.callback_url,params=param)
        print '请求地址:' + r.url + '\n支付宝即时到账回调返回结果:\n' + r.text
        self.assertEqual(r.text,"success")

    def tearDown(self):
        pass

class ALIPAY_APP(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()  # 初始化body
        self.body['channel'] = 'alipay_app'
        self.headers = HttpUtil.setHeader()  # 初始化headers
        self.callback_url = 'http://172.30.21.22:8888/webservice/alipay_app'

    def test_alipay_app(self):
        # 下单
        PaymaxUtil.echo_title(u'支付宝移动支付流程')
        status_code, url, text = Charge.create(self.body, headers=self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        PaymaxUtil.TestAssertion().charge_assertion(text=text,body=self.body)

        print u"\n下单成功,订单号:%s" % text['id']

        print u'\n准备支付回调 订单号:%s' % text['id']
        # 模拟支付回调
        param = {"buyer_id":"2088702215837421",
                 "trade_no":"%s" % PaymaxUtil.trade_no,
                 "use_coupon":"N",
                 "notify_time": "2016-09-09 17:47",
                 "subject":u"模拟支付宝移动支付回调",
                 "sign_type":"RSA",
                 "is_total_fee_adjust":"N",
                 "notify_type":"trade_status_sync",
                 "out_trade_no":"%s" % text['id'],
                 "trade_status":"TRADE_SUCCESS",
                 "gmt_payment":"%s" % PaymaxUtil.gen_now(str="%Y-%m-%d %H:%M:%S"),
                 "discount":"0.00",
                 "sign":"d6610596790d19569c4222fc2e5865b3",
                 "buyer_email":"18521568091",
                 "gmt_create":"%s" % PaymaxUtil.gen_now(str="%Y-%m-%d %H:%M:%S"),
                 "price":self.body['amount'],
                 "total_fee":self.body['amount'],
                 "quantity":"1",
                 "seller_id":"2088911369891184",
                 "seller_email":"18601088140@163.com",
                 "notify_id":"f19fe6cb69d5aa49f0e9b703376feafj8q",
                 "payment_type":"1"
                 }

        r = requests.post(url=self.callback_url, params=param)
        print '请求地址:' + r.url + '\n支付宝移动支付回调返回结果:\n' + r.text
        self.assertEqual(r.text, "success")

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()