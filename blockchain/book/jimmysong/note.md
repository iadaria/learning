> python3 main.py

### График онлайн
https://www.mathway.com/ru/graph

1 Посмотреть результат raw[-4:] что нам дает
For example a list:
```python
people = ["Tom", "Bob", "Alice", "Sam", "Tim", "Bill"]

slice_people1 = people[:3] # from 0 to 3 Tom, Bob, Alice

slice_people2 = people[:-1] # с предпоследнего по нулевой

slice_people2 = people[-3;-1] # с третьего с конца по предпоследний Sam, Tim
```

# stack[-1]
```python
stack = ["A", "B", "C", "D", "E"]
print(stack[-1]) # E

stack.append(stack[-1])
print(stack) # ['A', 'B', 'C', 'D', 'E', 'E']

element = stack.pop()
print(element) # E
print(stack) # ['A', 'B', 'C', 'D', 'E']

print(stack.pop(0)) # "A"
```

# stream
```python
from io import BytesIO
stream = BytesIO(bytes.fromhex('6b4830'))
current = stream.read(1)
print(current) # b'k'
print(current[0]) # 107 => 107(10) = 6b(16)
```

# arrays
```python
c = [1, 2]
d = [3, 4]
e = c + d
print(e) # [1, 2, 3, 4]
```