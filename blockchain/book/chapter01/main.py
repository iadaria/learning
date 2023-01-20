
from ecc import FieldElement

a = FieldElement(7, 13)
b = FieldElement(6, 13)

print('a == b', a == b)
print('a == a', a == a)

print('a != b', a != b)
print('a != a', a != a)

print('a + b', a + b)
print('a - b', a - b)

x = 12^7*77^49
y = x / 97
d = x - y * 91
print('x={}, y={}, d={}', x, y, d)