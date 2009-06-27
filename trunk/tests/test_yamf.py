import sys
sys.path.insert(0, '../yamf')

import unittest
from yamf import Mock, MockModule

class TestMethodCallExpectations(unittest.TestCase):

    def testMockIsCallable(self):
        m = Mock()
        self.assertEquals(m, m(5,k=5))

    def testExpectedMethodCalled(self):
        m = Mock()
        m.method.mustBeCalled
    
        m.method()
        m.verify() 

    def testExpectingCallOnlyOnce(self):
        m = Mock()
        m.method.mustBeCalled.once
    
        m.method()
        m.verify() 

    def testTooManyCalls(self):
        m = Mock()
        m.method.mustBeCalled.once
    
        m.method()
        m.method()
        self.assertRaises(AssertionError, m.verify)

    def testExpectedMethodCalledWithParams(self):
        m = Mock()
        m.method.mustBeCalled
    
        m.method(5)
        m.verify() 

    def testExpectingManyCallsOk(self):
        m = Mock()
        m.method.mustBeCalled.times(2)
    
        m.method()
        m.method()
        m.verify()  
 
    def testExpectedCallsCalledMoreThanExpected(self):
        m = Mock()
        m.method.mustBeCalled.atLeastTimes(2)
    
        m.method()
        m.method()
        m.method()
        m.verify()   

    def testExpectedCallsCalledLessThanExpected(self):
        m = Mock()
        m.method.mustBeCalled.atLeastTimes(2)
    
        m.method()
        self.assertRaises(AssertionError, m.verify)

    def testExpectingManyCallsWithArgsOk(self):
        m = Mock()
        m.method.mustBeCalled.withArgs(5).mustBeCalled.withArgs(6)
    
        # Order is not specified
        m.method(6)
        m.method(5)
        m.verify()

    def testExpectingManyCallsWithArgsFails(self):
        m = Mock()
        m.method.mustBeCalled.withArgs(5).mustBeCalled.withArgs(6)
    
        # Order is not specified
        m.method(5)
        m.method(5)
        self.assertRaises(AssertionError, m.verify)

    def testExpectingManyCallsFails(self):
        m = Mock()
        m.method.mustBeCalled.times(3)
    
        m.method()
        m.method()
        self.assertRaises(AssertionError, m.verify)

    def testAnotherExpectedMethodCalled(self):
        m = Mock()
        m.anotherMethod.mustBeCalled
        
        m.anotherMethod()
        m.verify() 

    def testExpectedMethodNotCalled(self):
        m = Mock()
        m.anotherMethod.mustBeCalled
        
        self.assertRaises(AssertionError, m.verify)

    def testNotExpectedMethodNotCalled(self):
        m = Mock()
        m.method.mustNotBeCalled
        m.verify()

    def testNotExpectedMethodCalled(self):
        m = Mock()
        m.method.mustNotBeCalled
        m.method()
        self.assertRaises(AssertionError, m.verify)      

class TestMethodCallExpectationsWithArguments(unittest.TestCase):
        
    def testExpectedMethodCalledOk(self):
        m = Mock()
        m.method.mustBeCalled.withArgs(5)

        m.method(5)
        m.verify()

    def testExpectedMethodCalledWihtoutArgs(self):
        m = Mock()
        m.method.mustBeCalled.withArgs(5)

        m.method()
        self.assertRaises(AssertionError, m.verify)

    def testExpectedMethodCalledWithWrongArgs(self):
        m = Mock()
        m.method.mustBeCalled.withArgs(5, name='a')

        m.method(5)
        self.assertRaises(AssertionError, m.verify)

class TestReturnValue(unittest.TestCase):
    
    def testSettingReturnValue(self):
        m = Mock()
        m.method.returns(5)

        self.assertEquals( m.method(), 5)

    def testReturnValueWithExpectation(self):
        m = Mock()
        m.method.mustBeCalled.returns(1)

        self.assertEquals(m.method(), 1)
        m.verify()

    def testReturnValueWithExpectationArgs(self):
        m = Mock()
        m.method.mustBeCalled.withArgs(1).returns(1)

        self.assertEquals(m.method(1), 1)
        m.verify()

class TestExecuting(unittest.TestCase):
        
    def testExecuting(self):
        m = Mock()
        executed = []
        def method(a,b):
            executed.append(True)
        m.method.execute(method)
        m.method(1,2)
        self.assertEquals(executed, [True])

class TestMockingModule(unittest.TestCase):

    def testExpectedModuleMethodCalled(self):
        m = MockModule('os')
        m.getcwd.mustBeCalled
        import os
        os.getcwd()
        m.verify()

    def testModuleMethodReturnValue(self):
        m = MockModule('os')
        m.getcwd.returns('abc123')
        import os
        self.assertEquals(os.getcwd(), 'abc123')
        

if __name__ == '__main__':
    unittest.main()