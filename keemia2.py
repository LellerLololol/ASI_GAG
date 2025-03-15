# AI PROMT: make a chemistry solver using chempy
# AI kasutatud osa balance_equation funktsiooni jaoks, aga mitte teiste funktsioonide jaoks
# Format input: CO2 + H2O -> C6H12O6 + O2
# Format output: 6CO2 + H2O -> C6H12O6 + 6O2
from chempy import balance_stoichiometry, Substance
import re


def parse_for_chempy(element: str) -> str:

    element = element.strip()
    pattern = r"\{([^}]+)\}"

    try:
        result = re.findall(pattern, element)[0][::-1]
    except IndexError:
        result = ""
    element = re.sub(pattern, result, element)
    # print(element)
    return element
def parse_from_chempy(element: str) -> str:

    element = element.strip()
    pattern = r"\d+([-+]\d+)"

    try:
        result = re.findall(pattern, element)[0][::-1]
    except IndexError:
        result = ""
    element = re.sub(pattern, "{" + result + "}", element)
    # print(element)
    return element



def balance_equation(equation: str):
    # try:
    reactants, products = equation.split("->")
    reactants = [
        Substance.from_formula(parse_for_chempy(r)) for r in reactants.split("+")
    ]
    products = [
        Substance.from_formula(parse_for_chempy(p)) for p in products.split("+")
    ]

    reactant_formulas = {r.name for r in reactants}
    product_formulas = {p.name for p in products}

    balanced = balance_stoichiometry(reactant_formulas, product_formulas)

    balanced_reactants = " + ".join(
        f"{balanced[0][r.name] if balanced[0][r.name] != 1 else ''}{parse_from_chempy(r.name)}"
        for r in reactants
    )
    balanced_products = " + ".join(
        f"{balanced[1][p.name] if balanced[1][p.name] != 1 else ''}{parse_from_chempy(p.name)}"
        for p in products
    )
    
    return f"{balanced_reactants} -> {balanced_products}"


# except Exception as e:
#     return f"Error: {str(e)}"

if __name__ == "__main__":
    # Example usage
    equation = "CO2 + H2O -> C6H12O6 + O2"
    print(balance_equation(equation))
    equation = "SO2{2-} + O2 -> SO3{2-}"
    print(balance_equation(equation))
