import unittest
from ecctest import ECCTest

def suite():
    suite = unittest.TestSuite()
    #suite.addTest(ECCTest('test_on_curve'))
    #suite.addTest(ECCTest('test_add'))
    #suite.addTest(ECCTest('test_sum'))
    #suite.addTest(ECCTest('find_n'))
    suite.addTest(ECCTest('test_rmul'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())