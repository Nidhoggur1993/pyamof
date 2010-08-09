import sys
import os
sys.path.insert(0, os.path.pardir)
import unittest

from yamf import MockMethod

class TestMockMethod(unittest.TestCase):

    def testMockMethodCalled(self):
        method = MockMethod()
        method.mustBeCalled
        method()
        method.verify()

    def testMockMethodNotCalled(self):
        method = MockMethod()
        method.mustBeCalled
        self.assertRaises(AssertionError, method.verify)
