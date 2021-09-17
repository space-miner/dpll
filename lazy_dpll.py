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


def setup(raw_formula):
    formula = []
    variables = set()
    for clause in raw_formula:
        ref_a = clause[0]
        ref_b = clause[-1]
        formula.append([clause, ref_a, ref_b])
        variables |= set(abs(lit) for lit in clause)
    variable_map = {var:i for i, var in enumerate(variables)}
    nb_vars = len(variables)
    assignment = [0] * nb_vars
    return formula, variable_map, assignment


def is_satisfiable(formula):
    return formula == []


def is_unsatisfiable(formula):
    for (clause, ref_a, ref_b) in formula:
        if clause == []:
            return True
    return False


def is_consistent(literals):
    for lit in literals:
        if -lit in literals:
            return False
    return True


def is_unassigned(var, variable_map, assignment):
    i = variable_map[var]
    return assignment[i] == 0


def unit_literals(formula):
    units = set()
    for (clause, ref_a, ref_b) in formula:
        if ref_a == ref_b:
            units.add(ref_a)
    return units


def choose_literal(formula, variable_map, assignment):
    for (clause, ref_a, ref_b) in formula:
        var_a = abs(ref_a)
        if is_unassigned(var_a, variable_map, assignment):
            return ref_a
        var_b = abs(ref_b)
        if is_unassigned(var_b, variable_map, assignment):
            return ref_b
    return None


def update_ref(ref, clause, units, variable_map, assignment):
    if -ref in units:
        for lit in clause:
            var = abs(lit)
            if is_unassigned(var, variable_map, assignment):
                return lit
        return None
    return ref


def unit_propagation(formula, units, variable_map, assignment):
    modified_formula = []
    for (clause, ref_a, ref_b) in formula:
        if ref_a in units or ref_b in units:
            continue
        else:
            if -ref_a in units:
                for lit in clause:                  # ref_a starts at the front of the clause and works backwards
                    var = abs(lit)
                    i = variable_map[var]
                    if assignment[i] == lit:   # true literal 
                        break
                    elif assignment[i] == 0:        # unassigned literal
                        ref_a = lit
                        break
                else:
                    ref_a = None                    # no free literals were found
            
            if -ref_b in units:
                for lit in clause[::-1]:            # ref_b starts from the back of the clause and works forward
                    var = abs(lit)
                    i = variable_map[var]
                    if assignment[i] == lit:   # true literal 
                        break
                    elif assignment[i] == 0:        # unassigned literal
                        ref_b = lit
                        break
                else:
                    ref_b = None                    # no free literals were found

            # ref_a or ref_b were not reassigned meaning they hit a true literal
            if (ref_a and -ref_a in units) or (ref_b and -ref_b in units):  
                continue
            # ref_a and ref_b were both unchanged or reassigned
            elif ref_a and ref_b:
                modified_clause = [clause, ref_a, ref_b]
            # ref_a and ref_b are None meaning all the variables in the clause were assigned to false
            else:
                modified_clause = [[], ref_a, ref_b]
            modified_formula.append(modified_clause)
    return modified_formula


def assign_units(units, variable_map, assignment):
    for lit in units:
        var = abs(lit)
        i = variable_map[var]
        assignment[i] = lit
    return assignment


def dpll(formula, variable_map, assignment):
    # satisfiable
    if is_satisfiable(formula):
        return SATISFIABLE, assignment
    # unsatisfiable
    elif is_unsatisfiable(formula):
        return UNSATISFIABLE
    # unresolved
    units = unit_literals(formula) 
    while units:
        if not is_consistent(units):
            return UNSATISFIABLE
        assign_units(units, variable_map, assignment)      
        formula = unit_propagation(formula, units, variable_map, assignment)
        if is_unsatisfiable(formula):
            return UNSATISFIABLE
        units = unit_literals(formula)
    lit = choose_literal(formula, variable_map, assignment)
    if lit:
        return dpll(formula+[[[lit], lit, lit]], variable_map, assignment[:]) or \
            dpll(formula+[[[-lit], -lit, -lit]], variable_map, assignment[:])
    return dpll(formula, variable_map, assignment)
