import hashlib
import hmac
from point import Point
from field import FieldElement

A = 0
B = 7
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
P = 2 ** 256 - 2 ** 32 - 977

# ********************

class S256Field(FieldElement):
    def __init__(self, num, prime=None):
        super().__init__(num, P)

    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)

# ********************

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

    def sec(self, compressed=True):
        '''Возвращает двоичный вариант данных формата SEC'''
        if compressed:
            if self.y.num % 2 == 0:
                return b'\x02' + self.x.num.to_bytes(32, 'big')
            else:
                return b'\x03' + self.x.num.to_bytes(32, 'big')
        else:
            return b'\x04' + self.x.num.to_bytes(32, 'big') + self.y.num.to_bytes(32, 'big')

# ********************

G = S256Point(
  0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
  0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
)
# ********************
# Класс Signature для хранения величин r и s
class Signature:
    def __init__(self, r, s):
        self.r = r
        self.s = s

    def __repr__(self):
        return 'Signature({:x}, {:x})'.format(self.r, self.s)

# ********************

class PrivateKey:

    def __init__(self, secret):
        # secret key - e
        self.secret = secret
        # poin = public key = e * G
        self.poin = secret * G

    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)

    def sign(self, z):
        k = self.deterministic_k(z)
        # r - целевая х, R - целевая точка = k*G
        r = (k * G).x.num
        k_inv = pow(k, N-2, N)
        # s = (z + r*e)/k
        s = (z + r * self.secret) * k_inv % N
        # При малой величине s получаются узлы для передачи транзакций.
        # Это делаетя для большей гибкости.
        if s > N/2:
            s = N - s
        return Signature(r, s)

    def deterministic_k(self, z):
        k = b'\x00' * 32
        v = b'\x01' * 32
        if z > N:
            z -= N
        z_bytes = z.to_bytes(32, 'big')
        secret_bytes = self.secret.to_bytes(32, 'big')
        s256 = hashlib.sha256
        k = hmac.new(k, v + b'\x00' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b'\x01' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, 'big')
            if candidate >= 1 and candidate < N:
                return candidate
            k = hmac.new(k, v + b'\x00', s256).digest()
            v = hmac.new(k, v, s256).digest()