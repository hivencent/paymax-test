# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import settings

if settings.API_ENV == 'PRODUCTION_1':
    #线上环境
    # Paymax提供给商户的SecretKey
    # 登录网站后查看
    PAYRIGHT_SECRET_KEY="fc03d8dd040a41d49ef3d79ad28ea357"

    # 商户自己的私钥
    # 样例 见 rsa_private_key.pem
    PrivateKey = 'rsa_private_key.pem'

    # Paymax提供给商户的公钥路径
    # 登录网站后查看,把它保存到一个pem文件中
    # 样例 见 paymax_rsa_public_key.pem
    PaymaxPublicKey = 'rsa_public_key.pem'

if settings.API_ENV == 'PRODUCTION_2':
    #线上环境
    # Paymax提供给商户的SecretKey
    # 登录网站后查看
    PAYRIGHT_SECRET_KEY="55970fdbbf10459f966a8e276afa86fa"

    # 商户自己的私钥
    # 样例 见 rsa_private_key.pem
    PrivateKey = 'rsa_private_key_product_2.pem'

    # Paymax提供给商户的公钥路径
    # 登录网站后查看,把它保存到一个pem文件中
    # 样例 见 paymax_rsa_public_key.pem
    PaymaxPublicKey = 'rsa_public_key_product_2.pem'

if settings.API_ENV == 'TEST_OLD':
    #测试环境2547995165@qq.com 的数据
    PAYRIGHT_SECRET_KEY = "27ab6b803cae4e69959543aacf0836d6"
    PrivateKey = 'rsa_private_key_test.pem'
    PaymaxPublicKey = 'rsa_public_key_test.pem'


if settings.API_ENV == 'DEV':
    #DEV环境
    PAYRIGHT_SECRET_KEY="b3fc21858fa5424cafecd338252b155c"
    PrivateKey = 'rsa_private_key_dev.pem'
    PaymaxPublicKey = 'rsa_public_key_dev.pem'

if settings.API_ENV == 'TEST_NEW':
    # 测试环境:商户18910505634的
    PAYRIGHT_SECRET_KEY = "543a09f2c7d84487a53b759c3624532f"
    PrivateKey = 'rsa_private_key_test_new.pem'
    PaymaxPublicKey = 'rsa_public_key_test_new.pem'