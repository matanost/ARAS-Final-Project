
from itertools import combinations
import copy

#Remove redundant clauses, either bacuase they are duplication of clauses, or becuase they're tautologies.
def remove_redundant_clauses(formula):

    formula_copy = copy.deepcopy(formula)
    for clause_comb in combinations(formula,2):
        c1,c2 = clause_comb
        if c1 == c2:
            formula_copy.remove(c2)        
    formula = formula_copy
    formula_copy = copy.deepcopy(formula)
    for clause in formula:
        if len(clause) == 0:
            formula_copy.remove(clause)            
        else :
            for lit_comb in combinations(clause,2):
            l1,l2 = lit_comb
            if l1 == -l2:
                formula_copy.remove(clause)
    return formula_copy                                              
    