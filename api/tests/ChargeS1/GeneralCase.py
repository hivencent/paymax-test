# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import sys
import unittest
sys.path.append('../../')
from api.model.Charge import *
from api.model.Refund import *
from api.util import HttpUtil
from api.util import PaymaxUtil
import json
import settings

'''
此文件是支付的重要的基本逻辑测试
基本测试点:
1. SecretKey为空
2. 非法的SecretKey
3. 签名校验失败
4, 应用不存在
5. 订单不存在
6. 该支付渠道未申请或者未开通
7. 金额不足
8. 进行中的退款请求只能有一笔
9. 商户订单号已存在
10. 参数错误
11. 支付渠道参数配置有误
12. 向支付渠道下单失败
13. 该支付渠道已经被冻结交易
14. 向支付渠道申请退款失败
'''


class SECRET_KEY_IS_BLANK(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()              #初始化body

        self.headers = HttpUtil.setHeader()         #初始化headers
        self.headers['Authorization'] = ''          #更新secret_key为空

    def test_secret_key_is_blank(self):
        PaymaxUtil.echo_title(u'测试SecretKey为空-SECRET_KEY_IS_BLANK')
        status_code,url,text = Charge.create(self.body,headers=self.headers)
        self.assertEqual(status_code,401)
        self.assertEqual(text['failure_code'],'SECRET_KEY_IS_BLANK')
        print u'地址:' + url + '\n', text

    def tearDown(self):
        pass

class SECRET_KEY_IS_INVALID(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()

        self.headers = HttpUtil.setHeader()
        self.headers['Authorization'] = 'Invalid_Secret_Key%'

    def test_secret_key_is_invalid(self):
        PaymaxUtil.echo_title(u'测试非法的SecretKey-SECRET_KEY_IS_INVALID')
        status_code,url,text = Charge.create(self.body,self.headers)
        self.assertEqual(status_code,401)
        self.assertEqual(text['failure_code'],'SECRET_KEY_IS_INVALID')
        print u'地址:' + url + '\n', text

    def tearDown(self):
        pass

class SIGN_CHECK_FAILED(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()

        self.headers = HttpUtil.setHeader()
        self.headers['timestamp'] = '1472638615'        # 测试数据:写死的时间戳,且不是13位

    def test_sign_check_failed(self):
        PaymaxUtil.echo_title(u'测试签名校验失败-SIGN_CHECK_FAILED')
        status_code,url,text = Charge.create(self.body,self.headers)
        self.assertEqual(status_code,401)
        self.assertEqual(text['failure_code'],'SIGN_CHECK_FAILED')
        print u'地址:' + url + '\n', text


    def tearDown(self):
        pass

class APP_NOT_EXISTED(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()
        self.body['app'] = 'app_not_existed_test'       #不存在的app_key

        self.headers = HttpUtil.setHeader()

    def test_app_not_existed(self):
        PaymaxUtil.echo_title(u'测试应用不存在-APP_NOT_EXISTED')
        status_code, url, text = Charge.create(self.body, self.headers)
        self.assertEqual(status_code,400)
        self.assertEqual(text['failure_code'],'APP_NOT_EXIST')
        print u'地址:' + url + '\n', text

    def tearDown(self):
        pass

class ORDER_NO_NOT_EXIST(unittest.TestCase):
        #调用订单查询接口
    def setUp(self):
        self.chargeId = 'test_order_not_exist'          #不存在的订单id
        self.headers = HttpUtil.setHeader()


    def test_order_not_exist(self):
        PaymaxUtil.echo_title(u'测试订单不存在-ORDER_NO_NOT_EXIST')
        status_code, url, text = Charge.retrieve(self.chargeId, self.headers)
        self.assertEqual(status_code,400)
        self.assertEqual(text['failure_code'],'ORDER_NO_NOT_EXIST')
        print u'地址:' + url + '\n', json.dumps(text,ensure_ascii=False)

    def tearDown(self):
        pass

class CHANNEL_NOT_AVAILABLE(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()
        self.body['app'] = 'app_U3nwTZyhnw221o2j'               #测试账号:ChannelNotAvailable
        self.body['channel'] = 'lakala_h5'                   #测试环境该应用lakala_h5未开通

        self.headers = HttpUtil.setHeader()

    def test_channel_not_available(self):
        PaymaxUtil.echo_title(u'测试该支付渠道未申请或者未开通-CHANNEL_NOT_AVAILABLE')
        status_code, url, text = Charge.create(self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text,ensure_ascii=False)
        self.assertEqual(status_code,400)
        self.assertEqual(text['failure_code'],'CHANNEL_NOT_AVAILABLE')

    def tearDown(self):
        pass


class AMOUNT_NOT_ENOUGH(unittest.TestCase):
    #调用申请退款接口
    #订单号: ch_a5d83653a9505467277152c9 订单金额:0.1元
    def setUp(self):
        self.chargeId = 'ch_a5d83653a9505467277152c9'
        self.body = {'amount': 11, 'description': u'金龙测试退款-金额不足'}
        self.headers = HttpUtil.setHeader()

    def test_amount_not_enough(self):
        PaymaxUtil.echo_title(u'测试退款金额不足-AMOUNT_NOT_ENOUGH')
        status_code, url, text = Refund.create(chargeId=self.chargeId,body=self.body,headers=self.headers)
        print u'地址:' + url + '\n',json.dumps(text,ensure_ascii=False)
        self.assertEqual(status_code,400)
        self.assertEqual(text['failure_code'],'AMOUNT_NOT_ENOUGH')

    def tearDown(self):
        pass

class MULTI_REFUND_RECORDS(unittest.TestCase):
    #TODO 这个case需要每次都申请一个新的退款,否则1小时候订单状态就"退款失败",待提供模拟退款接口,每次新生成一个订单支付

    def setUp(self):
        self.chargeId = 'ch_1d913791bc7a1b2e3c3898cc'
        self.body = {'amount': 0.01, 'description': u'金龙测试退款-进行中的退款请求只能有一笔'}
        self.headers = HttpUtil.setHeader()

    @unittest.skip(u"这个case需要每次都申请一个新的退款,否则1小时候订单状态就'退款失败',待提供模拟退款接口,每次新生成一个订单支付")
    def test_multi_refund_records(self):
        PaymaxUtil.echo_title(u'测试进行中的退款请求只能有一笔-MULTI_REFUND_RECORDS')
        status_code, url, text = Refund.create(chargeId=self.chargeId,body=self.body,headers=self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code,400)
        self.assertEqual(text['failure_code'],'MULTI_REFUND_RECORDS')


    def tearDown(self):
        pass

class ORDER_NO_DUPLICATE(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()
        self.body['order_no'] = '908c0bab01d94cb290fc28bacbfa3898'          #已经生成过得商户订单号
        self.headers = HttpUtil.setHeader()

    def test_order_no_duplicate(self):
        PaymaxUtil.echo_title(u'测试商户订单号已存在-ORDER_NO_DUPLICATE')
        status_code, url, text = Charge.create(self.body, self.headers)
        self.assertEqual(status_code,400)
        self.assertEqual(text['failure_code'],'ORDER_NO_DUPLICATE')
        print u'地址:' + url + '\n',json.dumps(text,ensure_ascii=False)

    def tearDown(self):
        pass

class ILLEGAL_ARGUMENT(unittest.TestCase):

    #TODO  {"failure_msg": "商户用户唯一标识为空", "failure_code": "ILLEGAL_ARGUMENT"}

    def setUp(self):
        pass

    def test_illegal_argument(self):
        self.body = HttpUtil.setBody()
        self.body['client_ip'] = '127.0.0.0.1'  # 错误的client_ip格式

        self.headers = HttpUtil.setHeader()

        PaymaxUtil.echo_title(u'测试参数错误-client ip 格式不正确')
        status_code, url, text = Charge.create(self.body, self.headers)
        self.assertEqual(status_code,400)
        self.assertEqual(text['failure_code'],'ILLEGAL_ARGUMENT')
        self.assertEqual(text['failure_msg'],u'client ip 格式不正确')
        print u'地址:' + url + '\n',json.dumps(text,ensure_ascii=False)

    def test_iglegal_argument_authorization_null(self):
        self.body = HttpUtil.setBody()
        self.headers = HttpUtil.setHeader()

        PaymaxUtil.echo_title(u'测试参数错误-原支付单支付状态不是Success,不能进行退款操作')
        self.chargeId = 'ch_ca618861ab12cee2161c009f'       #该订单状态:付款失败
        status_code, url, text = Refund.create(self.chargeId,body=self.body,headers=self.headers)
        self.assertEqual(status_code,400)
        self.assertEqual(text['failure_code'],'ILLEGAL_ARGUMENT')
        self.assertEqual(text['failure_msg'],u'原支付单支付状态不是Success,不能进行退款操作')
        print u'地址:' + url + '\n',json.dumps(text,ensure_ascii=False)

    def test_user_id_null(self):
        self.body = HttpUtil.setBody()



    def tearDown(self):
        pass

@unittest.skip(u"测试支付渠道参数配置有误,需要三方返回错误,暂时测不了")
class ILLEGAL_CHANNEL_PARAMETERS(unittest.TestCase):
    #测试数据:app_Q5R525k5HW9C9945
    #微信移动支付参数错误
    #TODO 接口返回500
    def setUp(self):
        self.body = HttpUtil.setBody()
        self.body['app'] = 'app_Q5R525k5HW9C9945'  # 测试环境该应用alipay_app未开通
        self.body['channel'] = 'wechat_app'

        self.headers = HttpUtil.setHeader()

    def test_illegal_channel_parameters(self):
        HttpUtil.echo_title(u'测试支付渠道参数配置有误-ILLEGAL_CHANNEL_PARAMETERS')
        status_code, url, text = Charge.create(self.body, self.headers)
        print status_code,url,text
        self.assertEqual(status_code, 400)

    def tearDown(self):
        pass


class CHANNEL_CHARGE_FAILED(unittest.TestCase):

    '''
    渠道:拉卡拉移动SDK渠道
    下单金额:10001
    测试准备:在拉卡拉后台配置总控规则:商户账户、终端、用户消费、收款方,单笔最大金额10000
    '''
    #TODO {"failure_msg": "向支付渠道下单失败,原因:生成支付宝支付凭据失败,请检查密钥配置", "failure_code": "CHANNEL_CHARGE_FAILED"}
    #18910505634商户,支付宝渠道

    def setUp(self):
        self.headers = HttpUtil.setHeader()

    def test_channel_charge_failed(self):

        self.body = HttpUtil.setBody()
        self.body['amount'] = 10001             #拉卡拉风控交易的下单最大限额10000(总控规则)
        self.body['channel'] = 'lakala_app'
        self.body['extra'] = {"user_id": "888888"}

        HttpUtil.echo_title(u'测试向支付渠道下单失败-下单金额超限')
        status_code, url, text = Charge.create(self.body, self.headers)
        self.assertEqual(status_code,400)
        print u'地址:' + url + '\n',json.dumps(text,ensure_ascii=False)
        self.assertEqual(text['failure_code'],'CHANNEL_CHARGE_FAILED')

    def test_channel_charge_failed_wechat_wap(self):
        self.body = HttpUtil.setBody()
        self.body['channel'] = 'wechat_wap'
        self.body['extra'] = {"open_id":"obc-jswk25IUGp3q8RPTYu083rmk"}

        HttpUtil.echo_title(u'测试向支付渠道下单失败-(微信公众号)错误的open_id')
        status_code, url, text = Charge.create(self.body, self.headers)
        self.assertEqual(status_code,400)
        print u'地址:' + url + '\n',json.dumps(text,ensure_ascii=False)
        self.assertEqual(text['failure_code'],'CHANNEL_CHARGE_FAILED')

    # 测试商户唯一标示为空
    def test_iglegal_argument_not_openid(self):
        self.body = HttpUtil.setBody()
        self.body['channel'] = 'wechat_wap'
        self.body['extra'] = {"open_id": ""}
        self.headers = HttpUtil.setHeader()

        PaymaxUtil.echo_title(u'向支付渠道下单失败,原因:JSAPI支付必须传入openid或sub_openid')
        status_code, url, text = Charge.create(body=self.body, headers=self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code,400)
        self.assertEqual(text['failure_code'],'CHANNEL_CHARGE_FAILED')

    def tearDown(self):
        pass

class CHANNEL_FREEZE(unittest.TestCase):

    def setUp(self):
        self.body = HttpUtil.setBody()
        self.body['app'] = 'app_83TIszKA9289MJ1L'       #应用名:冻结交易

        self.headers = HttpUtil.setHeader()

    def test_channel_freeze(self):
        HttpUtil.echo_title(u'测试该支付渠道已经被冻结交易-CHANNEL_FREEZE')
        status_code, url, text = Charge.create(self.body, self.headers)
        self.assertEqual(status_code,400)
        print u'地址:' + url + '\n',json.dumps(text,ensure_ascii=False)
        self.assertEqual(text['failure_code'],'CHANNEL_FREEZE')

    def tearDown(self):
        pass

class CHANNEL_REFUND_FAILED(unittest.TestCase):
    '''
    退款失败
    退款金额超过拉卡拉后台配置的最大金额:对49号上空设置上限为5000
    '''
    def setUp(self):
        self.chargeId = 'ch_87a9410f86cd3d87fa2d5341'
        self.body = {'amount': 160, 'description': u'退款金额超限'}
        self.headers = HttpUtil.setHeader()

    def test_channel_refund_failed(self):
        HttpUtil.echo_title(u'向支付渠道申请退款失败-CHANNEL_REFUND_FAILED')
        status_code, url, text = Refund.create(chargeId=self.chargeId,body=self.body,headers=self.headers)
        print status_code
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)

    def tearDown(self):
        pass


class FACE_AUTH(unittest.TestCase):
    '''
    测试人脸识别未开通下单失败
    '''
    def setUp(self):
        self.headers = HttpUtil.setHeader()

    def test_face_auth(self):
        self.body = HttpUtil.setBody()
        self.body['channel'] = 'lakala_app'
        self.body['extra'] = {"user_id": "888888"}

        HttpUtil.echo_title(u'测试人脸识别开通下单成功')
        status_code, url, text = Charge.create(self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        PaymaxUtil.TestAssertion().charge_assertion(text=text, body=self.body)

    def test_face_not_auth(self):
        self.body = HttpUtil.setBody()
        self.body['channel'] = 'lakala_app'
        self.body['extra'] = {"user_id": "test_face_not_auth"}

        HttpUtil.echo_title(u'测试人脸识别未开通下单失败-USER_FACE_NOT_AUTH')
        status_code, url, text = Charge.create(self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code,400)
        self.assertEqual(text['failure_code'],'USER_FACE_NOT_AUTH')
        self.assertEqual(text['failure_msg'],u'商户用户未进行人脸识别')

    def tearDown(self):
        #重载配置文件
        # reload(settings)
        pass

if __name__ == '__main__':
    unittest.main()
