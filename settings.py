# -*- coding: utf-8 -*-
__author__ = 'jinlong'
from web import db as dbs


# 设置接口环境参数
# PRODUCTION:线上环境
# TEST_OLD:测试环境     旧商户: 2547995165@qq.com  Aa1234
# DEV:开发环境
# TEST_NEW:        新商户:18910505634   Jinlong1990
API_ENV = 'TEST_NEW'

#设置WEB环境参数
WEB_ENV = 'TEST'

#设置数据库链接配置

def db_config(db='channel'):
    db_test = dbs.database(host="secret", port=3306, dbn='mysql', user='root', pw='secret', db='%s' % db)
    return db_test

