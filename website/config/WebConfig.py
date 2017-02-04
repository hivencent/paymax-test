# -*- coding: utf-8 -*-
import settings
import os

class HOST:
    if settings.WEB_ENV == 'TEST':
        #测试地址
        FRONTEND_TEST_HOST = 'http://test.paymax.cc'
        BACKEND_TEST_HOST = 'http://172.30.21.22:9006'           #搬家后新后台地址


class USER:
    pub_user = {
        "username" : "2547995165@qq.com",
        "password" : "Aa1234"
    }

    jl_user = {
        "username" : "18910505634",
        "password" : "Jinlong1990"
    }

REGISTER_PW = "Jinlong1990"

#获取python site-packages路径
from distutils.sysconfig import get_python_lib
PHANTOMJS = get_python_lib()


#上传文件路径
#获取当前执行文件的目录 + 图片
ABSPATH = unicode(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)) + "/website/data/")