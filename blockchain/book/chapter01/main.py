from ecc import FieldElement


a = FieldElement(3, 13)
b = FieldElement(1, 13)

print(a**3 == b)
