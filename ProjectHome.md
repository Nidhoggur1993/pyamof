Mock framework for Python 2.x and 3.x, which has taken influence from jMock.

# Installing #
Download latest version from Downloads and extract the file. Run sudo setup.py install.

Best way to see the usage is to see the test code test\_yamf.py

# Basic usage #
To set basic expectation that doSomething must be called:
```
m = yamf.Mock()
m.doSomething.mustBeCalled
```
Method can be mocked also:
```
mockMethod = yamf.MockMethod()
mockMethod.mustBeCalled
```


To verify that the doSomething was called use:

```
m.verify()
```

The verify will raise assertion if the expectations are not met.

To verify that method is not called use:

```
m.doSomethingElse.mustNotBeCalled
```

# Call counts #
To check that method is called certain times:

```
m.doSomething.mustBeCalled.once
m.doSomething.mustBeCalled.times(2)
m.doSomething.mustBeCalled.atLeastTimes(2)
```

# Arguments #
To check arguments of the method:

```
m.doSomething.mustBeCalled.withArgs(5,2)
```

To check that method is called at least two times with specific args

```
m.doSomething.mustBeCalled.withArgs(5).mustBeCalled.withArgs(6)
```

To check that method is called two times with same args

```
m.doSomething.mustBeCalled.withArgs(5).times(2)
```

# Return value #
To make a method to return value:

```
m.doSomething.returns(1)
```

This will also work

```
m.doSomething.mustBeCalled.once.returns(5)
```

# Executing #
To execute something when mock method is called:

```
def method(a,b): 
    #Do something. Note that the method return value is not given to caller

m.doSomething.execute(method) # execute takes callable
```

# History #
To find out certain call's arguments:
```
#Somewhere mock gets called like
m.doSomething(1,k=2) 
m.doSomething(5,k=6)

# calls will be [((1),{'k':2}), (5,{'k':6})]
calls = m.doSomething.history
```

# Array of mocks #
To handle situation where there are array of mocks:
```
mocks = MockArray(4)
mocks.method.mustBeCalled.times(2)
        
for mock in mocks: mock.method() 
for mock in mocks: mock.method() 
        
mocks.verify()
```

# Modules #
To verify that certain module method is called
```
m = MockModule('os')
m.getcwd.mustBeCalled
# testing...
m.verify()
```

To make the module method to return value
```
m = MockModule('os')
m.getcwd.returns('abc123')
```

# 0.7 version #
To verify all mocks at once. SHOULD NOT BE USED! HAS BUG SEE ISSUES
```
import yamf
m = yamf.Mock()
m2 = yamf.Mock()
yamf.verify()
```

To get errors when mock is accessing attributes that mocked class does not have
```
import yamf
m = yamf.Mock(MyClass)

m.method() # Generates assertion error if method is not MyClass's attribute
```

To return different values for different calls
```
import yamf
m = yamf.Mock()
m.method.returns(1).returns(2)
m.method() # returns 1
m.method() # returns 2
m.method() # returns 2
```







