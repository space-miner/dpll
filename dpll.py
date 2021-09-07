import sys


SAT = True
UNSAT = False


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
        if int_line := (int(x) for x in line.split()):
            for lit in int_line:
                if lit == 0:
                    if clause:
                        formula.append(clause)
                    clause = []
                elif lit != 0:
                    clause.append(lit)
    if clause:
        formula.append(clause)
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
        return SAT, sorted(assignments, key=lambda x: abs(x))
    elif [] in formula:
        return UNSAT
    # unit propagation
    units = get_units(formula)
    assignments |= units
    for lit in units:
        formula = unit_propagation(formula, lit)
    if formula == [[]]: 
        return UNSAT
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
        ("sat_aim-50-1_6-yes1-4.cnf", SAT),
        ("sat_choueiry.cnf", SAT),
        ("sat_quinn.cnf", SAT),
        ("sat_jgalenson.cnf", SAT),
        ("sat_simple_v3_c2.cnf", SAT),
        ("sat_sukrutrao.cnf", SAT),
        ("sat_zebra_v155_c1135.cnf", SAT),
        ("unsat_aim-100-1_6-no-1.cnf", UNSAT),
        # ("unsat_bf0432-007.cnf", UNSAT),
        ("unsat_dubois20.cnf", UNSAT),
        ("unsat_dubois21.cnf", UNSAT),
        ("unsat_dubois22.cnf", UNSAT),
        ("unsat_hole6.cnf", UNSAT),
        ("unsat_maf.cnf", UNSAT)
    ]
    for (dimacs_file, sat) in tests:
        formula = parse("tests/" + dimacs_file)
        result = dpll(formula, set())
        print(dimacs_file)
        if result:
            res, assignment = result
            print(f"SAT {' '.join(str(x) for x in assignment)}\n")
        else:
            print("UNSAT\n")
        assert (bool(result) == sat)
