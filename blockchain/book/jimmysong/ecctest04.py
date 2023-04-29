import unittest
from ecc import G, N

class ECCTest04(unittest.TestCase):
    def exercise_1(self):
        e = 5000
        point = e * G
        print(point.sec().hex())
        print(point, '\n')

        e = 2018 ** 5
        point = e * G
        print(point.sec().hex())
        print(point, '\n')

        e = 0xdeadbeef12345
        point = e * G
        print(point.sec().hex())
        print(point, '\n')
        