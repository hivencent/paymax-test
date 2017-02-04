# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import sys
sys.path.append('../../')
import platform
import HTMLTestRunner
import os

from api.tests.ChargeS1.AllChannelCharge import *
from api.tests.ChargeS1.GeneralCase import *

now = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")

def general_suite():
    # suite = unittest.TestSuite()
    # suite.addTest(SECRET_KEY_IS_BLANK('test_secret_key_is_blank'))
    # suite.addTest(SECRET_KEY_IS_INVALID('test_secret_key_is_invalid'))
    # suite.addTest(ChargeRetrieve('test_retrieve_success'))
    print u"测试环境：%s" % settings.API_ENV
    print u"测试支付接口异常情况."

    suite_1 = unittest.TestSuite(unittest.makeSuite(SECRET_KEY_IS_BLANK,'test'))
    suite_2 = unittest.TestSuite(unittest.makeSuite(SECRET_KEY_IS_INVALID,'test'))
    suite_3 = unittest.TestSuite(unittest.makeSuite(SIGN_CHECK_FAILED,'test'))
    suite_4 = unittest.TestSuite(unittest.makeSuite(APP_NOT_EXISTED,'test'))
    suite_5 = unittest.TestSuite(unittest.makeSuite(ORDER_NO_NOT_EXIST,'test'))
    suite_6 = unittest.TestSuite(unittest.makeSuite(CHANNEL_NOT_AVAILABLE,'test'))
    suite_7 = unittest.TestSuite(unittest.makeSuite(AMOUNT_NOT_ENOUGH,'test'))
    suite_8 = unittest.TestSuite(unittest.makeSuite(MULTI_REFUND_RECORDS,'test'))
    suite_9 = unittest.TestSuite(unittest.makeSuite(ORDER_NO_DUPLICATE,'test'))
    suite_10 = unittest.TestSuite(unittest.makeSuite(ILLEGAL_ARGUMENT,'test'))
    suite_11 = unittest.TestSuite(unittest.makeSuite(ILLEGAL_CHANNEL_PARAMETERS,'test'))      #测试支付渠道参数配置有误,需要三方返回错误,暂时测不了
    suite_12 = unittest.TestSuite(unittest.makeSuite(CHANNEL_CHARGE_FAILED,'test'))
    suite_13 = unittest.TestSuite(unittest.makeSuite(CHANNEL_FREEZE,'test'))
    suite_14 = unittest.TestSuite(unittest.makeSuite(CHANNEL_REFUND_FAILED,'test'))
    suite_15 = unittest.TestSuite(unittest.makeSuite(FACE_AUTH,'test'))

    suite = unittest.TestSuite((suite_1,suite_2,suite_3,suite_4,suite_5,suite_6,suite_7,suite_8,suite_9,suite_10,suite_11,
                                suite_12,suite_13,suite_14,suite_15,))
    # suite = unittest.TestSuite((suite_11,))
    return suite

def all_channel_suite():
    print u"测试支付接口所有渠道下单成功.\n"

    suite_1 = unittest.TestSuite(unittest.makeSuite(ALIPAY_APP,'test'))
    suite_2 = unittest.TestSuite(unittest.makeSuite(WECHAT_APP,'test'))
    suite_3 = unittest.TestSuite(unittest.makeSuite(WECHAT_WAP,'test'))
    suite_4 = unittest.TestSuite(unittest.makeSuite(WECHAT_CSB,'test'))
    suite_5 = unittest.TestSuite(unittest.makeSuite(ALIPAY_WEB,'test'))
    suite_6 = unittest.TestSuite(unittest.makeSuite(LAKALA_WEB,'test'))
    suite_7 = unittest.TestSuite(unittest.makeSuite(LAKALA_WEB_FAST,'test'))
    suite_8 = unittest.TestSuite(unittest.makeSuite(LAKALA_APP,'test'))
    suite_9 = unittest.TestSuite(unittest.makeSuite(LAKALA_H5,'test'))

    # suite = unittest.TestSuite((suite_1,suite_2,suite_3,suite_4,suite_5,suite_6,suite_7,suite_8,suite_9,))
    suite = unittest.TestSuite((suite_1,))

    return suite


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'html':
        mysuit = unittest.TestSuite((general_suite(),all_channel_suite(),))
        if platform.system() == 'Windows':
            filename = "C:\\SuiteChargeS1.html"       #设置测试报告的位置
        else:
            #测试报告设置
            if os.path.exists('/tmp/Test_Report') == False:
                os.system('mkdir /tmp/Test_Report')
            filename = "/tmp/Test_Report/SuiteChargeS1.html"
            if os.path.exists(filename):
                os.system('rm %s' % filename)

            #环境变量设置
            # os.putenv()
        fp = file(filename,'wb')
        runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title=u'支付接口第一优先级用例',description=u'1. 包括API详细的错误代码表及示例\n2. 所有的下单流程')
        result = runner.run(mysuit)
        print '已经生成测试报告 >> ',filename

        #测试概要统计
        general_report = PaymaxUtil.success_rate(result.error_count,result.failure_count,result.testsRun)
        print general_report

        PaymaxUtil.fail(result.error_count,result.failure_count)

    elif len(sys.argv) == 2 and sys.argv[1] == 'text':
        mysuit = unittest.TestSuite((general_suite(),all_channel_suite(),))
        runner = unittest.TextTestRunner()
        result = runner.run(mysuit)

        #测试概要统计
        general_report = PaymaxUtil.success_rate(len(result.errors),len(result.failures),result.testsRun)
        print general_report



    else:
        print '参数错误！测试报告:html，控制台输出：text'
