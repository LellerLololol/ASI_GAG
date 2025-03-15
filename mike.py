from chempy import balance_stoichiometry
import pubchempy as pcp
import re

def parse_for_chempy(element: str) -> str:
    element = element.strip()
    pattern = r"\{([^}]+)\}"
    try:
        result = re.findall(pattern, element)[0][::-1]
    except IndexError:
        result = ""
    element = re.sub(pattern, result, element)
    return element

def parse_from_chempy(element: str) -> str:
    element = element.strip()
    pattern = r"\d+([-+]\d+)"
    try:
        result = re.findall(pattern, element)[0][::-1]
    except IndexError:
        result = ""
    element = re.sub(pattern, "{" + result + "}", element)
    return element


def get_chemical_name(reaction: str) -> str:
    try:
        reactants_str, products_str = reaction.split("->")
        
        def process_side(side_str):
            compounds = []
            for comp in side_str.split(" + "):
                comp = comp.strip()
                coefficient = ''
                formula = comp
                # Extract coefficient
                if comp and comp[0].isdigit():
                    i = 0
                    while i < len(comp) and comp[i].isdigit():
                        coefficient += comp[i]
                        i += 1
                    formula = comp[i:].strip()
                # Handle ions and special characters
                formula_clean = formula.split('+')[0].split('-')[0].strip()
                # Search PubChem by formula
                results = pcp.get_compounds(formula_clean, 'formula')
                if not results:
                    name = formula
                else:
                    # Get the first compound's IUPAC name
                    cid = results[0].cid
                    full_compound = pcp.Compound.from_cid(cid)
                    name = full_compound.iupac_name if full_compound.iupac_name else formula
                # Reattach coefficient with *
                compounds.append(f"{coefficient}*{name}" if coefficient else name)
            return " + ".join(compounds)
        
        balanced_reactants = process_side(reactants_str.strip())
        balanced_products = process_side(products_str.strip())
        
        return f"{balanced_reactants} -> {balanced_products}"
    except Exception as e:
        return f"Error: {str(e)}"

def balance_equation(equation: str) -> str:
    try:
        reactants_str, products_str = equation.split("->")
        reactants = [parse_for_chempy(r) for r in reactants_str.split(" + ")]
        products = [parse_for_chempy(p) for p in products_str.split(" + ")]
        reac, prod = balance_stoichiometry(reactants, products)
        
        def format_side(coeff_dict):
            return " + ".join([f"{int(v)}{parse_from_chempy(k)}" if v != 1 else k for k, v in coeff_dict.items()])
        def format_side_pcp(coeff_dict):
            return " + ".join([f"{int(v)}{k}" if v != 1 else k for k, v in coeff_dict.items()])
        
        return f"Balanced: {format_side(reac)} -> {format_side(prod)}\nNamed: {get_chemical_name(f'{format_side_pcp(reac)} -> {format_side_pcp(prod)}')}"
    except Exception as e:
        return f"Error: {str(e)}"

# Example Usage
equation1 = "CO2 + H2O -> C6H12O6 + O2"
balanced_eq1 = balance_equation(equation1)
print(f"Balanced: {balanced_eq1}")
# print(f"Named: {get_chemical_name(balanced_eq1)}")



equation2 = "Fe+2 + MnO4- + H+ -> Fe+3 + Mn+2 + H2O"
balanced_eq2 = balance_equation(equation2)
print(f"\nBalanced: {balanced_eq2}")
# print(f"Named: {get_chemical_name(balanced_eq2)}")

equation2 = "Fe+2 + MnO4- + H+ -> Fe+3 + Mn+2 + H2O"
balanced_eq2 = balance_equation(equation2)
print(f"\nBalanced: {balanced_eq2}")
# print(f"Named: {get_chemical_name(balanced_eq2)}")