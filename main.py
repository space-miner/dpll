import time 
import glob 

import naive_dpll
import lazy_dpll

for test_set in ["uf20-91", "uf50-218", "uuf50-218"]:
    start_time = time.time() 
    for dimacs_file in glob.glob(f"./tests/{test_set}/*.cnf"):
        formula = naive_dpll.parse(dimacs_file)
        naive_dpll.dpll(formula)
    end_time = time.time()
    print(f"naive dpll on {test_set}: {end_time - start_time}s")

    start_time = time.time()
    for dimacs_file in glob.glob(f"./tests/{test_set}/*.cnf"):
        raw_formula = lazy_dpll.parse(dimacs_file)
        formula, variable_map, assignment = lazy_dpll.setup(raw_formula)
        lazy_dpll.dpll(formula, variable_map, assignment)
    end_time = time.time()
    print(f"lazy dpll on {test_set}: {end_time - start_time}s")