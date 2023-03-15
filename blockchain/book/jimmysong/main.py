from ecc import FieldElement
from point import Point

a = FieldElement(0, 223)
b = FieldElement(7, 223)
x = FieldElement(192, 223)
y = FieldElement(105, 223)

x2 = FieldElement(17, 223)
y2 = FieldElement(56, 223)

x3 = FieldElement(200, 223)
y3 = FieldElement(119, 223)

x4 = FieldElement(1, 223)
y4 = FieldElement(193, 223)

x5 = FieldElement(42, 223)
y5 = FieldElement(99, 223)

p1 = Point(x, y, a, b)
p2 = Point(x2, y2, a, b)
#p3 = Point(x3, y3, a, b)
p4 = Point(x4, y4, a, b)
#p5 = Point(x5, y5, a, b)
print(p1)
print(p2)
print(p4)
