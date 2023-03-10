from ecc import FieldElement
from point import Point

a = FieldElement(3, 31)
b = FieldElement(24, 31)

p1 = Point(-1, -1, 5, 7)
p2 = Point(2,5, 5, 7)
p3 = Point(-1, -1, 5, 7)

print(p1 + p2)
print(p1 + p3)

