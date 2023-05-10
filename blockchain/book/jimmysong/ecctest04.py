import unittest
from ecc import G, Signature

class ECCTest04(unittest.TestCase):

    # Представьте в формате DER подпись со следующими величинами r и s:
    def exercise_3(self):
        r = 0x37206a0610995c58074999cb9767b87af4c4978db68c06e8e6e81d282047a7c6
        s = 0x8ca63759c1157ebeaec0d03cecca119fc9a75bf8e6d0fa65c841c8e2738cdaec
        signature = Signature(r, s)
        print(signature)
        der = signature.der()
        print(der)
        print(der.hex())

    # Представляем открытый ключ в несжатом формате SEC,
    # если имеются следующие секретные ключи
    def exercise_1(self):
        e = 5000
        point = e * G
        print(point.sec(False).hex())
        print(point, '\n')

        e = 2018 ** 5
        point = e * G
        print(point.sec(False).hex())
        print(point, '\n')

        e = 0xdeadbeef12345
        point = e * G
        print(point.sec(False).hex())
        print(point, '\n')

    # Находим открытый ключ в сжатом формате SEC
    # если имеются следующие секретные ключи
    def exercise_2(self):
        e = 5001
        point = e * G
        print(point.sec().hex())
        print(point, '\n')

        e = 2019 ** 5
        point = e * G
        print(point.sec().hex())
        print(point, '\n')

        e = 0xdeadbeef54321
        point = e * G
        print(point.sec().hex())
        print(point, '\n')
        