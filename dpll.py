

def parse(dimacs_file):
    """
    given:
        path to dimacs cnf file
    return:
        formula: represented as list of list of ints
    """
    formula = []
    clause = []
    for line in open(dimacs_file):
        if not line:
            continue
        if line[0] in "cp":
            continue
        if not clause:
            clause.extend([int(x) for x in line.split()])
            if clause[-1] == 0:
                clause.pop()
                formula.append(clause)
                clause = []
    return formula


def get_units(formula):
    """
    given: 
        formula: list of clauses
    returns:
        set of unit literals
    """
    units = []
    for clause in formula:
        if len(clause) == 1:
            units.append(clause[0])
    return set(units)


def unit_propagation(formula, lit):
    """
    given: 
        formula and unit literal
    return: 
        modified formula based on unit propogation or formula with empty clause if conflict
    """
    modified_formula = []
    for clause in formula:
        if lit in clause:
            continue
        elif -lit in clause:
            modified_clause = [x for x in clause if x != -lit]
            modified_formula.append(modified_clause)
        else:
            modified_formula.append(clause)
    return modified_formula


def get_pures(formula):
    """
    given:
        formula
    return:
        set of pure literals
    """
    literals = set()
    for clause in formula:
        literals |= set(clause)
    pures = []
    for lit in literals:
        if -lit not in literals:
            pures.append(lit)
    return set(pures)


def pure_literal_elimination(formula, lit):
    """
    given: 
        formula and pure literal
    return:
        modified formula based on pure literal elimination
    """
    modified_formula = []
    for clause in formula:
        if lit in clause:
            continue
        else:
            modified_formula.append(clause)
    return modified_formula


def choose_literal(formula):
    """
    given:
        formula
    return:
        any literal from the formula or none if theres none
    """
    for clause in formula:
        for lit in clause:
            return lit
    return None


def dpll(formula, assignments):
    """
    given:
        formula
    return:
        true and satisfiable assignment or false if unsatisfiable
    """
    if formula == []:
        return True, assignments
    elif [] in formula:
        return False
    # unit propagation
    units = get_units(formula)
    assignments |= units
    for lit in units:
        formula = unit_propagation(formula, lit)
    if formula == [[]]: 
        return False
    # pure literal elimination
    pures = get_pures(formula)
    assignments |= pures
    for lit in pures:
        formula = pure_literal_elimination(formula, lit)
    # choose a literal
    lit = choose_literal(formula)
    if lit:
        return dpll(formula+[[lit]], assignments | set([lit])) or dpll(formula+[[-lit]], assignments | set([-lit]))
    return dpll(formula, assignments)

if __name__ == "__main__":
    tests = [
        ("sat_aim-50-1_6-yes1-4.cnf", True),
        ("sat_quinn.cnf", True),
        ("sat_jgalenson.cnf", True),
        ("sat_simple_v3_c2.cnf", True),
        ("sat_zebra_v155_c1135.cnf", True),
        ("unsat_aim-100-1_6-no-1.cnf", False),
        # ("unsat_bf0432-007.cnf", False),
        ("unsat_dubois20.cnf", False),
        ("unsat_dubois21.cnf", False),
        ("unsat_dubois22.cnf", False),
        ("unsat_hole6.cnf", False)
    ]
    for (dimacs_file, sat) in tests:
        formula = parse("tests/" + dimacs_file)
        sat = dpll(formula, set())
        if sat:
            sat, assignment = sat
            print(f"{dimacs_file}: {sat}\n\t{list(assignment)}\n")
        else:
            print(f"{dimacs_file}: {sat}\n")
