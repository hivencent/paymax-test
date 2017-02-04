# -*- coding: utf-8 -*-
__author__ = 'jinlong'
from paymax.model.Charge import *
from paymax.util.PaymaxUtil import *
def changeExample():

    #请求参数
    body = {'order_no':generate_uuid(),
            'amount':0.1,
            'subject':'python_测试subject',
            'body':'python_测试body',
            'channel':'alipay_app',
            'app':'%s' % PaymaxConfig.PAYRIGHT_APP_KEY,
            'client_ip':'127.0.0.1',
            'description':'description',
            'time_expire': int(generate_timestamp()) + (5*60*1000),     #失效时间
            'currency': 'CNY',
            }

    response = Charge.create(body)
    print u'下单接口返回:\n',response

    global chargeId
    chargeId = json.loads(response)['id']

changeExample()