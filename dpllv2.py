import sys

def parse(dimacs_file):
    """
    given:
        path to dimacs cnf file
    return:
        formula represented as map of clauses, a set of ints
    """
    formula = dict()
    clause = set()
    clause_id = 1
    for line in open(dimacs_file):
        if not line:
            continue
        if line[0] in "cp":
            continue
        if not clause:
            clause |= set(int(x) for x in line.split())
            if 0 in clause:
                clause.remove(0)
                formula[clause_id] = clause
                clause_id += 1
                clause = set()
    return formula


def get_units(formula):
    """
    given: 
        formula: map of clauses
    returns:
        set of unit literals
    """
    units = set()
    for clause in formula.values():
        if len(clause) == 1:
            units |= clause
    return units

def is_consistent(units):
    """
    given:
        units: set of unit literals
    return:
        true if consistent false if not
    """
    for lit in units:
        if -lit in units:
            return False
    return True
    

def unit_propagation(formula, units):
    """
    given: 
        formula: map of clauses
        units: set of unit literals
    return: 
        modified formula based on unit propogation or formula with empty clause if conflict
    """
    if not is_consistent(units):
        return {0: set()}
    neg_units = set(-x for x in units)
    modified_formula = dict()
    for clause_id, clause in formula.items():
        if units & clause:
            continue
        else:
            modified_clause = clause - neg_units
            modified_formula[clause_id] = modified_clause
    return modified_formula


def get_pures(formula):
    """
    given:
        formula
    return:
        set of pure literals
    """
    literals = set()
    for clause in formula.values():
        literals |= set(clause)
    pures = set()
    for lit in literals:
        if -lit not in literals:
            pures.add(lit)
    return pures


def pure_literal_elimination(formula, pures):
    """
    given: 
        formula and pure literal
    return:
        modified formula based on pure literal elimination
    """
    modified_formula = dict()
    for clause_id, clause in formula.items():
        if pures & clause:
            continue
        else:
            modified_formula[clause_id] = clause
    return modified_formula


def choose_literal(formula):
    """
    given:
        formula
    return:
        any literal from the formula or none if theres none
    """
    for clause in formula.values():
        for lit in clause:
            return lit
    return None


def is_sat(formula):
    return len(formula) == 0


def is_unsat(formula):
    for clause in formula.values():
        if len(clause) == 0:
            return True
    return False


def dpll(formula):
    """
    given:
        formula
    return:
        true if the formula is satisfiable and false if unsatisfiable
    """
    if is_sat(formula):
        return True
    elif is_unsat(formula):
        return False
    # unit propagation
    units = get_units(formula)
    formula = unit_propagation(formula, units)
    if is_unsat(formula): 
        return False
    # pure literal elimination
    pures = get_pures(formula)
    formula = pure_literal_elimination(formula, pures)
    # choose a literal
    lit = choose_literal(formula)
    if lit:
        return dpll({0:set([lit]), **formula}) or dpll({0:set([-lit]), **formula})
    return dpll(formula)

if __name__ == "__main__":
    tests = [
        ("sat_aim-50-1_6-yes1-4.cnf", True),
        ("sat_jgalenson.cnf", True),
        ("sat_quinn.cnf", True),
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
        print(dimacs_file, dpll(formula)) 
