import sys
import collections


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
    var_map = {var:i for i, var in enumerate(variables)}
    return formula, assignment, var_map

def is_unit(ref_a, ref_b):
    return ref_a == ref_b

def unit_literals(formula):
    units = set()
    for (clause, ref_a, ref_b) in formula:
        if is_unit(ref_a, ref_b):
            units.add(ref_a)
    return units

def is_consistent(container):
    for lit in container:
        if -lit in container:
            return False
    return True

def choose_literal(formula):
    for (clause, ref_a, ref_b) in formula:
       return ref_a
    return None

def update_ref(clause, assignment, var_map, ref, units):
    if ref in units or -ref in units:
        for lit in clause:
            var = abs(lit)
            i = var_map[var]
            if assignment[i] == 0:
                ref = lit
        if ref in [lit, -lit]:
            ref = None
    return ref

def is_sat(formula):
    return formula == []

def is_unsat(formula):
    for (clause, ref_a, ref_b) in formula:
        if clause == []:
            return True
    return False

def unit_propagation(formula, assignment, var_map, units):
    modified_formula = []
    for (clause, ref_a, ref_b) in formula:
        ref_a = update_ref(clause, assignment, var_map, ref_a, units)
        ref_b = update_ref(clause[::-1], assignment, var_map, ref_b, units)
        if ref_a and ref_b:
            modified_clause = [clause, ref_a, ref_b]
            modified_formula.append(modified_clause)
        else:
            modified_formula.append([[], ref_a, ref_b])
    return modified_formula

def assign(assignment, units):
    for lit in units:
        var = abs(lit)
        i = var_map[var]
        assignment[i] = lit//var
    return assignment

def dpll(formula, assignment, var_map):
    if is_sat(formula):
        return SAT, assignment
    elif is_unsat(formula):
        return UNSAT
    else: # unresolved
        # unit prop
        units = unit_literals(formula)
        if not is_consistent(units):
            return UNSAT
        while units:
            modified_assignment = assign(assignment, units)
            formula = unit_propagation(formula, modified_assignment, var_map, units) 
            units = unit_literals(formula)
            if is_unsat(formula):
                return UNSAT
        # pure literal elim
        # branch
        lit = choose_literal(formula)
        if lit:
            return dpll(formula+[[0, [lit], lit, lit]], assignment, var_map) \
                or dpll(formula+[[0, [-lit], -lit, -lit]], assignment, var_map)
        return dpll(formula, assignment, var_map)

if __name__ == "__main__":
    tests = [
        # ("sat_quinn.cnf", SAT),
        ("sat_simple_v3_c2.cnf", SAT),
        ("sat_simple_v3_c3.cnf", SAT),
        # ("unsat_maf.cnf", UNSAT)
    ]
    for (dimacs_file, sat) in tests:
        raw_formula = parse("tests/" + dimacs_file)
        formula, assignment, var_map = setup(raw_formula)
        res = dpll(formula, assignment, var_map)
        if res:
            sat, assignment = res
            for var in var_map:
                i = var_map[var]
                assignment[i] *= var
            print(assignment)
        print(res)