import types

class MockModule(object):
    """For mocking module"""
        
    def __init__(self, moduleNameOrModule):
        """Module can be given as string or the module itself"""
        if type(moduleNameOrModule) is types.StringType:
            self._module = __import__(moduleNameOrModule, globals(), locals(), [], -1)
        else:
            self._module = moduleNameOrModule
        self._mock = Mock()

    def __getattr__(self, name):
        mockedAttr = getattr(self._mock, name)
        setattr(self._module, name, mockedAttr)
        return mockedAttr

    def verify(self):
        self._mock.verify()

class Mock(object):

    def __init__(self):
        self._mockMethods = {}

    def verify(self):
        map(lambda method: method.mockVerify(), self._mockMethods.values())

    def __getattr__(self, name):
        if name not in self._mockMethods:
            mockMethod = MockMethod(name)
            self._mockMethods[name] = mockMethod
        return self._mockMethods[name]

    def __call__(self, *args, **kwargs):
        return self
        
class CallExpectation(object):
    
    def __init__(self, mockMethod):
        self.mockIsCalled = False
        self.mockMethod = mockMethod
        self.mockExpectedArgs = None
        self.mockExpectedKwargs = None
        self.mockExpectedCallCount = None
        self.mockReceivedCalls = 0

    def mockVerify(self):   
        assert self.mockIsCalled, 'Method %s(%s,%s) was not called' \
            % (self.mockMethod.mockMethodName, self.mockExpectedArgs,self.mockExpectedKwargs)
        
        self.mockVerifyCallCount()


    def mockSetExpectedArgs(self, *args, **kwargs):
        self.mockExpectedArgs = args
        self.mockExpectedKwargs = kwargs
        return self.mockMethod

    def mockSetExpectedCallCount(self, count):
        self.mockExpectedCallCount = count
        return self.mockMethod

    def mockVerifyCallCount(self):
        assert 'FAILURE: verify call count not set'

    def mockVerifyCallCountExactly(self):
        if self.mockExpectedCallCount:
            assert self.mockReceivedCalls == self.mockExpectedCallCount, \
                'Method %s was called %d times, but expectations was %d times' \
                    % (self.mockMethod.mockMethodName, self.mockReceivedCalls, self.mockExpectedCallCount)

    def mockVerifyCallCountAtLeast(self):
        if self.mockExpectedCallCount:
            assert self.mockReceivedCalls >= self.mockExpectedCallCount, \
                'Method %s was called %d times, but expectations was at least %d times' \
                    % (self.mockMethod.mockMethodName, self.mockReceivedCalls, self.mockExpectedCallCount)

    def __getattr__(self,name):
        if name == 'withArgs':
            return self.mockSetExpectedArgs
        elif name == 'once':
            self.mockVerifyCallCount = self.mockVerifyCallCountExactly
            return self.mockSetExpectedCallCount(1)
        elif name == 'times':
            self.mockVerifyCallCount = self.mockVerifyCallCountExactly
            return self.mockSetExpectedCallCount
        elif name == 'atLeastTimes':
            self.mockVerifyCallCount = self.mockVerifyCallCountAtLeast
            return self.mockSetExpectedCallCount
        else:
            return self.mockMethod.__getattr__(name)

    def __call__(self, *args, **kwargs):
        if self.mockExpectedArgs:
            if self.mockExpectedArgs != args:
                return
        if self.mockExpectedKwargs:
            if self.mockExpectedKwargs != kwargs:
                return
        self.mockIsCalled = True
        self.mockReceivedCalls += 1

class CallNotExpected(object):
    
    def __init__(self, mockMethod):
        self.mockIsCalled = False
        self.mockMethod = mockMethod

    def mockVerify(self):   
        assert not self.mockIsCalled, "Method %s was called" % (self.mockMethod.mockMethodName)

    def mockIsOk(self):
        return not self.mockIsCalled

    def __getattr__(self,name):
        return self.mockMethod.__getattr__(name)

    def __call__(self, *args, **kwargs):
        self.mockIsCalled = True

    

class MockMethod(object):
    
    def __init__(self, methodName):
        self.mockMethodName = methodName
        self.mockExpectations = []
        self.mockMethodCallable = None

    def mockVerify(self):
        map(lambda expectation: expectation.mockVerify(), self.mockExpectations)

    def mockSetReturnValue(self, value):
        self.returnValue = value
    
    def mockMethodToBeCalled(self, method):
        self.mockMethodCallable = method

    def __getattr__(self,name):
        if name == 'mustBeCalled':
            expectation = CallExpectation(self)
            self.mockExpectations.append(expectation)
            return expectation
        elif name == 'mustNotBeCalled':
            expectation = CallNotExpected(self)
            self.mockExpectations.append(expectation)
            return expectation
        elif name == 'returns':
            return self.mockSetReturnValue
        elif name == 'execute':
            return self.mockMethodToBeCalled

    def __call__(self, *args, **kwargs):
        for expectation in self.mockExpectations:
            expectation(*args, **kwargs)
            #if expectation.mockIsOk():
            #    self.mockExpectations.remove(expectation)
            #    break
        if self.mockMethodCallable:
            self.mockMethodCallable(*args, **kwargs)
        return self.returnValue
