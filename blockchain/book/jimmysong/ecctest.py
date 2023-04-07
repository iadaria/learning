import unittest
from field import FieldElement
from point import Point

class ECCTest(unittest.TestCase):

    def test_rmul(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(15, prime)
        y = FieldElement(86, prime)
        p = Point(x, y, a, b)
        print(7 * p)


    # Найти порядок группы
    def find_n(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        x = FieldElement(15, prime)
        y = FieldElement(86, prime)
        p = Point(x, y, a, b)
        inf = Point(None, None, a, b)
        product = p
        count = 1
        while product != inf:
            product += p
            count += 1
        print(count)
        self.assertEqual(7, count)

    def test_on_curve(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        valid_points = ((192,105), (17,56), (1, 193))
        invalid_points = ((200, 119), (42, 99))
        for x_raw, y_raw in valid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            Point(x, y, a, b)
        for x_raw, y_raw in invalid_points:
            x = FieldElement(x_raw, prime)
            y = FieldElement(y_raw, prime)
            with self.assertRaises(ValueError):
                Point(x, y, a, b)

    def test_add(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        additions = (
            (170, 142, 60, 139),
            (47, 71, 17, 56),
            (143, 98, 76, 66),
            (170, 142, 170, 142),
        )
        for x1_raw, y1_raw, x2_raw, y2_raw in additions:
            x1 = FieldElement(x1_raw, prime)
            y1 = FieldElement(y1_raw, prime)
            p1 = Point(x1, y1, a, b)
            x2 = FieldElement(x2_raw, prime)
            y2 = FieldElement(y2_raw, prime)
            p2 = Point(x2, y2, a, b)
            p3 = p1 + p2
            print(p3)
            self.assertEqual(p3, p1 + p2)

    def test_sum(self):
        prime = 223
        a = FieldElement(0, prime)
        b = FieldElement(7, prime)
        
        x1 = FieldElement(192, prime)
        y1 = FieldElement(105, prime)
        p1 = Point(x1, y1, a, b)
        print()
        print(p1 + p1)
        print(2 * p1)
        
        x1 = FieldElement(143, prime)
        y1 = FieldElement(98, prime)
        p2 = Point(x1, y1, a, b)
        print()
        print(p2 + p2)
        print(2 * p2)

        for mult in (2, 4, 8, 21):
            print('mult = {}'.format(mult))
            x = FieldElement(47, prime)
            y = FieldElement(71, prime)
            p = Point(x, y, a, b)
            print(mult * p)
    
    def secp256k1(self):
        gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        p = 2 ** 256 - 2 ** 32 - 977
        print(gy ** 2 % p == (gx ** 3 + 7) % p)

    def secp256k1_check_n(self):
        gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        p = 2 ** 256 - 2 ** 32 - 977
        n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        x = FieldElement(gx, p)
        y = FieldElement(gy, p)
        seven = FieldElement(7, p)
        zero = FieldElement(0, p)
        G = Point(x, y, zero, seven)
        print(n * G)