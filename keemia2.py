from chempy import balance_stoichiometry
from chempy.chemistry import Substance

def balance_equation(equation: str):
    try:
        reactants, products = equation.split("->")
        reactants = [r.strip() for r in reactants.split("+")]
        products = [p.strip() for p in products.split("+")]

        # Parse as substances to include charge information
        reactant_set = {Substance.from_formula(r) for r in reactants}
        product_set = {Substance.from_formula(p) for p in products}

        balanced = balance_stoichiometry(reactant_set, product_set)

        # Format output
        balanced_reactants = " + ".join(
            f"{balanced[0][Substance.from_formula(r)] if balanced[0][Substance.from_formula(r)] != 1 else ''}{r}"
            for r in reactants
        )
        balanced_products = " + ".join(
            f"{balanced[1][Substance.from_formula(p)] if balanced[1][Substance.from_formula(p)] != 1 else ''}{p}"
            for p in products
        )

        return f"{balanced_reactants} -> {balanced_products}"
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
equation1 = "CO2 + H2O -> C6H12O6 + O2"
equation2 = "Fe2+ + MnO4- + H+ -> Fe3+ + Mn2+ + H2O"

print(balance_equation(equation1))
print(balance_equation(equation2))
