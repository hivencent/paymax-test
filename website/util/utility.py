# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import random
import os


class UTILITY(object):

    #生成随机手机号
    @classmethod
    def random_phone(cls):
        RandomPhone = str(174) + str(random.randrange(10000000,99999999))
        # print '生成的随机手机号是： ' , RandomPhone
        return RandomPhone

    #根生成随机应用名字
    @classmethod
    def gen_appname(cls,TYPE):
        return u"%s自动化测试应用_%s" % (TYPE,str(random.randint(1000,9999)))


    @classmethod
    def create_log_path(cls,log_path):
        if os.path.exists(log_path) == False:
            os.system('mkdir -p %s' % log_path)