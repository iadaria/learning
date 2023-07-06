import unittest
from test import ecctest05
from tx import TxTest

from ecc import PrivateKey

def suite():
    suite = unittest.TestSuite()
    suite.addTest(ecctest05.ECCTest05('exercise_5'))
    //suite.addTest(TxTest('test_fee'))
    return suite

def manaul():
    privateKey = PrivateKey(12345)
    print(privateKey.deterministic_k(12345))


def from256bit_to32byte():
    for digit in range(1, 50):
        print(digit)
        digit_byte_big = digit.to_bytes(32, 'big')
        print('simple byte {} = big byte = {}'.format(digit.to_bytes(), digit_byte_big))

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
