What are SAT Solvers and why care?
- given a propositional formula (made from conjunction, disjunction, negation of variables), can tell you if it's satisfiable or not. and if it is give the correct assignment.
- SAT can derive a satisfying propositional backbone for some theories, all theory solvers need to do is some procedure to verify them against
- modern SAT solvers are fast.
- used as part of the machinery that powers smt solvers

SMT Solver
- automated theorem provers
- hardware and software verification


DIMACS format and CNF 
- typically assumes formulas are in conjunctive normal form (CNF).
- anything can be converted to CNF by demorgan laws
- example of CNF: (x1 or x2 or ~x3) and (~x1) and (~x2 or ~x4) and (x2 or x3 or x4) and (x5)
- dimacs format of the above formula:
```
c the characters c and p are ignored
c c is for starting a comment line
c p is for meta data for number of variables and clauses
p cnf 5 4
1 2 -3 0
-1 0
-2 -4 0
2 3 4 0
5 0
```
- clauses are terminated by zeros and the negative for negation of a variable

Unit Propogation
- unit clauses are those where all there is only one unassigned literal and all other literals evaluate to false
- so the only way to satisfy the clause is to assign the proper value to make the unassigned literal true
- examples of units:
(~x1) and (x2 or x3) obviously ~x1 is an unit here as the only way to satisfy the first clause is to make ~x1 true.
suppose we have a clause that looks like (x1 or x2 or ~x3) if we know that x1 or x2 both are both assigned to false then ~x3 is an unit as it's the only unassigned literal in the clause and we want the clause to be true.


Pure Literal Elimination
- literals where no clause in the formula contain the negation of the literal
- example of pure literal:
(x1 or x2) and (~x1 or ~x3 or x4) and (x2 or x3 or ~x4)
here x2 would be a pure since ~x2 does not show up in the formula

DPLL
- do unit propogation and pure literal elimination whenever possible otherwise just make a guess
 

Literal Watching
- idea is to not look through the whole clause searching for units
- keep track of two literals
- update the watched literals to a new unwatched and unassigned literal if there is conflict
- when there is only one literal being watched it is a unit

