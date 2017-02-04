# -*- coding: utf-8 -*-
__author__ = 'jinlong'
from api.config import PaymaxConfig
from ApiResource import *
import json



class Refund(object):

    @classmethod
    def create(cls,chargeId,body,headers):
        if not chargeId:
            return 'chargeId can not be blank.'
        #将body转成jon对象
        body = json.dumps(body)
        uri = PaymaxConfig.CREATE_CHARGE + '/' + chargeId + '/refunds'
        return ApiResource.request(uri=uri,body=body,headers=headers)

    @classmethod
    def retrieve(cls,chargeId,refundId,headers):
        if not chargeId or not refundId:
            return 'chargeId or refundId can not be blank.'
        uri = PaymaxConfig.CREATE_CHARGE + '/' + chargeId + '/refunds/' + refundId
        return ApiResource.request(uri=uri,headers=headers)

