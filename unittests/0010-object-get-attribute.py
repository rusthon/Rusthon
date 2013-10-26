class A():
    
    def __init__(self):
        self.one = 'one'
        self.constant = 21

    def get_value(self, factor):
        return self.constant * factor

a = A()
print a.one
a.two = "two"
print a.two
print a.get_value(2)
