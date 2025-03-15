# AI PROMT: make a chemistry solver using chempy
# Format input: CO2 + H2O -> C6H12O6 + O2
# Format output: 6CO2 + H2O -> C6H12O6 + 6O2
from chempy import balance_stoichiometry

def balance_equation(equation: str):
    try:
        reactants, products = equation.split("->")
        reactants = [r.strip() for r in reactants.split("+")]
        products = [p.strip() for p in products.split("+")]
        
        balanced = balance_stoichiometry(set(reactants), set(products))
        
        balanced_reactants = " + ".join(f"{balanced[0][r] if balanced[0][r] != 1 else ''}{r}" for r in reactants)
        balanced_products = " + ".join(f"{balanced[1][p] if balanced[1][p] != 1 else ''}{p}" for p in products)
        
        return f"{balanced_reactants} -> {balanced_products}"
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
equation = "CO2+ H2O -> C6H12O6 + O2"
equation2 = "CO2+H8(O2)2->C6H12O6+O2"
print(balance_equation(equation))