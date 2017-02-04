# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import uuid
import time
import unittest
from timeit import reindent
import datetime
import random


#生成一次性随机串
def generate_uuid():
    nonce = str(uuid.uuid1()).replace('-','')
    return nonce

#当前时间时间戳,毫秒
#time_now是时间戳
def generate_timestamp(time_now = time.time()):

    timestamp = "%d" % (time_now * 1000)
    return timestamp

def generate_userId():
    userId = "8" + str(random.randint(1000000, 9999999))
    return userId

def echo_title(name):
    echo_title = '\n' + '#' * 40 + '%s' % name +  '#' * 40
    print echo_title

def success_rate(error_count,failure_count,testsRun):
    #统计成功率
    success_rate = round((1 - ((float(error_count) + float(failure_count)) / float(testsRun))) * 100, 2)
    #概要结果
    message = '测试结果概要 >> run=%s errors=%s failures=%s 通过率=%s%%' % (testsRun, error_count, failure_count, success_rate)

    return reindent("""
            #########################################################################
            ## %s
            ## 详细结果查看测试报告
            #########################################################################
            """ % message, 0)

def gen_now(str):
    return datetime.datetime.now().strftime("%s" % str)

def trade_no():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(10000000000000,99999999999999))

#随机产生字符串
def gen_strs():
    str=random.sample('abcdefghijklmnopqrstuvwxyz!@#$%^&*(),.:"', random.randint(1,20))
    return str

#获取当前时间-5分钟
def getBeforeTimestamp():
    #当前时间减5分钟
    time_now = (datetime.datetime.now() - datetime.timedelta(seconds=-300))
    #转换为时间戳
    timeStamp = int(time.mktime(time_now.timetuple()))
    print timeStamp
    return timeStamp

#获取当前时间+4分钟
def getAfterTimestamp():
    # 当前时间+4分钟
    print datetime.datetime.now().timetuple()
    time_now = (datetime.datetime.now() + datetime.timedelta(minutes=20))
    # 转换为时间戳
    aftertimeStamp = int(time.mktime(time_now.timetuple()))


    print aftertimeStamp
    return aftertimeStamp

def fail(error_count,failure_count):
    #如果存在错误或失败的case，测试失败
    if error_count > 0 or failure_count > 0:
        # 如果存在error或failure的用例,测试失败
        raise RuntimeError(u'\n测试失败,详细见测试报告 >> ERROR:%s个  FAILURE:%s个\n' % (error_count,failure_count))


class TestAssertion(unittest.TestCase):

    def __init__(self):
        pass

    def charge_assertion(self,text,body):
        #下单的断言集合
        self.assertEqual(text['channel'], body['channel'])
        self.assertTrue(text['amount'] == body['amount'])
        self.assertEqual(text['order_no'], body['order_no'])
        self.assertIsNotNone(text['id'])
        self.assertEqual(text['id'][0:2], 'ch')  # 断言id以ch开头
        self.assertNotEqual(text['credential'], '') or self.assertIsNotNone(text['credential'])  # 断言credential不为空
        self.assertTrue(text['credential'].has_key(text['channel']))  # 断言credential（key）和 channel一致
        self.assertEqual(text['status'], 'PROCESSING')
