# -*- coding: utf-8 -*-
__author__ = 'lzh'
from api.model.Charge import Charge
from api.util import HttpUtil
from api.util import PaymaxUtil
import unittest
import json
from random import choice


class ChargeNormal(unittest.TestCase):
    def setUp(self):
        self.body = {'amount': 110000.03, "subject": "python subject", "body": "Your Body",
                     "order_no": HttpUtil.generate_uuid(), "channel": "lakala_web", "client_ip": "127.0.0.1",
                     "app": "app_11wa6OO34y320OM8", "currency": "CNY", "description": "aaaaaa",
                     "extra": {"user_id": "111", "return_url": "http://132.123.221.22/333/kad"}}
        self.headers = HttpUtil.setHeader()  # 初始化headers

    def test_charge_success(self):
        status_code, url, text = Charge.create(self.body, self.headers)
        print u'下单(成功) >> ' + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 200, u'返回status_code错误: %s %s' % (status_code, text))
        PaymaxUtil.TestAssertion().charge_assertion(text=text, body=self.body)

    def tearDown(self):
        pass


class OrderNo_IS_INVALID(unittest.TestCase):
    def setUp(self):
        self.body = HttpUtil.setBody()

        self.headers = HttpUtil.setHeader()
        self.body['order_no'] = PaymaxUtil.gen_strs()

    def test_orderno_is_invalid(self):
        PaymaxUtil.echo_title(u'测试非法的order_no')
        status_code, url, text = Charge.create(self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 400)
        # self.assertEqual(text['failure_code'], 'ILLEGAL_ARGUMENT')
        # self.assertEqual(text['failure_code'],'OrderNo_IS_INVALID')

    def tearDown(self):
        pass


class Amount_IS_INVALID(unittest.TestCase):
    def setUp(self):
        self.body = HttpUtil.setBody()

        self.headers = HttpUtil.setHeader()
        self.body['amount'] = -1

    def test_amount_is_invalid(self):
        PaymaxUtil.echo_title(u'测试非法的amount')
        status_code, url, text = Charge.create(self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_code'], 'ILLEGAL_ARGUMENT')
        self.assertEqual(text['failure_msg'], u'交易金额不能小于0')

    def tearDown(self):
        pass


class TimeExpireBeforeNow(unittest.TestCase):
    def setUp(self):
        self.body = HttpUtil.setBody()

        self.headers = HttpUtil.setHeader()
        self.body['time_expire'] = PaymaxUtil.getBeforeTimestamp()

    def test_time_expire_before_now(self):
        PaymaxUtil.echo_title(u'time_expire不能早于当前时间')
        status_code, url, text = Charge.create(self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_code'], 'ILLEGAL_ARGUMENT')
        self.assertEqual(text['failure_msg'], u'time_expire早于当前时间')

    def tearDown(self):
        pass


class TimeExpireAfterNow(unittest.TestCase):
    def setUp(self):
        self.body = HttpUtil.setBody()
        self.headers = HttpUtil.setHeader()
        self.body['time_expire'] = int(PaymaxUtil.generate_timestamp()) + (4 * 60 * 1000)  # PaymaxUtil.getAfterTimestamp()

    def test_time_expire_after_now(self):
        PaymaxUtil.echo_title(u'time_expire为4分钟')
        status_code, url, text = Charge.create(self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 200)

    def test_time_expire_before_now(self):
        PaymaxUtil.echo_title(u'time_expire为5分钟')
        status_code,url,text = Charge.create(self.body,self.headers)
        print u'地址:' + url + '\n', json.dumps(text,ensure_ascii=False)
        self.assertEqual(status_code,200)
        self.assertEqual(text['time_expire'], self.body['time_expire'])
        PaymaxUtil.TestAssertion().charge_assertion(text=text, body=self.body)

    def test_time_expire_order_failed(self):
        # TODO:设置订单失效时间为4分钟,等待4分钟后,判断订单的状态为:付款失败
        pass


    def tearDown(self):
        pass




class CurrencyNotExists(unittest.TestCase):
    def setUp(self):
        self.body = HttpUtil.setBody()
        self.headers = HttpUtil.setHeader()
        self.body['currency'] = 'abc_currency'

    def test_currency_not_exist(self):
        PaymaxUtil.echo_title(u'currency编码不存在')
        status_code, url, text = Charge.create(self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 400)
        # {"failure_msg": "系统内部错误", "failure_code": "SYSTEM_ERROR"}
        PaymaxUtil.TestAssertion().charge_assertion(text=text, body=self.body)

    def tearDown(self):
        pass


class ExtraParameterTest(unittest.TestCase):
    def setUp(self):
        self.body = HttpUtil.setBody()
        self.headers = HttpUtil.setHeader()

    # 测试无附加参数的支付渠道:alipay_app
    def test_alipay_app_no_extra(self):
        self.body['channel'] = 'alipay_app'
        PaymaxUtil.echo_title(u'无附加参数测试:支付宝移动支付')
        status_code, url, text = Charge.create(self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 200)
        # {"failure_msg": "系统内部错误", "failure_code": "SYSTEM_ERROR"}
        PaymaxUtil.TestAssertion().charge_assertion(text=text, body=self.body)

    # 测试无附加参数的支付渠道: wechat_app
    def test_webchat_app_no_extra(self):
        self.body['channel'] = 'wechat_app'
        PaymaxUtil.echo_title(u'无附加参数测试:微信移动支付')
        status_code, url, text = Charge.create(self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 200)
        PaymaxUtil.TestAssertion().charge_assertion(text=text, body=self.body)

    def need_extra_but_not_offer(self, channel):
        self.body['channel'] = channel
        PaymaxUtil.echo_title(u'有附加参数,但不提供--测试渠道:' + channel)
        status_code, url, text = Charge.create(self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        return status_code, url, text

    # 不提供附加参数:wechat_wap
    def test_wechat_wap_need_extra_but_not_offer(self):
        status_code, url, text =self.need_extra_but_not_offer('wechat_wap')
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_code'], 'ILLEGAL_ARGUMENT')



    # 不提供附加参数:alipay_web
    def test_alipay_web_need_extra_but_not_offer(self):
        status_code, url, text =self.need_extra_but_not_offer('alipay_web')
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_code'], 'ILLEGAL_ARGUMENT')

    # 不提供附加参数:lakala_web
    def test_lakala_web_need_extra_but_not_offer(self):
        channel='lakala_web'
        status_code, url, text =self.need_extra_but_not_offer(channel)
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_code'], 'ILLEGAL_ARGUMENT')
        self.assertEqual(text['failure_msg'], u'缺少附加参数user_id')

    def test_lakala_web_fast_need_extra_but_not_offer(self):
        channel = 'lakala_web_fast'
        status_code, url, text = self.need_extra_but_not_offer(channel)
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_code'], 'ILLEGAL_ARGUMENT')
        self.assertEqual(text['failure_msg'], u'缺少附加参数user_id')

    def test_lakala_h5_need_extra_but_not_offer(self):
        channel = 'lakala_h5'
        status_code, url, text = self.need_extra_but_not_offer(channel)
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_code'], 'ILLEGAL_ARGUMENT')
        self.assertEqual(text['failure_msg'], u'缺少附加参数user_id')

    def test_lakala_app_need_extra_but_not_offer(self):
        channel = 'lakala_app'
        status_code, url, text = self.need_extra_but_not_offer(channel)
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_code'], 'ILLEGAL_ARGUMENT')
        self.assertEqual(text['failure_msg'], u'商户用户唯一标识为空')



    # 只提供一个附加参数
    def lakala_h5_extra(self,body):
        # 拉卡拉 H5 支付
        self.body['channel'] = 'lakala_h5'
        status_code, url, text = Charge.create(body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        return status_code, url, text


    # 不提供user_id
    def test_lakala_h5_not_offer_userId(self):
        PaymaxUtil.echo_title(u'有附加参数,测试渠道:lakala_h5,缺少参数:user_id(提供return_url和show_url)')
        self.body['extra'] = {'return_url': 'http://www.abc.cn/','show_url': 'http://www.abc.cn/charge'}
        status_code, url, text = self.lakala_h5_extra(self.body)
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_msg'], u'缺少附加参数user_id')

    # 不提供return_url
    def test_lakala_h5_not_offer_return_url(self):
        PaymaxUtil.echo_title(u'有附加参数,测试渠道:lakala_h5,缺少参数:return_url(提供user_id和show_url)')
        self.body['extra'] = {'user_id': '111', 'show_url': 'http://www.abc.cn/charge'}
        status_code, url, text = self.lakala_h5_extra(self.body)
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_msg'], u'附加参数return_url')



    # 不提供show_url
    def test_lakala_h5_not_offer_show_url(self):
        PaymaxUtil.echo_title(u'有附加参数,测试渠道:lakala_h5,缺少参数:show_url(提供user_id和return_url)')
        self.body['extra'] = {'user_id': '111','return_url': 'http://www.abc.cn/'}
        status_code, url, text = self.lakala_h5_extra(self.body)
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_msg'], u'附加参数show_url')


    def test_lakala_web_not_offer_userId(self):
        PaymaxUtil.echo_title(u'有附加参数,测试渠道:lakala_web,缺少参数:user_id')
        self.not_offer_userId_extra('lakala_web')

    def test_lakala_web_fast_not_offer_userId(self):
        PaymaxUtil.echo_title(u'有附加参数,测试渠道:lakala_web_fast,缺少参数:user_id')
        self.not_offer_userId_extra('lakala_web_fast')

    def test_lakala_web_not_offer_return_url(self):
        PaymaxUtil.echo_title(u'有附加参数,测试渠道:lakala_web,缺少参数:return_url')
        self.not_offer_return_url_extra('lakala_web')

    def test_lakala_web_fast_not_offer_return_url(self):
        PaymaxUtil.echo_title(u'有附加参数,测试渠道:lakala_web_fast,缺少参数:return_url')
        self.not_offer_return_url_extra('lakala_web_fast')

    def not_offer_userId_extra(self,channel):
        self.body['channel'] = channel
        self.body['extra'] = {'return_url': 'http://www.abc.cn/'}
        status_code, url, text = Charge.create(self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_msg'], u'缺少附加参数user_id')

    def not_offer_return_url_extra(self, channel):
        self.body['channel'] = channel
        self.body['extra'] = {'user_id': '111'}
        status_code, url, text = Charge.create(self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_msg'], u'附加参数return_url')

    # 提供非法的附加参数
    def need_extra_and_offer_illegal(self, channel):
        lakalaChannelList = ['lakala_web', 'lakala_web_fast', 'lakala_app', 'lakala_h5']
        PaymaxUtil.echo_title(u'提供非法的附加参数,测试渠道:' + channel)
        self.body['channel'] = channel
        if channel in lakalaChannelList:
            self.body['extra'] = {'user_id': 'aaaaaaa'}
        elif channel == 'wechat_wap':
            self.body['extra'] = {'open_id': 'open_id_aaaaaaa'}
        elif channel == 'alipay_web':
            self.body['extra'] = {'return_url': 'aaaaaaa'}
        status_code, url, text = Charge.create(self.body, self.headers)
        print u'地址:' + url + '\n', json.dumps(text, ensure_ascii=False)
        return status_code, url, text

    # 提供非法的附加参数
    def test_lakala_all_need_extra_and_offer_illegal(self):
        lakalaChannelList = ['lakala_web', 'lakala_web_fast', 'lakala_h5']
        # 返回结果一样,所以随机选择一个支付渠道
        self.body['channel'] = choice(lakalaChannelList)
        status_code, url, text =self.need_extra_and_offer_illegal(self.body['channel'])
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_code'], 'ILLEGAL_ARGUMENT')
        self.assertEqual(text['failure_msg'], u'附加参数user_id格式不正确')

    # 提供非法的附加参数:wechat_wap
    def test_webchat_wap_need_extra_and_offer_illegal(self):
        status_code, url, text =self.need_extra_and_offer_illegal('wechat_wap')
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_code'], u'CHANNEL_CHARGE_FAILED')
        self.assertEqual(text['failure_msg'], u'向支付渠道下单失败,原因:sub_openid is invalid')

    # 提供非法的附加参数:alipay_web
    def test_alipay_web_need_extra_and_offer_illegal(self):
        status_code, url, text =self.need_extra_and_offer_illegal('alipay_web')
        self.assertEqual(status_code, 400)
        self.assertEqual(text['failure_code'], 'ILLEGAL_ARGUMENT')
        self.assertEqual(text['failure_msg'], u'附加参数return_url格式不正确')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
