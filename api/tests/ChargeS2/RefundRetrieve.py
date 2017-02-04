# -*- coding: utf-8 -*-
__author__ = 'lzh'
import sys
import unittest
sys.path.append('../../')
from api.model.Refund import *
from api.util import HttpUtil
from api.util import PaymaxUtil
import json


class RefundRetrieveTest(unittest.TestCase):

    def setUp(self):
        self.headers = HttpUtil.setHeader()

    # 支付订单号 和 退款订单号 都存在
    def test_retrieve_success(self):
        #支付渠道:微信CSB
        self.chargeId = 'ch_663964ec0125fe3e7cc2b4c2'
        refundId='re_650c839331f66962bd0e6452'
        PaymaxUtil.echo_title(u'退款订单查询:成功')
        status_code, url, text = Refund.retrieve(self.chargeId,refundId, self.headers)
        self.assertEqual(status_code, 200)
        self.assertEqual(text['id'], refundId)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)

    # 正确的支付订单号,错误的退款订单号
    def test_retrieve_refundId_not_exists(self):
        PaymaxUtil.echo_title(u'退款订单查询:查询不存在的退款订单')
        chargeId = 'ch_663964ec0125fe3e7cc2b4c2'
        refundId='re_aaaa'
        status_code, url, text = Refund.retrieve(chargeId,refundId, self.headers)
        self.assertEqual(status_code, 400)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(text['failure_msg'], u'退款订单不存在')
        self.assertEqual(text['failure_code'], 'ORDER_NO_NOT_EXIST')

    # 错误的支付订单号,正确的退款订单号
    def test_retrieve_chargeId_not_exists(self):
        PaymaxUtil.echo_title(u'退款订单查询:查询不存在的支付订单')
        chargeId = 'ch_1111111111'
        refundId = 're_650c839331f66962bd0e6452'
        status_code, url, text = Refund.retrieve(chargeId,refundId, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_msg'], u'支付订单不存在')
        self.assertEqual(text['failure_code'], 'ORDER_NO_NOT_EXIST')

    # 不存在的支付订单号,不存在的退款订单号
    def test_retrieve_allId_not_exists(self):
        PaymaxUtil.echo_title(u'退款订单查询:查询不存在的支付订单、不存在的退款订单号')
        chargeId = 'ch_1111111111'
        refundId = 're_2222222222'
        status_code, url, text = Refund.retrieve(chargeId, refundId, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_msg'], u'支付订单不存在')
        self.assertEqual(text['failure_code'], 'ORDER_NO_NOT_EXIST')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()