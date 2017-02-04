# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import settings

if settings.API_ENV == 'PRODUCTION_1':      #ANSON的
    #线上环境
    #Paymax服务器地址
    PAYRIGHT_SERVER_URL="https://www.paymax.cc/merchant-api"

    CREATE_CHARGE = '/v1/charges'

    #APP_KEY
    PAYRIGHT_APP_KEY="app_1r75lbxeP6S2oVLK"

if settings.API_ENV == 'PRODUCTION_2':      #测移动端的
    #线上环境
    #Paymax服务器地址
    PAYRIGHT_SERVER_URL="https://www.paymax.cc/merchant-api"

    CREATE_CHARGE = '/v1/charges'

    #APP_KEY
    PAYRIGHT_APP_KEY="app_7hqF2S6GYXET457i"

if settings.API_ENV == 'TEST_OLD':
    #测试环境,老商户
    #Paymax服务器地址
    PAYRIGHT_SERVER_URL="http://172.30.21.22:9001"
    # PAYRIGHT_SERVER_URL="http://test.paymax.cc/merchant-api"

    CREATE_CHARGE = '/v1/charges'
    PAYRIGHT_APP_KEY = "app_32947b1383f049f088eb5293e6390ac3"       #自动化测试应用
    # PAYRIGHT_APP_KEY = "app_11wa6OO34y320OM8"

if settings.API_ENV == 'DEV':
    #DEV环境
    CREATE_CHARGE = '/v1/charges'
    PAYRIGHT_SERVER_URL="http://172.30.21.20:9001"
    PAYRIGHT_APP_KEY = "app_06m9Q26zL61ee55a"


if settings.API_ENV == 'TEST_NEW':
    #测试环境,新商户
    PAYRIGHT_SERVER_URL="http://172.30.21.22:9001"
    # PAYRIGHT_SERVER_URL="http://118.186.238.194:9001"           #搬家后新的外网地址
    CREATE_CHARGE = '/v1/charges'
    PAYRIGHT_APP_KEY = "app_11wa6OO34y320OM8"
