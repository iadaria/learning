import unittest
# from ecctest import ECCTest
from ecctest03 import ECCTest03
from ecc import PrivateKey

def suite():
    suite = unittest.TestSuite()
    #suite.addTest(ECCTest('test_on_curve'))
    #suite.addTest(ECCTest('test_add'))
    #suite.addTest(ECCTest('test_sum'))
    #suite.addTest(ECCTest('find_n'))
    #suite.addTest(ECCTest('secp256k1_check_n'))
    suite.addTest(ECCTest03('test_signature_1'))
    suite.addTest(ECCTest03('test_signature_2'))
    suite.addTest(ECCTest03('test_create_signature'))
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
    #runner = unittest.TextTestRunner()
    #runner.run(suite())
    from256bit_to32byte()