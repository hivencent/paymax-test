# -*- coding: utf-8 -*-
__author__ = 'jinlong'
from api.util import HttpUtil
from api.config import SignConfig
from api.exception import exception



def _validateParams():
    if not SignConfig.PAYRIGHT_SECRET_KEY:
        raise exception.AuthorizationException("Secret key can not be blank.")

    if not SignConfig.PrivateKey:
        raise exception.AuthorizationException("The Path of RSA Private Key can not be blank.")

    if not SignConfig.PaymaxPublicKey:
        raise exception.AuthorizationException("The Path of Paymax Public Key can not be blank.")

class ApiResource(object):

    _validateParams()

    @classmethod
    def request(cls,uri,body='',headers = ''):

        if not body:
            return HttpUtil.get(uri,headers)

        else:
            return HttpUtil.post(uri,body,headers=headers)

