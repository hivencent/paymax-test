# -*- coding: utf-8 -*-
import sys
sys.path.append("../")
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
from api.util import PaymaxUtil
import requests
import datetime
import util
from jpype import *
import os
from urllib import *


# 开启JVM，且指定jar包位置
jarpath = os.path.abspath('.') + '/lakala-test.jar'
startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % jarpath)

# url = "http://172.30.21.35:8080/hipos/cashier"
url = "http://172.30.21.12:8080/hipos/cashier"

headers = {
        'Content-Type': "application/x-www-form-urlencoded;charset=UTF-8",
        'cache-control': "no-cache",
    }


#开发环境默认：商户号：888055015200001    客户号：13810353268
#小萌给的商户：商户号：888057373950001   客户号：17100000003
userId = PaymaxUtil.generate_userId()
DevmerchantInfo = {"merchantId":"888055015200001","purchaserId":userId}
TestmerchantInfo = {"merchantId":"888057373950001","purchaserId":"100000"}

def PrePaymentOrder():

    PaymaxUtil.echo_title(u"预下单接口")
    print 'userId',userId

    jsonDict = {'charset': '02',
                'version': '1.0',
                'signType': 'RSA',
                'service': 'PrePaymentOrder',
                # 'clientIP':'127.0.0.1',               #可空
                'requestId': PaymaxUtil.generate_uuid(),
                'purchaserId': DevmerchantInfo["purchaserId"],           #请求号
                'merchantId': DevmerchantInfo["merchantId"],    #商户号

                'orderId': "ch_" + PaymaxUtil.generate_uuid()[0:29],
                'orderTime': datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                'totalAmount': "11",
                # # 'currency': "CNY",
                'offlineNotifyUrl': "http://120.27.34.155:8090/mercStandard/notify.jsp",
                'validUnit': "02",
                'validNum': "6",
                # 'bankBoundNo': "",  #用户银行卡绑卡号   可空
                'capCrdName': '金龙',  #持卡人姓名 可空
                'idType': "00",  #证件类型 00：身份证     可空
                'idNo': "220202199002135415",  #持卡人证件号   可空
                'crdNo': "6222081203005165770",  #银行卡号    可空
                # # 'crdExpDat': "0119",  #信用卡有效期 可空
                # # 'cvn2': "368",  #信用卡校验码   可空
                'bnkPhone': "18910505634",  #预留手机号    可空
                'productName': "api-productName测试",  #商品名
                # # 'productId': "productId",  #商品编号   可空
                'productDesc': "productDesc-%s" % PaymaxUtil.gen_now(str="%Y%m%d%H%M%S"),  #商品描述
                # # 'backParam': "test",  #原样返回给商户数据     可空
                }

    #签名加密
    jsonDict = util.sign_jar(jsonDict=jsonDict)

    r = requests.post(url, data=jsonDict, headers=headers)
    print u"请求地址：\n", r.url
    print u"返回状态吗：", r.status_code
    print u"\n返回数据：\n", r.text
    message = util.url_decode(text=r.text,str_filter="returnMessage")
    print u"\n\nmessage:\n",message
    orderId = util.url_decode(text=r.text,str_filter="orderId")
    print u"\orderId:\n",orderId
    print "\n\n"

    # PaymaxUtil.echo_title(u"发送验证码接口")
    # # orderId = "ch_37bbacf8aae811e6bbb680e65000a"
    # jsonDict = {'charset': '02',
    #             'version': '1.0',
    #             'signType': 'RSA',
    #             'service': 'PaymentSmsSend',
    #             # 'clientIP':'127.0.0.1',
    #             'requestId': PaymaxUtil.generate_uuid(),
    #             'purchaserId': userId,  # user_id: 预下单请求的时候带的
    #             'merchantId': DevmerchantInfo["merchantId"],
    #             'orderId': util.url_decode(text=r.text, str_filter="orderId"),
    #             'refNumber': '201608200002674114',
    #             }
    #
    # jsonDict = util.sign_jar(jsonDict)
    #
    # r = requests.post(url, data=jsonDict, headers=headers)
    # print u"请求地址：\n", r.url
    # print u"返回状态吗：", r.status_code
    # print u"\n返回数据：\n", r.text
    # result = util.url_decode(text=r.text, str_filter="returnMessage")
    # print u"\n\nmessage:\n", result


def PaymentSmsSend():
    PaymaxUtil.echo_title(u"发送验证码接口")
    orderId = "ch_9af3b4dcac6e11e69af780e65000a"
    userId = "83964783"

    jsonDict = {'charset':'02',
               'version':'1.0',
               'signType':'RSA',
               'service':'PaymentSmsSend',
               # 'clientIP':'127.0.0.1',
               'requestId': PaymaxUtil.generate_uuid(),
               'purchaserId':userId,     #user_id: 预下单请求的时候带的
               'merchantId':DevmerchantInfo["merchantId"],
               'orderId':orderId,
               'refNumber':'201608200002674114',
               }

    jsonDict = util.sign_jar(jsonDict)

    r = requests.post(url, data=jsonDict, headers=headers)
    print u"请求地址：\n",r.url
    print u"返回状态吗：",r.status_code
    print u"\n返回数据：\n",r.text
    result = util.url_decode(text=r.text,str_filter="returnMessage")
    print u"\n\nmessage:\n",result

def PaymentCommit():
    PaymaxUtil.echo_title(u"支付确认")

    orderId = 'ch_9af3b4dcac6e11e69af780e65000a'
    validCode = "310988"

    jsonDict = {'charset': '02',
                'version': '1.0',
                'signType': 'RSA',
                'service': 'PaymentCommit',
                # 'clientIP':'127.0.0.1',
                'requestId': PaymaxUtil.generate_uuid(),
                'merchantId': DevmerchantInfo["merchantId"],    #商户号
                'orderId': orderId,
                'validCode': validCode,
                'backParam': "api-paymentCommit",
                }

    jsonDict = util.sign_jar(jsonDict)
    r = requests.post(url, data=jsonDict, headers=headers)
    print u"请求地址：\n", r.url
    print u"返回状态吗：", r.status_code
    print u"\n返回数据：\n", r.text, type(eval(r.text))
    print u"\n\nmessage:\n", unquote(eval(r.text)['returnmessage'])

def QueryBindCard():
    PaymaxUtil.echo_title(u"查询用户签约列表")

    jsonDict = {'charset': '02',
                'version': '1.0',
                'signType': 'RSA',
                'service': 'QueryBindCard',
                # 'clientIP':'127.0.0.1',
                'requestId': PaymaxUtil.generate_uuid(),
                'purchaserId': "693199",
                'merchantId': DevmerchantInfo['merchantId'],
                }

    jsonDict = util.sign_jar(jsonDict)

    r = requests.post(url, data=jsonDict, headers=headers)
    print u"请求地址：\n", r.url
    print u"返回状态吗：", r.status_code
    print u"\n返回数据：\n", r.text
    print u"\n\nmessage:\n", util.url_decode(text=r.text, str_filter="returnmessage")

def UnbindCard():
    PaymaxUtil.echo_title(u"解约")

    jsonDict = {'charset': '02',
                'version': '1.0',
                'signType': 'RSA',
                'service': 'UnbindCard',
                # 'clientIP':'127.0.0.1',
                'requestId': PaymaxUtil.generate_uuid(),
                'purchaserId': '13810353268',       #客户号（手机号）
                'merchantId': '888055015200001',        #给商户分配的唯一标识
                'bankBoundNo': '201610250000004422',        #用户签约号
                }

    jsonDict = util.sign_jar(jsonDict)
    r = requests.post(url, data=jsonDict, headers=headers)
    print u"请求地址：\n", r.url
    print u"返回状态吗：", r.status_code
    print u"\n返回数据：\n", r.text
    result = util.url_decode(text=r.text,str_filter="returnMessage")
    print u"\n\nmessage:\n",result

if len(sys.argv) != 2:
    print u"请填写参数！"
    sys.exit()
elif sys.argv[1] == "order":
    PrePaymentOrder()               #预下单
elif sys.argv[1] == "sms":
    PaymentSmsSend()                #发送验证码
elif sys.argv[1] == "commit":
    PaymentCommit()                 #确认支付
elif sys.argv[1] == "bind":
    QueryBindCard()                 #查询签约
elif sys.argv[1] == "unbind":
    UnbindCard()                     #解约

# 关闭JVM
shutdownJVM()
