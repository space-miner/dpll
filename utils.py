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