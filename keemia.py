
# Format input: CO2 + H2O -> C6H12O6 + O2 
# Format output: 6CO2 + H2O -> C6H12O6 + 6O2
left_side = right_side = input().strip().split("->")
left_side = left_side.split("+")
right_side = right_side.split("+")

for element in left_side:
    element = element.strip()
    
from sympy import symbols, Eq, solve
import re


def parse_compound(compound):
    elements = re.findall(r'([A-Z][a-z]*)(\d*)', compound)
    return {el: int(count) if count else 1 for el, count in elements}


def balance_equation(reactants, products):
    elements = set()
    reactant_dicts = []
    product_dicts = []

    for compound in reactants:
        parsed = parse_compound(compound)
        reactant_dicts.append(parsed)
        elements.update(parsed.keys())

    for compound in products:
        parsed = parse_compound(compound)
        product_dicts.append(parsed)
        elements.update(parsed.keys())

    coefficients = symbols(f'x1:{len(reactants)+len(products)+1}')
    equations = []

    for element in elements:
        lhs = sum(coefficients[i] * reactant_dicts[i].get(element, 0) for i in range(len(reactants)))
        rhs = sum(coefficients[i+len(reactants)] * product_dicts[i].get(element, 0) for i in range(len(products)))
        equations.append(Eq(lhs, rhs))

    solution = solve(equations, coefficients)
    
    if not solution:
        return "Equation cannot be balanced."

    coefficients_values = [solution.get(c, 1) for c in coefficients]
    lcm = max(1, *(c.q for c in coefficients_values if c.q != 1))
    balanced_coeffs = [c * lcm for c in coefficients_values]

    return " + ".join(f"{balanced_coeffs[i]} {reactants[i]}" for i in range(len(reactants))) + " -> " + \
           " + ".join(f"{balanced_coeffs[i+len(reactants)]} {products[i]}" for i in range(len(products)))

