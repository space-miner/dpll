SATISFIABLE = True
UNSATISFIABLE = False


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
        if line[0] == '%':
            break
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


def is_satisfiable(formula):
    return formula == []


def is_unsatisfiable(formula):
    return any(clause == [] for clause in formula)
     

def is_consistent(literals):
    for lit in literals:
        if -lit in literals:
            return False
    return True


def unit_literals(formula):
    """
    given: 
        formula: list of clauses
    returns:
        set of unit literals
    """
    units = set()
    for clause in formula:
        if len(clause) == 1:
            units.add(clause[0])
    return units


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
        else:
            modified_clause = [x for x in clause if x != -lit]
            modified_formula.append(modified_clause)
    return modified_formula


def pure_literals(formula):
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


def dpll(formula, assignments=set()):
    """
    given:
        formula
    return:
        true and satisfiable assignment or false if unsatisfiable
    """
    if is_satisfiable(formula):
        return SATISFIABLE, sorted(assignments, key=lambda x: abs(x))
    elif is_unsatisfiable(formula):
        return UNSATISFIABLE
    # unit propagation
    units = unit_literals(formula)
    while units:
        if not is_consistent(units):
            return UNSATISFIABLE
        assignments |= units
        for lit in units:
            formula = unit_propagation(formula, lit)
        if is_unsatisfiable(formula):
            return UNSATISFIABLE
        units = unit_literals(formula)
    # pure literal elimination
    pures = pure_literals(formula)
    assignments |= pures
    for lit in pures:
        formula = pure_literal_elimination(formula, lit)
    # choose a literal
    lit = choose_literal(formula)
    if lit:
        return dpll(formula+[[lit]], assignments|set([lit])) or \
               dpll(formula+[[-lit]], assignments|set([-lit]))
    return dpll(formula, assignments)
