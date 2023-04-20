import unittest
# from ecctest import ECCTest
from ecctest03 import ECCTest03
from ecc import G, N

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
    print(N * G)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())