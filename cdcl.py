import sys
import collections


SAT = True
UNSAT = False
BOTTOM = None


def parse(dimacs_file):
    """
    given:
        path to dimacs cnf file
    return:
        formula: represented as list of list of ints
    """
    formula = []
    clause = []
    clause_id = 1
    for line in open(dimacs_file):
        if not line:
            continue
        if line[0] in "cp":
            continue
        if int_line := (int(x) for x in line.split()):
            for lit in int_line:
                if lit == 0:
                    if clause:
                        formula.append([clause_id, clause])
                    clause = []
                    clause_id += 1
                elif lit != 0:
                    clause.append(lit)
    if clause:
        formula.append([clause_id, clause])
    return formula


def get_unit(formula):
    for (clause_id, clause) in formula:
        if len(clause) == 1:
            return (clause_id, clause)
    return None


def unit_propagation(formula, lit):
    modified_formula = []
    for (clause_id, clause) in formula:
        if lit in clause:
            continue
        elif -lit in clause:
            modified_clause = [x for x in clause if x != -lit]
            modified_formula.append([clause_id, modified_clause])
        else:
            modified_formula.append([clause_id, clause])
    return modified_formula


def bcp(formula, assignment):
    """
    repeatedly apply unit propogation till either conflict or fix state
    """
    #trail[ (decide, 1)-> (unit, c1, 5)-> .... -> (decide, 2)]
          
    while unit := get_unit(formula):
        clause_id, [lit] = unit
        formula = unit_propagation(formula, lit)
        assignment.add(lit)
        # check for conflict and put the conflict clause into trails if exists
        for (clause_id, clause) in formula:
            if clause == []:
                return UNSAT
    return formula


def analyze_conflict(formula, assignment):
    """
    compute backtracking level
    detect global unsatisfiability
    adding new constraints on search
    """
    pass


def resolution(clause1, clause2):
    """
    binary resolution
    """
    pass


def choose_literal(formula):
    for (clause_id, clause) in formula:
        for lit in clause:
            return lit
    return None


def cdcl(formula):
    assignment = set()
    history = collections.defaultdict()
    while True:
        if bcp(formula, assignment) == UNSAT:
            backtrack_level = analyze_conflict()
            if backtrack_level < 0:
                return UNSAT
            backtrack(backtrack_level)
        elif bcp(formula, assignment) != UNSAT:
            lit = choose_literal(formula)
            if not lit:
                return SAT
            formula = formula + [[0, [lit]]]
