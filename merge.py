from chempy import balance_stoichiometry, Substance
import pubchempy as pcp
import re

# Parsing functions
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

# Chemical name retrieval
def get_chemical_name(reaction: str) -> str:
    try:
        reactants_str, products_str = reaction.split("->")
        
        def process_side(side_str):
            compounds = []
            for comp in side_str.split(" + "):
                comp = comp.strip()
                coefficient = ''
                formula = comp
                if comp and comp[0].isdigit():
                    i = 0
                    while i < len(comp) and comp[i].isdigit():
                        coefficient += comp[i]
                        i += 1
                    formula = comp[i:].strip()
                formula_clean = formula.split('+')[0].split('-')[0].strip()
                results = pcp.get_compounds(formula_clean, 'formula')
                if not results:
                    name = formula
                else:
                    cid = results[0].cid
                    full_compound = pcp.Compound.from_cid(cid)
                    name = full_compound.iupac_name if full_compound.iupac_name else formula
                compounds.append(f"{coefficient}*{name}" if coefficient else name)
            return " + ".join(compounds)
        
        balanced_reactants = process_side(reactants_str.strip())
        balanced_products = process_side(products_str.strip())
        return f"{balanced_reactants} -> {balanced_products}"
    except Exception as e:
        return f"Error: {str(e)}"

# Balancing equation with enhanced features
def balance_equation(equation: str) -> str:
    try:
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
    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    equation1 = "CO2 + H2O -> C6H12O6 + O2"
    balanced_eq1 = balance_equation(equation1)
    print(f"Balanced: {balanced_eq1}")
    print(f"Named: {get_chemical_name(balanced_eq1)}")

    equation2 = "SO2{2-} + O2 -> SO3{2-}"
    balanced_eq2 = balance_equation(equation2)
    print(f"\nBalanced: {balanced_eq2}")
    print(f"Named: {get_chemical_name(balanced_eq2)}")
