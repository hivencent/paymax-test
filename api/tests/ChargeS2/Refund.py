# -*- coding: utf-8 -*-
__author__ = 'lzh'
import sys
import unittest
sys.path.append('../../../')
from api.model.Refund import *
from api.util import PaymaxUtil
from api.model.Charge import *
import json


class REFUND_TEST(unittest.TestCase):
    def setUp(self):
        self.chargeId = 'ch_e9d3a1c418785ad4f654db08'
        self.body = {'amount': 0.1, 'description': u'申请退款,订单id:%s' % self.chargeId}
        self.headers = HttpUtil.setHeader()

    #正常退款(默认退款:不提供金额和退款原因)(前提条件:已支付成功)
    def test_refund_defualt_success(self):
        #支付渠道:微信CSB
        PaymaxUtil.echo_title(u'正常退款(默认退款:不提供金额和退款原因)')
        #查询已支付的订单,即状态为:SUCCEED
        Charge.retrieve(self.chargeId,self.headers)
        self.chargeId = 'ch_663964ec0125fe3e7cc2b4c2'
        status_code, url, text = Refund.create(self.chargeId,self.body,self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 200)
        #self.assertEqual(text['id'], refundId)

    # 正常退款(提供金额和退款原因)(前提条件:已支付成功)
    def test_refund_offer_amount_success(self):
        # 支付渠道:微信CSB
        PaymaxUtil.echo_title(u'正常退款(提供金额和退款原因)')
        self.chargeId = 'ch_663964ec0125fe3e7cc2b4c2'
        self.body = {'amount': 0.1, 'description': u'就想退款,订单id:%s' % self.chargeId}
        status_code, url, text = Refund.create(self.chargeId,self.body,self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 200)
        #self.assertEqual(text['id'], refundId)

    # 未支付,进行退款
    def test_refund_not_charged(self):
        # 支付渠道:微信CSB
        PaymaxUtil.echo_title(u'未支付,进行退款。不能进行退款。')
        self.chargeId = 'ch_663964ec0125fe3e7cc2b4c2'
        status_code, url, text = Refund.create(self.chargeId, self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 400)
        # self.assertEqual(text['id'], refundId)

    # 退款金额>订单金额(前提条件:已支付成功)
    def test_refund_amount_more_than_charged(self):
        # 支付渠道:微信CSB
        PaymaxUtil.echo_title(u'退款金额>订单金额 ,退款失败。')
        self.chargeId = 'ch_663964ec0125fe3e7cc2b4c2'
        self.body['amount'] = 10
        status_code, url, text = Refund.create(self.chargeId, self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 400)

    # 退款金额=0(前提条件:已支付成功)
    def test_refund_amount_equals_zero(self):
        # 支付渠道:微信CSB
        PaymaxUtil.echo_title(u'退款失败。原因:退款金额为0')
        self.chargeId = 'ch_663964ec0125fe3e7cc2b4c2'
        self.body['amount'] = 0
        status_code, url, text = Refund.create(self.chargeId, self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 400)

    #(前提条件:1、已支付成功  2、支付渠道可以多次退款,如支付宝、微信)
    def test_multi_refund(self):
        PaymaxUtil.echo_title(u'申请退款,订单id:%s' % self.chargeId)
        status_code, url, text = Refund.create(chargeId=self.chargeId,body=self.body,headers=self.headers)
        print status_code
        print u'地址:' + url + '\n',json.dumps(text,ensure_ascii=False)


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()