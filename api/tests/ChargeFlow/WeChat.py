# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import unittest
from api.model.Charge import *
from api.util import HttpUtil
from api.util import PaymaxUtil
import json
import datetime
import requests
import settings

'''
此文件是测试【微信移动支付】的支付流程
'''

class WECHAT(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()              #初始化body
        self.body['channel'] = 'wechat_app'
        self.headers = HttpUtil.setHeader()         #初始化headers
        self.callback_url = 'http://172.30.21.22:8888/webservice/wechat'

        self.end_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    def test_wechat_app(self):
        #下单
        PaymaxUtil.echo_title(u'微信移动支付流程')
        status_code,url,text = Charge.create(self.body,headers=self.headers)
        print u'地址:' + url + '\n', json.dumps(text,ensure_ascii=False)
        PaymaxUtil.TestAssertion().charge_assertion(text=text,body=self.body)
        print u"\n下单成功,订单号:%s" % text['id']
        #下单成功断言该订单状态为"INIT"
        sql = "select * from t_trade where order_no = '%s'" % text['id']
        order_status = list(settings.db_config(db="channel").query(sql))[0].status
        print 'order_status',order_status


        print u'\n准备支付回调 订单号:%s' % text['id']
        #模拟支付回调
        body ="""
        <xml>
		<appid><![CDATA[wx5269eef08886e3d5]]></appid>
		<bank_type><![CDATA[CFT]]></bank_type>
		<cash_fee><![CDATA[1]]></cash_fee>
		<fee_type><![CDATA[CNY]]></fee_type>
		<is_subscribe><![CDATA[N]]></is_subscribe>
		<mch_id><![CDATA[1324016301]]></mch_id>
		<nonce_str><![CDATA[s0py1skwufn79v4g7l9efta308fm3gtr]]></nonce_str>
		<openid><![CDATA[oTHduwSCygtwaCRUl9uy19toT9-o]]></openid>
		<out_trade_no><![CDATA[%s]]></out_trade_no>
		<result_code><![CDATA[SUCCESS]]></result_code>
		<return_code><![CDATA[SUCCESS]]></return_code>
		<sign><![CDATA[A9E36F1597EFB2ACD41B140047CA4922]]></sign>
		<time_end><![CDATA[%s]]></time_end>
		<total_fee>1</total_fee>
		<trade_type><![CDATA[APP]]></trade_type>
		<transaction_id><![CDATA[4005722001201608252200279911]]></transaction_id>
	    </xml>
        """ % (text['id'],self.end_time)

        print u"请求body:\n",body

        r = requests.post(url=self.callback_url,data=body)
        print '请求地址:' + r.url + '\n微信移动支付返回结果:\n' + r.text
        self.assertEqual(r.text,'success')



    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()