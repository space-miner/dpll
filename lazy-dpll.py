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

def setup(raw_formula):
    variables = set()
    formula = []
    for clause in raw_formula:
        ref_a = clause[0]
        ref_b = clause[-1]
        variables |= set(abs(lit) for lit in clause)
        formula.append([clause, ref_a, ref_b])
    nb_vars = len(variables)
    assignment = [0] * nb_vars
    variable_map = {var:i for i, var in enumerate(variables)}
    return formula, assignment, variable_map


def unit_literals(formula):
    units = set()
    for (clause, ref_a, ref_b) in formula:
        if ref_a == ref_b:
            units.add(ref_a)
    return units

def is_consistent(literals):
    for lit in literals:
        if -lit in literals:
            return False
    return True

def is_unassigned(lit, assignment, variable_map):
    var = abs(lit)
    i = variable_map[var]
    return assignment[i] == 0

def choose_literal(formula, assignment, variable_map):
    for (clause, ref_a, ref_b) in formula:
        if is_unassigned(ref_a, assignment, variable_map):
            return ref_a
        if is_unassigned(ref_b, assignment, variable_map):
            return ref_b
    return None

def update_ref(clause, assignment, variable_map, units, ref):
    if ref in units or -ref in units:
        for lit in clause:
            if is_unassigned(lit, assignment, variable_map):
                return lit
        return None
    return ref

def is_sat(formula):
    return formula == []

def is_unsat(formula):
    for (clause, ref_a, ref_b) in formula:
        if clause == []:
            return True
    return False

import time 
def unit_propagation(formula, assignment, variable_map, units):
    if is_consistent(units):
        modified_assignment = assign_units(assignment, units)
        modified_formula = []
        for (clause, ref_a, ref_b) in formula:
            if ref_a in units or ref_b in units:
                continue
            else:
                ref_a = update_ref(clause, modified_assignment, variable_map, units, ref_a)
                ref_b = update_ref(clause[::-1], modified_assignment, variable_map, units, ref_b)
                if ref_a and ref_b:
                    modified_clause = [clause, ref_a, ref_b]
                    modified_formula.append(modified_clause)
                else:
                    modified_formula.append([[], ref_a, ref_b])
        return modified_formula, modified_assignment
    return formula, assignment

def assign_units(assignment, units):
    modified_assignment = assignment[:]
    for lit in units:
        var = abs(lit)
        i = variable_map[var]
        modified_assignment[i] = 1 if lit > 0 else -1
    return modified_assignment 

def dpll(formula, assignment, variable_map):
    if is_sat(formula):
        return SAT, assignment
    elif is_unsat(formula):
        return UNSAT
    # unit prop
    units = unit_literals(formula)
    while units:
        if not is_consistent(units):
            return UNSAT
        formula, assignment = unit_propagation(formula, assignment, variable_map, units) 
        if is_unsat(formula):
            return UNSAT
        units = unit_literals(formula)
    # pure literal elim
    lit = choose_literal(formula, assignment, variable_map)
    if lit:
        return dpll(formula+[[[lit], lit, lit]], assignment, variable_map) \
            or dpll(formula+[[[-lit], -lit, -lit]], assignment, variable_map)
    return dpll(formula, assignment, variable_map)

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
        raw_formula = parse("tests/" + dimacs_file)
        formula, assignment, variable_map = setup(raw_formula)
        res = dpll(formula, assignment, variable_map)
        print(dimacs_file)
        if res:
            sat, assignment = res
            for var in variable_map:
                i = variable_map[var]
                assignment[i] *= var
            print(assignment)
        else:
            print(res)