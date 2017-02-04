# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from api.config import PaymaxConfig
from api.config import SignConfig
from api.util import PaymaxUtil
from PaymaxUtil import *
from api.sign import RSASign
from api.exception import exception
import settings
import requests
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CERT_DIR = os.path.join(BASE_DIR, "sign")

#设置需要发送的HTTP头信息
def setHeader():
    nonce = generate_uuid()
    timestamp = generate_timestamp()
    header = {
        "Host":"www.paymax.cc",
        "Content-Type":"application/json;charset=utf-8",
        'nonce':nonce,
        "timestamp":timestamp,
        "Authorization":SignConfig.PAYRIGHT_SECRET_KEY
    }
    return header

def setBody():

    body = {'order_no': PaymaxUtil.generate_uuid(),
         'amount': 0.1,
         'subject': u'自动化测试订单_subject',
         'body': u'自动化测试订单_body',
         'channel': 'alipay_app',
         'app': '%s' % PaymaxConfig.PAYRIGHT_APP_KEY,
         'client_ip': '127.0.0.1',
         'description': 'description',
         'time_expire': int(PaymaxUtil.generate_timestamp()) + (5 * 60 * 1000),  # 失效时间
         'currency': 'CNY',
         }
    return body

#签名数据
def to_sign_data(header,method,uri,body=''):
    #默认为TEST商户密钥
    PRIVATE_KEY = os.path.join(CERT_DIR, SignConfig.PrivateKey)

    #预留:针对特定CASE更换密钥
    if settings.API_ENV == 'FACE':
        PRIVATE_KEY = os.path.join(CERT_DIR, SignConfig.PrivateKey_FACE)

    #组装签名数据，顺序必须一致
    nonce = header['nonce']
    timestamp = header['timestamp']
    Authorization = header['Authorization']
    #query目前4个接口都未空，预留参数
    query_string = ''
    sign_data = method+'\n'+uri+'\n'+query_string+'\n'+nonce+'\n'+timestamp+'\n'+Authorization+'\n'+ body
    #通过私钥签名
    sign_data = RSASign.RSASign.rsa_sign(data=sign_data,PRIVATE_KEY=PRIVATE_KEY)
    return sign_data

#验签数据
def to_verify_data(header,response_data):
    #默认为TEST商户密钥
    PaymaxPublicKey = os.path.join(CERT_DIR, SignConfig.PaymaxPublicKey)

    #预留:针对特定CASE更换密钥
    if settings.API_ENV == 'FACE':
        PaymaxPublicKey = os.path.join(CERT_DIR,SignConfig.PaymaxPublicKey_FACE)

    #验签的sign
    sign = header['sign']

    #验签的各个字段，顺序要一致
    nonce = header['nonce']
    timestamp = header['timestamp']
    Authorization = header['authorization']
    verify_data = nonce+'\n'+timestamp+'\n'+Authorization+'\n'+response_data
    verify_result = RSASign.RSASign.rsa_verify(verify_data,sign,PUBLIC_KEY=PaymaxPublicKey)
    if not verify_result:
        raise exception.InvalidResponseException("Invalid Response.[Response Data And Sign Verify Failure.]")

    if SignConfig.PAYRIGHT_SECRET_KEY != Authorization:
        raise exception.InvalidResponseException("Invalid Response.[Secret Key Is Invalid.]")

    if float(generate_timestamp()) - float(timestamp) >= 2*60*1000:
        raise exception.InvalidResponseException("Invalid Response.[Response Time Is Invalid.]")


#get请求方法
def get(uri,headers):
    #签名数据
    sign_data = to_sign_data(header=headers,method='get',uri=uri)

    #组装HTTP Header
    request_header = {'Host':headers['Host'],
                      "Content-Type":"application/json;charset=utf-8",
                      'Authorization':headers['Authorization'],
                      'nonce':headers['nonce'],
                      'timestamp':headers['timestamp'],
                      'sign':sign_data}

    url = PaymaxConfig.PAYRIGHT_SERVER_URL + uri

    try:
        r = requests.get(url=url,headers=request_header)
    except Exception as e:
        print u'请求失败：',e

    #验签
    if r.status_code < 400:
        to_verify_data(r.headers,r.text)
    return r.status_code,r.url,json.loads(r.text)

#post请求方法
def post(uri,body,headers):

    if uri == '':
        raise exception.AuthorizationException("Access url is empty")
    #签名数据
    sign_data = to_sign_data(header=headers,method='post',uri=uri,body=body)
    #组装HTTP Header
    request_header = {'Host':headers['Host'],
                      "Content-Type":"application/json;charset=utf-8",
                      'Authorization':headers['Authorization'],
                      'nonce':headers['nonce'],
                      'timestamp':headers['timestamp'],
                      'sign':sign_data}

    url = PaymaxConfig.PAYRIGHT_SERVER_URL + uri

    try:
        #发送HTTP请求
        r = requests.post(url=url,data=body,headers=request_header)
    except Exception as e:
        print u'请求失败：',e

    #验签
    if r.status_code < 400:
        to_verify_data(r.headers,r.text)
    print r.headers
    return r.status_code,r.url,json.loads(r.text)

