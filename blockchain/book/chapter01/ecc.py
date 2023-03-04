class FieldElement:
    def __init__(self, num, prime):
        if num >= prime or num < 0:
            error = 'Num{} not in field range 0 to {}'.format(num, prime - 1)
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return 'FieldElement_{}({})'.format(self.prime, self.num)

    def __eq__(self, operand):
        if operand is None:
            return False
        return self.num == operand.num and self.prime == operand.prime

    def __ne__(self, operand):
        return not (self == operand)

    def __add__(self, operand):
        # Проверяем принадлежность к одному и тому же конечному полю
        if self.prime != operand.prime:
            raise TypeError('Cannot add two numbers in different Fields')
        num = (self.num + operand.num) % self.prime
        # Возвращаем экземпляр данного класса
        return self.__class__(num, self.prime)

    def __sub__(self, operand):
        # Проверяем принадлежность к одному и тому же конечному полю
        if self.prime != operand.prime:
            raise TypeError('Cannot sub two numbers in different Fields')
        num = (self.num - operand.num) % self.prime
        # Возвращаем экземпляр данного класса
        return self.__class__(num, self.prime)

    def __mul__(self, operand):
        # Проверяем принадлежность к одному и тому же конечному полю
        if self.prime != operand.prime:
            raise TypeError('Cannot mul two numbers in different Fields')
        num = (self.num * operand.num) % self.prime
        return self.__class__(num, self.prime)

    def __pow__(self, exponent):
        # num = (self.num ** exponent) % self.prime
        """  n = exponent
        while n < 0:
            n += self.prime - 1 """
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__ (self, other):
        if self.prime != other.prime:
            raise TypeError('Cannot divide two numbers in defferent Fields')
        num = self.num * pow(other.num, self.prime - 2, self.prime) % self.prime
        return self.__class__(num, self.prime)