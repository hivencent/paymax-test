# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import sys
sys.path.append('../../')
import platform
import HTMLTestRunner
import os
from VerityChannel import *
import unittest
import datetime

now = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

def suite():
    #test
    print "\n\n\n"
    print u"####################################################################"
    print u"######################开始测试渠道申请和审核流程########################"
    print u"####################################################################"
    print "\n\n\n"

    suite = unittest.TestSuite()
    suite.addTest(VERITY_CHANNEL('test_verity_channel'))
    # suite.addTest(VERITY_COMPANY('test_backend_verity_company'))

    suite = unittest.TestSuite((suite,))
    return suite


if __name__ == '__main__':

    if len(sys.argv) == 2 and sys.argv[1] == 'html':
        mysuit = unittest.TestSuite((suite(),))
        if platform.system() == 'Windows':
            filename = "C:\\%s_result.html" % now
        else:
            if os.path.exists('/tmp/Test_Report') == False:
                os.system('mkdir /tmp/Test_Report')
            filename = "/tmp/Test_Report/Verity_Channel.html"
            if os.path.exists(filename):
                os.system('rm %s' % filename)
        fp = file(filename,'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title=u'Paymax渠道申请和审核流程',description=u'Paymax渠道申请和审核流程')
        result = runner.run(mysuit)
        print u'已经生成测试报告 >> ',filename

        #测试概要统计
        general_report = PaymaxUtil.success_rate(result.error_count,result.failure_count,result.testsRun)
        print general_report

        PaymaxUtil.fail(result.error_count,result.failure_count)


    elif len(sys.argv) == 2 and sys.argv[1] == 'text':
        mysuit = unittest.TestSuite((suite()))
        runner = unittest.TextTestRunner()
        result = runner.run(mysuit)

        #测试概要统计
        general_report = PaymaxUtil.success_rate(len(result.errors),len(result.failures),result.testsRun)
        print general_report


    else:
        print u'参数错误！测试报告:html，控制台输出：text'
