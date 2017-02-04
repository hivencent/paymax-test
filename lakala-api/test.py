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

userId = PaymaxUtil.generate_userId()

merchantId = raw_input(u"输入商户号：")

#更换商户时需要改的地方
# sign = os.getcwd() + "/888055015200001.p12"  888010044580002        #商户证书
sign = os.getcwd() + "/" + merchantId + ".p12"          #商户证书
print u"商户证书位置:",sign
passwd = "529876"                                   #商户证书密码
merchantInfo = {"merchantId":"888055015200001","purchaserId":userId}        #更改商户号：merchantId


# 开启JVM，且指定jar包位置
jarpath = os.path.abspath('.') + '/sign.jar'
startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % jarpath)

# url = "http://172.30.21.35:8080/hipos/cashier"
url = "http://172.30.21.12:8080/hipos/cashier"

headers = {
        'Content-Type': "application/x-www-form-urlencoded;charset=UTF-8",
        'cache-control': "no-cache",
    }


#开发环境默认：商户号：888055015200001    客户号：13810353268
#小萌给的商户：商户号：888057373950001   客户号：17100000003

def PrePaymentOrder():

    PaymaxUtil.echo_title(u"预下单接口")
    # userId = raw_input(u"输入用户id(后面接口会用到)：")
    # orderType = raw_input(u"是否用四要素下单? y/n :")
    # print "\n"

    jsonDict = {'charset': '02',
                'version': '1.0',
                'signType': 'RSA',
                'service': 'PrePaymentOrder',
                # 'clientIP':'127.0.0.1',               #可空
                'requestId': PaymaxUtil.generate_uuid(),
                'purchaserId': "123321",           #userId
                'merchantId': merchantId,    #商户号

                'orderId': "or_" + PaymaxUtil.generate_uuid()[0:29],
                'orderTime': datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                'totalAmount': "11",
                # # 'currency': "CNY",
                'offlineNotifyUrl': "http://120.27.34.155:8090/mercStandard/notify.jsp",
                'validUnit': "02",
                'validNum': "6",
                'bankBoundNo': "",  #用户银行卡绑卡号   可空
                'capCrdName': '金龙',  #持卡人姓名 可空
                'idType': "00",  #证件类型 00：身份证     可空
                'idNo': "220202199002135415",  #持卡人证件号   可空
                'crdNo': "6222081203005165770",  #银行卡号    可空
                # 'crdExpDat': "0119",  #信用卡有效期 可空
                # 'cvn2': "368",  #信用卡校验码   可空
                'bnkPhone': "18910505634",  #预留手机号    可空
                'productName': "api-productName测试",  #商品名
                # # 'productId': "productId",  #商品编号   可空
                'productDesc': "productDesc-%s" % PaymaxUtil.gen_now(str="%Y%m%d%H%M%S"),  #商品描述
                # # 'backParam': "test",  #原样返回给商户数据     可空
                }

    userId = raw_input(u"输入用户id(后面接口会用到)：")
    jsonDict['purchaserId'] = userId
    # orderType = raw_input(u"是否用四要素下单? y/n :")
    #如果用四要素下单
    if len(sys.argv) != 3:
        print u"预下单接口请输入支付方式:如，python test.py order siyaosu\n" \
              u"siyaosu：用四要素下单\n" \
              u"boundno：用绑定号下单\n" \
              u"credit：用信用卡下单\n"
        sys.exit()

    if sys.argv[2] == "siyaosu":
        del jsonDict["bankBoundNo"]         #加密前，删除绑定号

        #填写四要素信息
        capCrdName = raw_input(u"输入持卡人姓名：")
        jsonDict["capCrdName"] = capCrdName
        idNo = raw_input(u"输入持卡人证件号（身份证）：")
        jsonDict["idNo"] = idNo
        crdNo = raw_input(u"输入银行卡号：")
        jsonDict["crdNo"] = crdNo
        bnkPhone = raw_input(u"输入预留手机号：")
        jsonDict["bnkPhone"] = bnkPhone

    #如果用绑定码下单
    if sys.argv[2] == "boundno":
        #加密前，删除四要素字段
        del jsonDict["capCrdName"]
        del jsonDict["idNo"]
        del jsonDict["crdNo"]
        del jsonDict["bnkPhone"]

        bankBoundNo = raw_input(u"输入用户银行卡绑定号：")
        jsonDict["bankBoundNo"] = bankBoundNo


    #签名加密
    jsonDict = util.sign_jar(jsonDict=jsonDict,sign=sign,passwd=passwd)
    print u"加密后数据：",jsonDict
    r = requests.post(url, data=jsonDict, headers=headers)
    print u"\n\n请求地址：\n", r.url
    print u"返回状态吗：", r.status_code
    print u"\n返回数据：\n", r.text
    message = util.url_decode(text=r.text,str_filter="returnMessage")
    print u"\n\n返回码描述信息:",message
    orderId = util.url_decode(text=r.text,str_filter="orderId")
    print u"订单号:",orderId
    refNumber = util.url_decode(text=r.text,str_filter="refNumber")
    print u"refNumber：",refNumber
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

    orderId = raw_input(u"输入订单号：")
    userId = raw_input(u"输入用户id：")
    refNumber = raw_input(u"输入refNumber：")
    print u"\n\n"

    jsonDict = {'charset':'02',
               'version':'1.0',
               'signType':'RSA',
               'service':'PaymentSmsSend',
               # 'clientIP':'127.0.0.1',
               'requestId': PaymaxUtil.generate_uuid(),
               'purchaserId':userId,     #user_id: 预下单请求的时候带的
               'merchantId':merchantInfo["merchantId"],
               'orderId':orderId,
               'refNumber':refNumber,
               }

    jsonDict = util.sign_jar(jsonDict=jsonDict,sign=sign,passwd=passwd)

    r = requests.post(url, data=jsonDict, headers=headers)
    print u"请求地址：\n",r.url
    print u"返回状态吗：",r.status_code
    print u"\n返回数据：\n",r.text
    result = util.url_decode(text=r.text,str_filter="returnMessage")
    print u"\n\n返回码描述信息:",result
    print u"订单号：",orderId


def PaymentCommit():
    PaymaxUtil.echo_title(u"支付确认")
    orderId = raw_input(u"输入订单号：")
    validCode = raw_input(u"输入验证码：")
    print u"\n\n"

    jsonDict = {'charset': '02',
                'version': '1.0',
                'signType': 'RSA',
                'service': 'PaymentCommit',
                # 'clientIP':'127.0.0.1',
                'requestId': PaymaxUtil.generate_uuid(),
                'merchantId': merchantInfo["merchantId"],    #商户号
                'orderId': orderId,
                'validCode': validCode,
                'backParam': "api-paymentCommit",
                }

    jsonDict = util.sign_jar(jsonDict=jsonDict,sign=sign,passwd=passwd)
    r = requests.post(url, data=jsonDict, headers=headers)
    print u"请求地址：\n", r.url
    print u"返回状态吗：", r.status_code
    print u"\n返回数据：\n", r.text, type(eval(r.text))
    print u"\n\n返回码描述信息:\n", unquote(eval(r.text)['returnmessage'])

    print u"判断支付成功是否有BankBoundNo（绑定号）,参数名我猜是：bankBoundNo"
    try:
        if unquote(eval(r.text)['bankBoundNo']):
            print unquote(eval(r.text)['bankBoundNo'])
    except:
        print u"可能没有bankBoundNo，自己在检查下返回数据。"


def QueryBindCard():
    PaymaxUtil.echo_title(u"查询用户签约列表")
    userId = raw_input(u"输入用户id：")


    jsonDict = {'charset': '02',
                'version': '1.0',
                'signType': 'RSA',
                'service': 'QueryBindCard',
                # 'clientIP':'127.0.0.1',
                'requestId': PaymaxUtil.generate_uuid(),
                'purchaserId': userId,
                'merchantId': merchantInfo['merchantId'],
                }

    jsonDict = util.sign_jar(jsonDict=jsonDict,sign=sign,passwd=passwd)

    r = requests.post(url, data=jsonDict, headers=headers)
    print u"请求地址：\n", r.url
    print u"返回状态吗：", r.status_code
    print u"\n返回数据：\n", r.text
    result = util.url_decode(text=r.text, str_filter="returnMessage")
    print u"\n\n返回码描述信息:", result


def UnbindCard():
    PaymaxUtil.echo_title(u"解约")
    userId = raw_input(u"输入用户号：")
    bankBoundNo = raw_input(u"输入用户签约号：")


    jsonDict = {'charset': '02',
                'version': '1.0',
                'signType': 'RSA',
                'service': 'UnbindCard',
                # 'clientIP':'127.0.0.1',
                'requestId': PaymaxUtil.generate_uuid(),
                'purchaserId': userId,       #客户号（手机号）
                'merchantId': merchantInfo['merchantId'],        #给商户分配的唯一标识
                'bankBoundNo': bankBoundNo,        #用户签约号
                }

    jsonDict = util.sign_jar(jsonDict=jsonDict,sign=sign,passwd=passwd)
    print u"加密后数据：",jsonDict
    r = requests.post(url, data=jsonDict, headers=headers)
    print u"请求地址：\n", r.url
    print u"返回状态吗：", r.status_code
    print u"\n返回数据：\n", r.text
    result = util.url_decode(text=r.text,str_filter="returnMessage")
    print u"\n\n返回码描述信息:\n",result

if len(sys.argv) < 2:
    print u"请填写参数！"
    print u"order：预下单 \nsms:发送验证码 \ncommit:确认支付 \nbind：查询签约 \nunbind：解约"
    sys.exit()

if sys.argv[1] == "order":
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
