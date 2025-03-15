from chempy import balance_stoichiometry
import pubchempy as pcp

def get_chemical_name(reaction: str) -> str:
        reactants_str, products_str = reaction.split("->")
        
        # Parse reactants and products into sets
        reactants = {r.strip() for r in reactants_str.split(" + ")}
        products = {p.strip() for p in products_str.split(" + ")}

        r = []

        for compound in reactants:
            # Search PubChem for the compound
            if compound[0].isdigit():
                compound = compound[1:]
            compound_info = pcp.get_compounds(compound, 'name')
            print(compound_info)
            print(pcp.Compound.from_cid(280).record)
            if compound_info:
                # Return the IUPAC name or the common name
                r.append(compound_info[0].iupac_name)
            else:
                # If no name is found, return the compound itself
                r.append(compound)
        
        print(r, reactants)

def balance_equation(equation: str):
    try:
        # Split the equation into reactants and products
        reactants_str, products_str = equation.split("->")
        
        # Parse reactants and products into sets
        reactants = {r.strip() for r in reactants_str.split(" + ")}
        products = {p.strip() for p in products_str.split(" + ")}
        
        # Balance the equation - ChemPy expects sets of strings, not dictionaries
        reac_coeff, prod_coeff = balance_stoichiometry(reactants, products)
        
        # Format the balanced equation with chemical formulas
        balanced_reactants = " + ".join(
            f"{int(reac_coeff[r]) if reac_coeff[r] != 1 else ''}{r}"
            for r in reac_coeff
        )
        
        balanced_products = " + ".join(
            f"{int(prod_coeff[p]) if prod_coeff[p] != 1 else ''}{p}"
            for p in prod_coeff
        )
        
        # Return the balanced equation with formulas and names on separate lines
        return f"{balanced_reactants} -> {balanced_products}" # f"{reactant_names} -> {product_names}"
    
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
equation1 = "CO2 + H2O -> C6H12O6 + O2"
equation2 = "Fe+2 + MnO4- + H+ -> Fe+3 + Mn+2 + H2O"

print(get_chemical_name(balance_equation(equation1)))  # Should correctly balance photosynthesis and add names
print(balance_equation(equation2))  # Should balance the redox reaction and add names
