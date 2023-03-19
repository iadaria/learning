from ecc import FieldElement

class Point:
    def __init__(self, x, y, a, b):
        self.x = x
        self.y = y
        self.a = a
        self.b = b
        if self.x is None and self.y is None:
            return
        if self.y ** 2 != self.x ** 3 + a * x + b:
            error = '({}, {}) is not on the curve'.format(x, y)
            raise ValueError(error)
    
    def __repr__(self):
        if self.x is None or self.y is None:
            return 'Point = 0'
        return 'Elliptic curve: y^2 = x^3 + {}x + {}\nPoint: ({}, {})'.format(self.a.num, self.b.num, self.x.num, self.y.num)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.a == other.a and self.b == other.b
    
    def __ne__(self, other):
        return not (self == other)
    
    def __rmul__(self, coefficient):
        product = self.__class__(None, None, self.a, self.b)
        for _ in range(coefficient):
            product += self
        return product
    
    def __add__(self, other):
        if self.a != other.a or self.b != other.b:
            error = 'Points {}, {} are not on the same curve'.format(self, other)
            raise ValueError(error)
        if self.x is None:
            return other
        if other.x is None:
            return self
        if self.x == other.x and self.y != other.y:
            # Бесконечно удаленная точка
            print("x = x for ({}, {}), ({}, {})".format(self.x.num, self.y.num, other.x.num, other.y.num))
            return self.__class__(None, None, self.a, self.b)
        # P1 + P2 = P3
        if self.x != other.x:
            s = (other.y - self.y) / (other.x - self.x)
            x3 = s ** 2 - self.x - other.x
            y3 = s * (self.x - x3) - self.y
            #print("s={}, x3={}, y3={}".format(s.num, x3.num, y3.num))
            return self.__class__(x3, y3, self.a, self.b)
        # P1 = -P2 or P1 + P2 = I
        if self == other:
            if isinstance(self.x, FieldElement):
                three = FieldElement(3, self.x.prime)
                two = FieldElement(2, self.x.prime)
                s = (three * (self.x ** 2) + self.a) / (two * self.y)
                x3 = s ** 2 - two * self.x
                y3 = s *(self.x - x3) - self.y
            else:
                s = (3 * (self.x ** 2) + self.a) / (2 * self.y)
                x3 = s ** 2 - 2 * self.x
                y3 = s *(self.x - x3) - self.y
                    
            return self.__class__(x3, y3, self.a, self.b)
        