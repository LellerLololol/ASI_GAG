# Format input: CO2 + H2O -> C6H12O6 + O2
# Format output: 6CO2 + H2O -> C6H12O6 + 6O2
from collections import defaultdict as dd

left_side, right_side = input().strip().split("->")
left_side = left_side.split("+")
right_side = right_side.split("+")

counter_left = dd(int)
counter_right = dd(int)

buf = ""
buf_n = ""
for element in left_side:
    element: str = element.strip()
    for char in element:
        if char.isupper():
            if buf:
                if buf_n:
                    counter_left[buf] += int(buf_n)
                else:
                    counter_left[buf] += 1
            buf = char
            buf_n = ""
        elif char.islower():
            buf += char
        elif char.isdigit():
            buf_n += char
    if buf:
        if buf_n:
            counter_left[buf] += int(buf_n)
        else:
            counter_left[buf] += 1


print(counter_left)

buf = ""
buf_n = ""
for element in right_side:
    element: str = element.strip()
    for char in element:
        if char.isupper():
            if buf:
                if buf_n:
                    counter_left[buf] += int(buf_n)
                else:
                    counter_left[buf] += 1
            buf = char
            buf_n = ""
        elif char.islower():
            buf += char
        elif char.isdigit():
            buf_n += char
    if buf:
        if buf_n:
            counter_left[buf] += int(buf_n)
        else:
            counter_left[buf] += 1

print(counter_right)