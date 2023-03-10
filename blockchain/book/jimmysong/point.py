class Point:
    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        if self.x is None and self.y is None:
            return
        if y ** 2 != x ** 3 + a * x + b:
            error = '({}, {}) is not on the curve'.format(x, y)
            raise ValueError(error)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b
    
    def __ne__(self, other):
        return not (self == other)
    
    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            error = 'Points {}, {} are not on the same curve'.format(self, other)
            raise ValueError(error)
        if self.x is None:
            return other
        if other.x is None:
            return self
        if self.x == other.x and self.y != other.y:
            return self.__class__(None, None, self.a, self.b)