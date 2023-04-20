from point import Point
from field import FieldElement

A = 0
B = 7
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
P = 2 ** 256 - 2 ** 32 - 977

class S256Field(FieldElement):
    def __init__(self, num, prime=None):
        super().__init__(num, P)

    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)

# Класс Signature для хранения величин r и s
class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return 'Signature({:x}, {:x})'.format(self.r, self.s)

# Класс S256Poin представляет собой открытую точку для секретного ключа
class S256Point(Point):
    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(A), S256Field(B)
        #if type(x) == int:
        if isinstance(x, int):
            super().__init__(S256Field(x), S256Field(y), a, b)
        else:
            # Если инициализиуем бесконечно удаленную точку, задаем координаты (x,y) непосредственно
            super().__init__(x, y, a, b)

    # Делаем метод более эффективным т/к знаем порядок конечной группы - n
    # Выполняем операция по модулю N т/к nG = 0 т/е через каждые n итераций цикла - 
    # - возвращаемся к нулю или к бесконечно удаленной точке
    def __rmul__(self, coefficient):
        coef = coefficient % N
        return super().__rmul__(coef)

    def __repr__(self):
        if self.x is None or self.y is None:
            return 'S256Poin(infinity)'
        return 'Elliptic curve: y^2 = x^3 + {}x + {}\nS256Point: ({}, {})'.format(self.a.num, self.b.num, self.x.num, self.y.num)

    # z - хэш документа, который подписываем sig
    def verify(self, z, sig):
        s_inv = pow(sig.s, N - 2, N)
        u = z * s_inv % N
        v = sig.r * s_inv % N
        total = u * G + v * self
        return total.x.num == sig.r

G = S256Point(
  0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
  0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
)
