import random

class SomeObj:
    def __init__(self):
        print("SomeObj init")
        self.test_val = random.random()

class RealRoot:
    def __init__(self, some_value):
        print("RealRoot init")
        self.some_value = some_value

class Root:
    def __init__(self, some_value):
        if hasattr(self, '_init_done'):
            return
        else:
            self._init_done = True
            
        print("Root init")
        RealRoot.__init__(self, some_value)
        self.some_obj = SomeObj()


class A(Root):
    def __init__(self, some_value):
        Root.__init__(self, some_value)
        print("A init")

    def do_A(self):
        print(f"Doing A with {self.some_value} - {self.some_obj.test_val}")


class B(Root):
    def __init__(self, some_value):
        Root.__init__(self, some_value)
        print("B init") 

    def do_B(self):
        print(f"Doing B with {self.some_value} - {self.some_obj.test_val}")


class Full(A, B):
    def __init__(self, some_value):
        A.__init__(self, some_value)
        B.__init__(self, some_value)


full = Full("test value")
full.do_A()
full.do_B()