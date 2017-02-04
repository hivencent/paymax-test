# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


import os



def test_if():

    a = 150

    if a < 250 :
        print 'good man'
    elif a > 250:
        print 'i am lonely'
    else:
        print 'bad man'

def test_for():

    for i in xrange(1,20,1):
        print i

def test_for_1():
    a = [0,1,2,3,4,5,6]
    for i in 'ab':
        print(i)

def test_while():

    x = 1
    while x < 10:
        print x
        x += 1
        if x > 5:
            continue

#定义函数
def test_func(x,y):
    print x*y

#定义默认参数
def test_parm(b,a='hellow'):
    print a + ' ' + b

#可变参数
def test_calc(*numbers):
    a = []
    for n in numbers:
        print n,type(n)
        a.append(n)
    print a

#关键字参数
def person(name, age, **kw):
    #意义：它可以扩展函数的功能，如注册功能，必填项是必须按参数，非必填项是关键字参数。
    print('name:', name, 'age:', age, 'other:', kw)

#匿名函数
def test_lambda():
    f = lambda x:x*x
    print f(3)

def test_lambda_1():
    def test(x):
        x = x*x
        return x
    f = test(3)
    print f

#装饰器




# test_if()
# test_for()
# test_for_1()
# test_while()
# test_func(3,3)
# test_parm('hgff','123')
# test_calc(1,'2',3)

person('zhangsan',24,city='北京',city1 = 'shanghai')
# extra = {'city': 'Beijing', 'job': 'Engineer'}
# person('lisi',25,**extra)


# test_lambda_1()