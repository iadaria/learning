import unittest
from ecc import G, N, Signature

class ECCTest04(unittest.TestCase):

    # Представьте в формате DER подпись со следующими величинами r и s:
    def exercise_3(self):
        r = 1
        s = 1
        signature = Signature(1, 1)
        print(signature)

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
        