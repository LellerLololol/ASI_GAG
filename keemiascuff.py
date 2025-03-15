from chempy import balance_stoichiometry, balance_charge
#from chempy.electrochemistry.nernst import balance_charge

def balance_equation(equation: str):
    try:
        reactants, products = equation.split("->")
        reactants = [r.strip() for r in reactants.split("+")]
        products = [p.strip() for p in products.split("+")]

        # Use balance_stoichiometry() for normal (non-ionic) reactions
        try:
            balanced = balance_stoichiometry(set(reactants), set(products))
        except Exception:
            # If it fails, try balance_charge() for ionic equations
            balanced = balance_charge(reactants, products)

        # Format output correctly
        balanced_reactants = " + ".join(
            f"{balanced[0].get(r, 1) if balanced[0].get(r, 1) != 1 else ''}{r}"
            for r in reactants
        )
        balanced_products = " + ".join(
            f"{balanced[1].get(p, 1) if balanced[1].get(p, 1) != 1 else ''}{p}"
            for p in products
        )

        return f"{balanced_reactants} -> {balanced_products}"
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
equation1 = "CO2 + H2O -> C6H12O6 + O2"  # Normal stoichiometric reaction
equation2 = "Fe2+ + MnO4- + H+ -> Fe3+ + Mn2+ + H2O"  # Ionic reaction

print(balance_equation(equation1))  # Uses balance_stoichiometry()
print(balance_equation(equation2))  # Uses balance_charge()
