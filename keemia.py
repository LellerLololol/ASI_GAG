# Format input: CO2 + H2O -> C6H12O6 + O2
# Format output: 6CO2 + H2O -> C6H12O6 + 6O2
from collections import defaultdict as dd

left_side, right_side = input().strip().split("->")
left_side = left_side.split("+")
right_side = right_side.split("+")

def element_counter(reaction):
    counter = dd(list)

    buf = ""
    buf_n = ""
    for element in reaction:
        element: str = element.strip()
        for char in element:
            if char.isupper():
                if buf:
                    if buf_n:
                        counter[buf].append(int(buf_n))
                    else:
                        counter[buf].append(1)
                buf = char
                buf_n = ""
            elif char.islower():
                buf += char
            elif char.isdigit():
                buf_n += char
        if buf:
            if buf_n:
                counter[buf].append(int(buf_n))
            else:
                counter[buf].append(1)
    return counter

counter_left = element_counter(left_side)
counter_right = element_counter(right_side)


print(counter_left)
print(counter_right)