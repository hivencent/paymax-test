# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('../../../')
from api.util import HttpUtil
from api.util import PaymaxUtil
import unittest
import json
from api.exception import exception
import requests
from api.config import PaymaxConfig
import hashlib




class DuiZhangDan(unittest.TestCase):

    def setUp(self):

        appointDay = raw_input("input date(20161019):")
        print u"\n渠道> ALIPAY, WECHAT, APPLE, LAKALA, UPCP"
        channelCategory = raw_input("input channel(WECHAT):")
        print u"\n类别> ALL, REFUND, SUCCESS, WITHDRAW, WECHAT_CSB"
        statementType = raw_input("input type(ALL):")
        self.body = {"appointDay":appointDay,"channelCategory":channelCategory,"statementType":statementType}

        # self.body = "appid=wx5269eef08886e3d5&bill_date=20140603&bill_type=ALL&device_info=013467007045764&mch_id=49&nonce_str=ibuaiVcKdpRxkhJA"
        # stringSignTemp = self.body + "&key=192006250b4c09247ec02edce69f6a2d"
        # m = hashlib.md5()
        # m.update(stringSignTemp)
        # self.sign = m.hexdigest().upper()
        # print 'sign>',self.sign

        self.headers = HttpUtil.setHeader()  # 初始化headers
        self.uri = "/v1/statement/download"

    def test_post(self):

        uri = self.uri
        headers = self.headers
        body = json.dumps(self.body)


        if uri == '':
            raise exception.AuthorizationException("Access url is empty")
        # 签名数据
        sign_data = HttpUtil.to_sign_data(header=headers, method='post', uri=uri, body=body)
        print u'\n签名数据',sign_data
        # 组装HTTP Header
        request_header = {'Host': headers['Host'],
                          "Content-Type": "application/json;charset=utf-8",
                          'Authorization': headers['Authorization'],
                          'nonce': headers['nonce'],
                          'timestamp': headers['timestamp'],
                          'sign': sign_data}

        url = PaymaxConfig.PAYRIGHT_SERVER_URL + self.uri

        try:
            # 发送HTTP请求
            r = requests.post(url=url, data=body, headers=request_header)
            print u"请求地址:",r.url
            print u'\n\n返回数据\n' + json.loads(r.text)

        except Exception as e:
            print u'请求失败：', e

        # 验签
        # if r.status_code < 400:
        #     to_verify_data(r.headers, r.text)
        # return r.status_code, r.url, json.loads(r.text)



    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()