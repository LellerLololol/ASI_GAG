# Format input: CO2 + H2O -> C6H12O6 + O2 
# Format output: 6CO2 + H2O -> C6H12O6 + 6O2
left_side = right_side = input().strip().split("->")
left_side = left_side.split("+")
right_side = right_side.split("+")

for element in left_side:
    element = element.strip()
    if element[0].isdigit():
        print(element)
    else:
        print("1" + element)