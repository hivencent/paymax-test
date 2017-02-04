# -*- coding: utf-8 -*-
__author__ = 'lzh'
import sys
sys.path.append('../../')
import platform
import HTMLTestRunner
import os

from api.tests.ChargeS1.AllChannelCharge import *
from api.tests.ChargeS1.GeneralCase import *
from api.tests.ChargeS2.ChargeTest import *
from api.tests.ChargeS2.ChargeRetrieve import *
from api.tests.ChargeS2.Refund import *
from api.tests.ChargeS2.RefundRetrieve import *

now = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

def charges2_suite():
    #下单 测试用例
    suite_1 = unittest.TestSuite(unittest.makeSuite(ChargeNormal, 'test'))
    suite_2 = unittest.TestSuite(unittest.makeSuite(OrderNo_IS_INVALID, 'test'))
    suite_3 = unittest.TestSuite(unittest.makeSuite(Amount_IS_INVALID, 'test'))
    suite_4 = unittest.TestSuite(unittest.makeSuite(TimeExpireBeforeNow, 'test'))
    suite_5 = unittest.TestSuite(unittest.makeSuite(TimeExpireAfterNow, 'test'))
    suite_6 = unittest.TestSuite(unittest.makeSuite(CurrencyNotExists, 'test'))
    suite_7 = unittest.TestSuite(unittest.makeSuite(ExtraParameterTest, 'test'))
   #suite_11 = unittest.TestSuite(unittest.makeSuite(ExtraParameterTest, 'test_lakala_h5_not_offer_'))

    #查询下单 测试用例
    suite_8 = unittest.TestSuite(unittest.makeSuite(CHARGE_RETRIEVE_TEST, 'test'))
    #TODO 待支付沙箱完成,补充退款 测试用例
    suite_9 = unittest.TestSuite(unittest.makeSuite(REFUND_TEST, 'test'))
    #查询退款订单 测试用例
    suite_10 = unittest.TestSuite(unittest.makeSuite(RefundRetrieveTest, 'test'))

    suite = unittest.TestSuite((suite_1,suite_2,suite_3,suite_4,suite_5,suite_6,suite_7,suite_8,suite_10))
    # suite = unittest.TestSuite((suite_4,))

    return suite


if __name__ == '__main__':

    if len(sys.argv) == 2 and sys.argv[1] == 'html':
        mysuit = unittest.TestSuite((charges2_suite(),))
        if platform.system() == 'Windows':
            filename = "C:\\%s_result.html" % now
        else:
            if os.path.exists('/tmp/Test_Report') == False:
                os.system('mkdir /tmp/Test_Report')
            filename = "/tmp/Test_Report/SuiteChargeS2.html"
            if os.path.exists(filename):
                os.system('rm %s' % filename)
        fp = file(filename,'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title=u'支付接口第二优先级用例',description=u'1. 包括API详细的错误代码表及示例\n2. 正常流程及非正常数据测试流程')
        result = runner.run(mysuit)
        print '已经生成测试报告 >> ',filename

        #测试概要统计
        general_report = PaymaxUtil.success_rate(result.error_count,result.failure_count,result.testsRun)
        print general_report

        if result.error_count > 0 or result.failure_count > 0:
            #如果存在error或failure的用例,测试失败
            raise RuntimeError(u'\n测试失败,详细见测试报告 >> ERROR:%s个  FAILURE:%s个\n' % (result.error_count,result.failure_count))

    elif len(sys.argv) == 2 and sys.argv[1] == 'text':
        mysuit = unittest.TestSuite((charges2_suite(),))
        runner = unittest.TextTestRunner()
        result = runner.run(mysuit)

        #测试概要统计
        general_report = PaymaxUtil.success_rate(len(result.errors),len(result.failures),result.testsRun)
        print general_report



    else:
        print '参数错误！测试报告:html，控制台输出：text'
