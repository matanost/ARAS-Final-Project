
from itertools import combinations
import copy

def remove_redundant_clauses(formula):

    formula_copy = copy.deepcopy(formula)
    for clause in formula:
        for lit_comb in combinations(clause,2):
            l1,l2 = tuple(lit_comb)                      
            if l1 == -l2:
                formula_copy.remove(clause)

    return formula_copy
        
                
            
            
