# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import sys
sys.path.append('../../')
import platform
import HTMLTestRunner
import os
from ChargeFlow.Alipay import *
from ChargeFlow.WeChat import *
from ChargeFlow.Lakala import *
import unittest

now = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

def suite():
    suite_1 = unittest.TestSuite(unittest.makeSuite(ALIPAY_WEB,'test'))
    suite_2 = unittest.TestSuite(unittest.makeSuite(ALIPAY_APP,'test'))
    suite_3 = unittest.TestSuite(unittest.makeSuite(WECHAT,'test'))
    suite_4 = unittest.TestSuite(unittest.makeSuite(LAKALA_WEB,'test'))
    suite_5 = unittest.TestSuite(unittest.makeSuite(LAKALA_H5,'test'))
    suite_6 = unittest.TestSuite(unittest.makeSuite(LAKALA_APP,'test'))
    suite_7 = unittest.TestSuite(unittest.makeSuite(LAKALA_WEB_FAST,'test'))

    suite = unittest.TestSuite((suite_1,suite_2,suite_3,suite_4,suite_5,suite_6,suite_7))
    # suite = unittest.TestSuite((suite_7,))

    return suite


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'html':
        mysuit = unittest.TestSuite((suite(),))
        if platform.system() == 'Windows':
            filename = "C:\\%s_result.html" % now
        else:
            if os.path.exists('/tmp/Test_Report') == False:
                os.system('mkdir /tmp/Test_Report')
            filename = "/tmp/Test_Report/SuiteChargeFlow.html"
            if os.path.exists(filename):
                os.system('rm %s' % filename)
        fp = file(filename,'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title=u'支付接口流程测试',description=u'商户下单-支付成功-退款申请')
        result = runner.run(mysuit)
        print '已经生成测试报告 >> ',filename

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
