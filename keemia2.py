from chempy import balance_stoichiometry
from chempy.util.parsing import formula_to_composition

def balance_equation(equation: str):
    try:
        # Split the equation into reactants and products
        reactants_str, products_str = equation.split("->")
        
        # Parse reactants and products into lists
        reactants = [r.strip() for r in reactants_str.split("+")]
        products = [p.strip() for p in products_str.split("+")]
        
        # Convert to dictionaries that chempy can work with
        reactant_formulas = {r: formula_to_composition(r) for r in reactants}
        product_formulas = {p: formula_to_composition(p) for p in products}
        
        # Balance the equation
        reac_coeff, prod_coeff = balance_stoichiometry(reactant_formulas, product_formulas)
        
        # Format the balanced equation
        balanced_reactants = " + ".join(
            f"{int(reac_coeff[r]) if reac_coeff[r] != 1 else ''}{r}"
            for r in reactants
        )
        
        balanced_products = " + ".join(
            f"{int(prod_coeff[p]) if prod_coeff[p] != 1 else ''}{p}"
            for p in products
        )
        
        return f"{balanced_reactants} -> {balanced_products}"
    
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
equation1 = "CO2 + H2O -> C6H12O6 + O2"
equation2 = "Fe2+ + MnO4- + H+ -> Fe3+ + Mn2+ + H2O"

print(balance_equation(equation1))  # Should correctly balance photosynthesis
print(balance_equation(equation2))  # Should correctly balance the redox reaction