SAT = True
UNSAT = False


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


def bcp(formula):
    """
    repeatedly apply unit propogation till either conflict or fix state
    sh
    """
    partial_trail = []
    units = get_units(formula)
    while units:
        if is_consistent(units):
            for lit in units:
                formula = unit_propagation(formula, lit)
                if [] in formula:
                    return "CONFLICT"
            units = get_units(formula)
        else:
            return "CONFLICT"
    return formula


def analyze_conflict(formula, trail):
    """
    compute backtracking level
    detect global unsatisfiability
    adding new constraints on search
    """
     
    pass


def backtrack(level):
    """
    set decision level to level and erase assignments at levels higher
    """
    pass


def cdcl(formula):
    trail = []
    while True:
        if bcp() == "CONFLICT":             # params?
            level = analyze_conflict()      # params?
            if level < 0:
                return UNSAT
            backtrack()                     # params?
        elif bcp() != "CONFLICT":           # params?
            lit = choose_literal(formula)
            if not lit:
                return SAT
            formula = formula + [[lit]]
