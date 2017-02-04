# -*- coding: utf-8 -*-
__author__ = 'lzh'
import sys
sys.path.append('../../')
reload(sys)
from api.model.Charge import Charge
from api.util import HttpUtil
from api.util import PaymaxUtil
import unittest
import json


class CHARGE_RETRIEVE_TEST(unittest.TestCase):

    def setUp(self):
        self.headers = HttpUtil.setHeader()         #初始化headers

    def test_retrieve_success(self):
        PaymaxUtil.echo_title(u'测试:查询支付订单-成功')
        # 测试环境订单:ch_d438de8ddef777b57f89a258
        self.chargeId = 'ch_2f6bebe29a01ff962ea130f2'
        status_code,url,text = Charge.retrieve(self.chargeId,self.headers)
        self.assertEqual(status_code,200)
        self.assertEqual(text['id'],self.chargeId)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)

    def test_retrieve_not_exists(self):
        PaymaxUtil.echo_title(u'查询不存在的支付订单')
        self.chargeId = 'ch_aaaa'
        status_code, url, text = Charge.retrieve(self.chargeId, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_msg'], u'支付订单不存在')
        self.assertEqual(text['failure_code'], 'ORDER_NO_NOT_EXIST')

    def test_retrieve_chargeId_is_null(self):
        PaymaxUtil.echo_title(u'查询支付订单---支付订单号为空')
        self.chargeId = ''
        status_code, url, text = Charge.retrieve(self.chargeId,self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code,400)
        # self.assertEqual(text['failure_msg'], u'支付订单号不能为空')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()