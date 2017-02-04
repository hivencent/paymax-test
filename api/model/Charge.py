# -*- coding: utf-8 -*-
__author__ = 'jinlong'
from api.config import PaymaxConfig
from ApiResource import *
import json

class Charge(object):

    def __init__(self):
        pass

    @classmethod
    def create(cls,body,headers):

        #将body转成json对象
        body = json.dumps(body)
        #请求地址
        uri = str(PaymaxConfig.CREATE_CHARGE)
        return ApiResource.request(uri=uri,body=body,headers=headers)

    @classmethod
    def retrieve(cls,chargeId,headers):
        uri = PaymaxConfig.CREATE_CHARGE + '/' + chargeId
        # if not chargeId:
        #     return 'chargeId can not be blank.'
        return ApiResource.request(uri=uri,headers=headers)