class A:
    var = 1

    def __init__(self, inc):
        self.inc = inc

    def increment(self):
        self.var += self.inc

    def new_b(self):
        b = self.B()
        b.out()

    class B:
        def __init__(self):
            self.val = A.var

        def out(self):
            print(self.val)


a = A(3)
a.increment()
a.new_b()
