import unittest
from ecc import FieldElement
from point import Point

class ECCTest(unittest.TestCase):

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
            #with self.assertRaises(ValueError):
                #Point(x, y, a, b)

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
        