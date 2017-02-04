# -*- coding: utf-8 -*-
__author__ = 'jinlong'
import sys
sys.path.append("../")
reload(sys)
from webdriver_demo import *

def suite():
    test_suite = unittest123321.makeSuite(WebdriverDemo, 'test')

    suite = unittest123321.TestSuite((test_suite,))
    return suite

mysuit = suite()
runner = unittest123321.TextTestRunner()
runner.run(mysuit)